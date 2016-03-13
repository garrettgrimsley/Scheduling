import numpy as np
import simplejson as json
from datetime import time
from timeit import default_timer as timer
from math import ceil


def main():
    chem_102 = np.array([1, 0, 1, 0, 1, 1, 1], bool)
    csc_131 = np.array([0, 0, 0, 1, 0, 1, 0], bool)
    spn_101 = np.array([0, 1, 0, 1, 0, 0, 0], bool)
    print("chem and csc", np.any(np.logical_and(chem_102, csc_131)))
    print("chem and spn", np.any(np.logical_and(chem_102, spn_101)))
    print("chem102 and csc131 after logical and: ", np.logical_and(chem_102, csc_131))
    course_list = json_to_objects()
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
    obj((obj["days"]), obj(["time_start"]), obj(["time_end"]))
    return SuccinctCourse(obj["course_reference_number"], obj["subject_code"], obj["course_number"], obj["section_number"], obj["days"], obj["time_start"], obj["time_end"])


def json_to_objects():
    course_file = open("../smallout.json", mode="r")
    return json.load(course_file, object_hook=object_decoder)


class SuccinctCourse:
    def __init__(self, crn, subject, course_num, section_num, day, time_start, time_end):
        self.course_reference_number = crn
        self.subject_code = subject
        self.course_number = course_num
        self.section_number = section_num
        self.day = day
        self.time_start = time(hour=int(time_start.split(":")[0]), minute=int(time_start.split(":")[1]))
        self.time_end = time(hour=int(time_end.split(":")[0]), minute=int(time_end.split(":")[1]))
        self.victoria_bitstring = self.build_victoria_bitstring()

    def build_victoria_bitstring(self):  # Earliest: 07:00. Latest: 23:00. CRN 20816. Nursing courses...
        multi_array = [[False for x in range(65)] for y in range(6)]  # 64 = 16 hours * 4 (15 min blocks)

        def assigner(weekday):
            start_index = int((self.time_start.hour - 7) * 4 + ceil(self.time_start.minute / 15.0))
            end_index = int((self.time_end.hour - 7) * 4 + ceil(self.time_end.minute / 15.0))
            if not self.time_end.minute % 15:
                end_index += 1
            multi_array[weekday][start_index:end_index] = [True] * (end_index - start_index)
        for course_day in self.day:
            if course_day == "M":
                assigner(0)
            elif course_day == "T":
                assigner(1)
            elif course_day == "W":
                assigner(2)
            elif course_day == "R":
                assigner(3)
            elif course_day == "F":
                assigner(4)
            elif course_day == "S":  # There are 3 classes that occur on Saturday. CRNs 26287 23521 24735
                assigner(5)
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


class Student:
    def __init__(self, completed_courses):
        self.completed_courses = completed_courses

if __name__ == "__main__":
    main()
