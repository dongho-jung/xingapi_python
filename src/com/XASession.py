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
            logger.info("login success")
        else:
            logger.fatal(f"login fail: {msg}")
            if "3회 오류" in msg:
                logger.critical(f"accouint invalidation warning!")
                input("continue?")
            raise AssertionError("login fail")

    @final_post_quit
    def OnDisconnect(self):
        logger.fatal("server disconnected")


def get_session():
    return win32com.client.DispatchWithEvents(
        "XA_Session.XASession", XASessionEventHandler
    )
