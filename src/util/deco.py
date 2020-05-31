import ctypes
import functools
import signal
import threading

import pythoncom

import util.logger


def signal_handler(signum, frame):
    ctypes.windll.user32.PostQuitMessage(0)
    raise KeyboardInterrupt


logger = util.logger.get()
signal.signal(signal.SIGINT, signal_handler)


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


def post_quit():
    ctypes.windll.user32.PostQuitMessage(0)


def final_post_quit(func):
    """
    send WM_QUIT message for callback after the func
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            func(*args, **kwargs)
        finally:
            post_quit()

    return inner


def timeout(wait_sec: int = 5):
    def deco(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            res = [Exception(f"{func.__name__} timeout {wait_sec} seconds")]

            def target():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e

            t = threading.Thread(target=target)
            t.daemon = True
            try:
                t.start()
                t.join(wait_sec)
            except Exception as e:
                logger.fatal("starting thread error")
                raise e
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret

        return inner

    return deco
