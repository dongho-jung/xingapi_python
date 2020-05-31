import os
import win32com

from util.deco import final_post_quit


class XAQueryEventHandler:
    """
    Event handler for XAQuery com object
    """

    @final_post_quit
    def OnReceiveData(self, code):
        pass


def get_xaquery_event_proxy(res, res_path="C:/eBEST/xingAPI/Res/"):
    event_proxy = win32com.client.DispatchWithEvents(
        "XA_DataSet.XAQuery", XAQueryEventHandler
    )
    event_proxy.ResFileName = os.path.join(res_path, res + ".res")
    return event_proxy
