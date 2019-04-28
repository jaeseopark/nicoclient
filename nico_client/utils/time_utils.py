import time
from datetime import datetime


def get_posix_now():
    return get_posix(datetime.now())


def get_posix(datime_obj):
    utc = datime_obj.utctimetuple()
    t = time.mktime(utc)
    return int(t)
