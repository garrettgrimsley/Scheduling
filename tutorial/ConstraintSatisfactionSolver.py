import numpy as np
import simplejson as json
from datetime import time
from timeit import default_timer as timer
from math import ceil


class SuccinctCourse:
    def __init__(self, crn, subject, course_num, section_num, combined):
        self.course_reference_number = crn
        self.subject_code = subject
        self.course_number = course_num
        self.section_number = section_num
        self.combined = [combined]
        self.victoria_bitstring = []

    def build_victoria_bitstring(self):  # Earliest: 07:00. Latest: 23:00. CRN 20816. Nursing courses...
        multi_array = [[False for x in range(65)] for y in range(6)]  # 64 = 16 hours * 4 (15 min blocks)

        def assigner(weekday, position):
            time_start = 1
            time_end = 2

            start_index = int((self.combined[position][time_start].hour - 7) * 4 + ceil(self.combined[position][time_start].minute / 15.0))
            end_index = int((self.combined[position][time_end].hour - 7) * 4 + ceil(self.combined[position][time_end].minute / 15.0))
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
                    elif self.combined[i][0][k] == "S":  # There are 3 classes that occur on Saturday. CRNs 26287 23521 24735
                        assigner(5, i)
        return np.array(multi_array, dtype=bool)  # Turn it into a numpy array before returning it.

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
        there_is_a_conflict = False
        for weekday in self.day:
            if weekday in another_course.day:
                if self.time_start <= another_course.time_end:
                   if self.time_end >= another_course.time_start:
                        there_is_a_conflict = True
                elif self.time_end >= another_course.time_start:
                    if self.time_start <= another_course.time_end:
                        there_is_a_conflict = True
            return there_is_a_conflict

    def false_starting_conflict(self, another_course):
        conflict = True
        for weekday in self.day:
            if weekday in another_course.day:
                if self.time_end < another_course.time_start:
                    conflict = False
                elif another_course.time_end < another_course.time_start:
                    conflict = False
            return conflict

    def __str__(self):
        return str("CRN: {}. Subject-Course#-Section# {}{}-{}. Days: {}. Times: {}-{}".format(
            self.course_reference_number, self.subject_code, self.course_number, self.section_number,
            self.day, self.time_start, self.time_end))


def main():
    chem_102 = np.array([1, 0, 1, 0, 1, 1, 1], bool)
    csc_131 = np.array([0, 0, 0, 1, 0, 1, 0], bool)
    spn_101 = np.array([0, 1, 0, 1, 0, 0, 0], bool)
    print("chem and csc", np.any(np.logical_and(chem_102, csc_131)))
    print("chem and spn", np.any(np.logical_and(chem_102, spn_101)))
    print("chem102 and csc131 after logical and: ", np.logical_and(chem_102, csc_131))
    course_list = json_to_objects("../different_times.json")
    for course in course_list:
        if course.course_reference_number == "" or course.course_reference_number == " ":
            current_index = course_list.index(course)
            course_list[current_index - 1].combined.append(course_list[current_index].combined[0])
    filtered_list = [item for item in course_list if item.course_reference_number != u""]
    course_list = filtered_list
    for course in course_list:
        if course.course_reference_number == "21459":  # {"time_start": "08:00", "course_reference_number": "21459", "section_number": ["003"], "days": ["M", "W", "F"], "subject_code": ["BIO"], "course_number": ["201"], "time_end": "08:50"},
                                                       # {"time_start": "14:00", "course_reference_number": "", "section_number": ["\u00a0"], "days": ["M"], "subject_code": ["\u00a0"], "course_number": ["\u00a0"], "time_end": "16:50"},
            print(course.victoria_bitstring)           # So the output here should include the 08:00-08:50 slots as True in the array
                                                       # and then down at the next "if course.course_reference_number == "21459""
                                                       # it should also have the Monday 14:00-16:50 as True in the array, but it does not
                                                       # Haven't tried to debug this yet, need food.
            break
    for course in course_list:
        course.victoria_bitstring = course.build_victoria_bitstring()
    for course in course_list:
        if course.course_reference_number == "21459":
            print(course.victoria_bitstring)
            break
    start = timer()
    comparisons = 0
    conflicts_detected = 0
    print(course_list[0].victoria_bitstring.shape)
    for course in course_list:
        for course2 in course_list:
            # CRN 20816, 20817, 20818, etc.
            # I think it is an error with how I coded your method. 23 - 7 = 16 * 4 = 64 + 1 = 65 = OUTSIDE ARRAY.
            # Going to bed for now though, will look at it later. Sorry for messy code. Goodnight.
            #if not (course2.conflict_exists(course) == course2.victoria_conflict_exists(course)):
            if course2.victoria_conflict_exists(course):
            #if course2.conflict_exists(course):
                conflicts_detected += 1
                #print(course2.conflict_exists(course))
                #print(course2.victoria_conflict_exists(course))
                #print("Conflict mismatch with courses \n {} and \n {}" .format(course.__str__(), course2.__str__()))
            # Prints if the whether a conflict exists using the time comparison method, then the Victoria bitstring method,
            # then the CRN for which courses we are comparing, and finally whether the two comparisons agree.
            comparisons += 1
    print(timer() - start)  # Run it and see how fast!!! It's even faster if you take everything except your method
    print(comparisons)
    # out of the loop


def classes_conflict(potential_schedule):
    pass


def object_decoder(obj):
    time_start = time(hour=int(obj["time_start"].split(":")[0]), minute=int(obj["time_start"].split(":")[1]))
    time_end = time(hour=int(obj["time_end"].split(":")[0]), minute=int(obj["time_end"].split(":")[1]))
    days = [obj["days"], time_start, time_end]
    return SuccinctCourse(obj["course_reference_number"], obj["subject_code"], obj["course_number"], obj["section_number"], days)


def json_to_objects(filename):
    course_file = open(filename, mode="r")
    return json.load(course_file, object_hook=object_decoder)


class Student:
    def __init__(self, completed_courses):
        self.completed_courses = completed_courses


if __name__ == "__main__":
    main()
