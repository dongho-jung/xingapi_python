import ctypes
import functools

import pythoncom

import util.logger

logger = util.logger.get()


def callback(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        pythoncom.PumpMessages()

    return inner


def final_post_quit(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            ctypes.windll.user32.PostQuitMessage(0)

    return inner
