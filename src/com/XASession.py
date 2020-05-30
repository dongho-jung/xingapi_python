import win32com.client

from util.deco import final_post_quit
import util.logger

logger = util.logger.get()


class XASessionEventHandler:
    """
    Event handler for XASession com object
    """

    @final_post_quit
    def OnLogin(self, code, msg):
        if code == "0000":
            logger.info("Login success")
        else:
            logger.fatal(f"Login fail: {msg}")
            raise AssertionError("Login fail")


def get_session():
    return win32com.client.DispatchWithEvents(
        "XA_Session.XASession", XASessionEventHandler
    )
