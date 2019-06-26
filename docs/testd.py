#!/usr/bin/env python
import time
from functools import wraps


def warper(func):

    print(">go in side")
    @wraps(func)
    def __warper(*args, **kwargs):
        start = time.time()
        print(" >>> do task", func.__name__)
        time.sleep(1)
        rest = func(*args, **kwargs)
        end = time.time() -  start
        print("<<go outside, time elasped: {}s".format(end) )
        return rest

    print("<<go..." )

    return __warper


@warper
def TaskFunc(name="do task", task_id=1):

    print(name, task_id)
    message = "{}.{}".format(name, task_id)
    #return message


TaskFunc(name="do task1", task_id=1)


