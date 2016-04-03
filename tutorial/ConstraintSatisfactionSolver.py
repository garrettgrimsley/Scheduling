from __future__ import print_function

import numpy as np
import simplejson as json
from datetime import time
from timeit import default_timer as timer
from math import ceil
from random import randrange
from itertools import product
import numba


class SuccinctCourse(object):
    def __init__(self, crn, subject, course_num, section_num, combined):
        self.course_reference_number = crn
        self.subject_code = subject
        self.course_number = course_num
        self.section_number = section_num
        self.combined = [combined]
        self.day_time = {}
        self.victoria_bitstring = []

    def build_victoria_bitstring(self):  # Earliest: 07:00. Latest: 23:00. CRN 20816. Nursing courses...
        multi_array = [[False for x in range(65)] for y in range(6)]  # 64 = 16 hours * 4 (15 min blocks)

        def assigner(weekday, position):
            time_start = 1
            time_end = 2

            start_index = int((self.combined[position][time_start].hour - 7) * 4 + ceil(self.combined[position]
                                                                                        [time_start].minute / 15.0))
            end_index = int((self.combined[position][time_end].hour - 7) * 4 + ceil(self.combined[position]
                                                                                    [time_end].minute / 15.0))
            if not self.combined[position][time_end].minute % 15:
                end_index += 1
            multi_array[weekday][start_index:end_index] = [True] * (end_index - start_index)
        for i in range(len(self.combined)):
                for k in range(len(self.combined[i][0])):
                    if self.combined[i][0][k] == "M":
                        assigner(0, i)
                    elif self.combined[i][0][k] == "T":
                        assigner(1, i)
                    elif self.combined[i][0][k] == "W":
                        assigner(2, i)
                    elif self.combined[i][0][k] == "R":
                        assigner(3, i)
                    elif self.combined[i][0][k] == "F":
                        assigner(4, i)
                    elif self.combined[i][0][k] == "S":  # At least 3 classes occur on Saturday. CRNs 26287 23521 24735
                        assigner(5, i)
        return multi_array

    def build_day_time(self):
        for item in self.combined:
            for day in item[0]:
                self.day_time.setdefault(day, []).append((item[1], item[2]))

    def victoria_conflict_exists(self, another_course):
        return np.any(np.logical_and(self.victoria_bitstring, another_course.victoria_bitstring))

    def build_garrett_bitstring(self):
        pass

    def garrett_conflict_exists(self, another_course):
        pass

    def conflict_exists(self, another_course):
        """
        :type self: SuccinctCourse
        :type another_course: SuccinctCourse
        """
        if self.subject_code + self.course_number == another_course.subject_code + another_course.course_number:
            return True
        time_start = 0
        time_end = 1
        for day in self.day_time.keys():
            if day in another_course.day_time:
                for time_slot in self.day_time[day]:
                    for other_time_slots in another_course.day_time[day]:
                        if time_slot[time_start] <= other_time_slots[time_end]:
                            if time_slot[time_end] >= other_time_slots[time_start]:
                                return True
                        elif time_slot[time_end] >= other_time_slots[time_start]:
                            if time_slot[time_start] <= other_time_slots[time_end]:
                                return True
        return False

    def __str__(self):
        return str("CRN: {}. Subject-Course#-Section# {}{}-{}. Combined {}".format(
            self.course_reference_number, self.subject_code, self.course_number, self.section_number,
            self.combined))


def main():
    course_list = json_to_objects("../resources/different_times.json")
    for course in course_list:
        if course.course_reference_number == "" or course.course_reference_number == " ":
            current_index = course_list.index(course)
            course_list[current_index - 1].combined.append(course_list[current_index].combined[0])
    filtered_list = [item for item in course_list if item.course_reference_number != u""]
    course_list = filtered_list
    for course in course_list:
        course.build_day_time()
        course.victoria_bitstring = course.build_victoria_bitstring()
    unique_timeslots = []
    for course in course_list:
        if course.combined not in unique_timeslots:
            unique_timeslots.append(course.combined)
    # cpp_declarations(course_list)
    # print("Number on courses on number_of_courses_on("Fri", course_list))
    # print("Number of unique timeslot configurations:", len(unique_timeslots))
    start = timer()

    brute_force_schedule_generator(course_list, 5)
    print(timer() - start)


def number_of_courses_on(day_of_week, course_list):
    course_count = 0
    days = ["mo", "tu", "we", "th", "fr", "sa", "su"]
    days_alias = ["M",   "T",    "W",  "R",   "F",   "S",   "U"]
    day_code = days_alias[days.index(day_of_week[:2].lower())]
    for lets_see in course_list:
        if day_code in lets_see.day_time:
            course_count += 1
    return day_of_week, course_count


def cpp_declarations(course_list):
    out_list = file("get_out.txt", mode='w')
    crn_bitstring = [(x.course_reference_number, x.victoria_bitstring) for x in course_list]
    for entry in range(len(crn_bitstring)):
        array = "{}".format(course_list[entry].victoria_bitstring).replace("[", "{").replace("]", "}")
        outline = str.lower(str("courses[{}].crn = \"{}\", courses[{}].bitstring.assign({});"
                                .format(entry, course_list[entry].course_reference_number, entry, array)))
        out_list.write(outline)
        out_list.write("\n")


@numba.jit
def numba_try(course_list):
    start = timer()
    comparisons = 0
    conflicts_detected = 0
    for course in course_list:
        for course2 in course_list:
            if course2.victoria_conflict_exists(course):
                conflicts_detected += 1
            comparisons += 1
    print("Time:", timer() - start, "Comparisons:", comparisons, "Conflicts detected", conflicts_detected)


def crossover(parent1, parent2):
    offspring = list()
    offspring.append(parent1[:len(parent1)/2])
    offspring.append(parent2[len(parent2) - (len(parent1) / 2) - 1:])
    return offspring


def mutate(schedule, course_list):
    n = len(course_list)
    j = randrange(0, len(schedule))
    i = randrange(0, n)
    for x in range(1000):  # Attempt to perform the mutation a maximum of 1000 times.
        if schedule[j] != course_list[i]:
            schedule[j] = course_list[i]
            return schedule
    return schedule


def fitness(schedule, preferred_courses):
    fitness_score = 0
    for course in schedule:
        if course.subject_code + course.course_number in preferred_courses:
            fitness_score += 1
    return fitness_score


def choose_parents(population):
    selection_range = len(population)/2
    parent1 = randrange(selection_range)
    parent2 = randrange(selection_range)
    while parent1 == parent2:
        parent2 = randrange(selection_range)
    return population[parent1], population[parent2]


def random_choose():
    pass


def elitist_choose():
    pass


def generate_starting_population(course_list, preferred_courses, schedule_length, population_size):
    schedule_population = []
    potential_schedule = []
    while len(schedule_population) < population_size:
        for i in range(schedule_length):
            potential_schedule.append(course_list[randrange(len(course_list))])
        schedule_fitness = fitness(potential_schedule, preferred_courses)
        if not classes_conflict(potential_schedule) and schedule_fitness >= 1:
            schedule_population.append((schedule_fitness, potential_schedule))
    return schedule_population


def genetic_algorithm(course_list, preferred_courses):
    schedule_length = 6
    population_size = 50
    population = generate_starting_population(course_list, preferred_courses, schedule_length, population_size)
    population = sorted(population)
    generation = 0
    while generation < 10:
        new_population = [population[0], population[1]]
        while len(new_population) < 50:
            parent1, parent2 = choose_parents(population)
            offspring = crossover(parent1[1], parent2[1])
            mutate(offspring, course_list)
        generation += 1
    return population[0]


def apply_constraints(course_list):
    preferred = input(print("Input preferred courses: ")).split()
    filtered_courses = [item for item in course_list if item.course_reference_number != u""]
    print(preferred, "\n", filtered_courses)


def brute_force_schedule_generator(course_list, schedule_length):
    lists = []
    for i in range(schedule_length):
        lists.append(course_list[:10])
    schedule_checks= 0
    for items in product(*lists):
        if not classes_conflict(items):
            schedule_checks += 1
        else:
            schedule_checks += 1
    print("Schedule checks processed: {:,}".format(schedule_checks))


def random_schedule_generator(course_list, schedule_length):
    random_schedule = []
    for x in range(schedule_length):
        random_schedule.append(course_list[randrange(0, schedule_length)])
    return random_schedule


def classes_conflict(potential_schedule):
    for one_course in potential_schedule:
        for another_course in potential_schedule:
            if one_course != another_course:
                if one_course.conflict_exists(another_course):
                    return True
    return False


def object_decoder(obj):
    time_start = time(hour=int(obj["time_start"].split(":")[0]), minute=int(obj["time_start"].split(":")[1]))
    time_end = time(hour=int(obj["time_end"].split(":")[0]), minute=int(obj["time_end"].split(":")[1]))
    days = [obj["days"], time_start, time_end]
    return SuccinctCourse(obj["course_reference_number"],
                          obj["subject_code"],
                          obj["course_number"],
                          obj["section_number"], days)


def json_to_objects(filename):
    course_file = open(filename, mode="r")
    return json.load(course_file, object_hook=object_decoder)


if __name__ == "__main__":
    main()
