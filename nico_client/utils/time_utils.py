import time
from datetime import datetime


def get_posix_now():
    return get_posix(datetime.now())


def get_posix(datime_obj):
    return int(time.mktime(datime_obj.utctimetuple()))
