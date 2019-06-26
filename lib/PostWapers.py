from functools import partial, wraps
import time

def metricsDecoretor(func, **kwargs):

    @wraps(func)
    def __wapper_func(*args, **kwargs):
        # time elasped or hanlding request
        start = time.time()
        rest = func(*args, **kwargs)
        end = time.time() - start
        print("Time Elasped: {:.4f} s".format(end))
        return rest 

    return __wapper_func