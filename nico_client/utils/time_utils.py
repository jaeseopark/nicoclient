import time
from datetime import datetime


def get_posix_now():
    return get_posix(datetime.now())


def get_posix(datime_obj):
    utc = datime_obj.utctimetuple()
    t = time.mktime(utc)
    return int(t)


def str_to_posix(date_str):
    """
    Converts datetime_str to datetime_int

    :param date_str: A string representation of datetime. The format is "YYYY/mm/DD HH:MM" (16 characters).
                     If the string is bigger than 16 characters long, then it gets truncated.
    :return: A posix/integer representation of datetime
    """
    dt = datetime.strptime(date_str[:16], "%Y/%m/%d %H:%M")
    return get_posix(dt)
