import os
import win32com

from util.deco import final_post_quit
import util.logger

logger = util.logger.get()


class XAQueryEventHandler:
    """
    Event handler for XAQuery com object
    """

    @final_post_quit
    def OnReceiveData(self, code):
        logger.debug(f"OnReceiveData: code={code}")


def get_xaquery_event_proxy(res, res_path="C:/eBEST/xingAPI/Res/"):
    res_file_name = os.path.join(res_path, res + ".res")
    if not os.path.isfile(res_file_name):
        logger.fatal(f"can't find {res_file_name}")
        raise FileNotFoundError
    event_proxy = win32com.client.DispatchWithEvents(
        "XA_DataSet.XAQuery", XAQueryEventHandler
    )
    event_proxy.ResFileName = res_file_name
    return event_proxy
