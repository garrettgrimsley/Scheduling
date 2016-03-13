# This file is not part of our project.
#
# import random
# import time
#
#
# def find_max(a_list):
#     a_max = a_list[0]
#     assignment_count = 1
#     for x in range(len(a_list)):
#         if a_list[x] > a_max:
#             assignment_count += 1
#             a_max = a_list[x]
#     return assignment_count
#
#
# def main():
#     start_time = time.time()
#     trials = 5000
#     sum_random_in_range = 0
#     for x in range(trials):
#         random_in_range = [int(1000*random.uniform(0, 1)) for i in range(1000)]
#         sum_random_in_range += find_max(random_in_range)
#
#     execution_time = time.time() - start_time
#     print("Executed in", execution_time, "seconds.")  # Way faster if using PyPy JIT.
#     print(sum_random_in_range / trials, "reassignments.")
#
#
# if __name__ == "__main__":
#     main()
