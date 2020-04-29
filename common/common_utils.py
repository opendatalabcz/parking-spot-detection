import base64


def serialize_bytes(bytes):
    return base64.encodebytes(bytes).decode("UTF-8")


def deserialize_bytes(src):
    return base64.decodebytes(src.encode("UTF-8"))


import functools
import time


def timed(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer
