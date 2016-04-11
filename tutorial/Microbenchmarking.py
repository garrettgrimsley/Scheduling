def test_string_comparison():
    """String comparison timings"""
    day1 = "M"
    day2 = "M"
    if day1 == day2:
        pass


def test_integer_comparison():
    day1 = 0
    day2 = 0
    if day1 == day2:
        pass


def test_string_in_dict():
    dict1 = {"M": ""}
    dict2 = {"M": ""}
    for key in list(dict1.keys()):
        if key in dict2:
            pass


def test_integer_in_dict():
    dict1 = {1: ""}
    dict2 = {1: ""}
    for key in list(dict1.keys()):
        if key in dict2:
            pass


def linear_membership():
    list1 = [1, 3, 5]
    day = 5
    if day in list1:
        pass


def dict_membership():
    dict1 = {"M": "", "W": "", "F": ""}
    day = "F"
    if day in dict1:
        pass


if __name__ == "__main__":
    import timeit

    print("Integer comparison",
        timeit.timeit("test_integer_comparison()", setup="from __main__ import test_integer_comparison", number=100000000))
    print("String comparison",
        timeit.timeit("test_string_comparison()", setup="from __main__ import test_string_comparison", number=100000000))
    print("String in dict",
          timeit.timeit("test_string_in_dict()", setup="from __main__ import test_string_in_dict", number=10000000))
    print("Integer in dict",
          timeit.timeit("test_integer_in_dict()", setup="from __main__ import test_integer_in_dict", number=10000000))
    print("Linear membership",
          timeit.timeit("linear_membership()", setup="from __main__ import linear_membership", number=100000000))
    print("Dictionary membership",
          timeit.timeit("dict_membership()", setup="from __main__ import dict_membership", number=100000000))