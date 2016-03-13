import scrapy


def serialize_course_reference_number(crn):
        return str(crn[0])


def serialize_days(days):
    if "\u00a0" in days:
        return ""
    else:
        return list(days[0])


def serialize_time_start(time_start):
    time_string = time_start[0].split("-")[0]
    if "am" in time_string:
        hour_and_min = time_string.split(":")
        return str(int(hour_and_min[0])).zfill(2) + ":" + str(int(hour_and_min[1][:2])).zfill(2)
    elif "pm" in time_string:
        hour_and_min = time_string.split(":")
        if int(hour_and_min[0]) != 12:
            return str(int(hour_and_min[0]) + 12).zfill(2) + ":" + str(int(hour_and_min[1][:2])).zfill(2)
            # return time(int(hour_and_min[0] + 12, int(hour_and_min[1][:2])))
        else:
            return str(int(hour_and_min[0])).zfill(2) + ":" + str(int(hour_and_min[1][:2])).zfill(2)
            # return time(int(hour_and_min[0], int(hour_and_min[1][:2])))


def serialize_time_end(time_end):
    time_string = time_end[0].split("-")[1]
    if "am" in time_string:
        hour_and_min = time_string.split(":")
        return str(int(hour_and_min[0])).zfill(2) + ":" + str(int(hour_and_min[1][:2])).zfill(2)
        # return time(int(hour_and_min[0]), int(hour_and_min[1][:2]))
    elif "pm" in time_string:
        hour_and_min = time_string.split(":")
        if int(hour_and_min[0]) != 12:
            return str(int(hour_and_min[0]) + 12).zfill(2) + ":" + str(int(hour_and_min[1][:2])).zfill(2)
            # return time(int(hour_and_min[0] + 12, int(hour_and_min[1][:2])))
        else:
            return str(int(hour_and_min[0])).zfill(2) + ":" + str(int(hour_and_min[1][:2])).zfill(2)
            # return time(int(hour_and_min[0], int(hour_and_min[1][:2])))


def serialize_subject_code(subject_code):
    return subject_code[0]


def serialize_section_number(section_number):
    return section_number[0]


class TimeItem(scrapy.Item):
    day = scrapy.Field()
    time = scrapy.Field()


class CourseItem(scrapy.Item):
    selectable = scrapy.Field()
    course_reference_number = scrapy.Field(serializer=serialize_course_reference_number)
    subject_code = scrapy.Field()
    course_number = scrapy.Field()
    section_number = scrapy.Field()
    campus = scrapy.Field()
    credit_hours = scrapy.Field()
    course_title = scrapy.Field()
    days = scrapy.Field(serializer=serialize_days)   # Critical
    time_start = scrapy.Field(serializer=serialize_time_start)  # Critical
    time_end = scrapy.Field(serializer=serialize_time_end)
    section_capacity = scrapy.Field()
    section_actual = scrapy.Field()  # Number enrolled
    section_remaining = scrapy.Field()  # Seats available, possibly negative.
    waitlist_capacity = scrapy.Field()
    waitlist_actual = scrapy.Field()  # Number wait listed
    waitlist_remaining = scrapy.Field()
    reserved_remaining = scrapy.Field()  # Some seats reserved for new admits.
    instructor = scrapy.Field()
    date = scrapy.Field()  # Critical
    location = scrapy.Field()  # Building code and room number.
    attribute = scrapy.Field()  # List of requirements a course satisfies.
