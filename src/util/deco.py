import ctypes
import functools

import pythoncom

import util.logger

logger = util.logger.get()


def callback(func):
    """
    a decorator for callback. when you use win32com.client.DispatchWithEvents
    you need to pump the message after you send or trigger something and this
    deco make it automatically.

    this deco is pair with @final_post_quit because pythoncom.PumpMessages would
    wait until a WM_QUIT message.
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        pythoncom.PumpMessages()

    return inner


def final_post_quit(func):
    """
    send WM_QUIT message for callback after the func
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            ctypes.windll.user32.PostQuitMessage(0)

    return inner
