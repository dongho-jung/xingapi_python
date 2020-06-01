from functools import lru_cache
from typing import Union, Optional

import pandas as pd

from util.deco import callback, post_quit, timeout
from util.finder import find_res
from util.parser import ResParser
from util.secrets import get_secrets
from com.XASession import get_session
from com.XAQuery import get_xaquery_event_proxy
import util.logger

logger = util.logger.get()


class Xing:
    session = get_session()

    @classmethod
    @lru_cache(maxsize=None)
    def get_xaquery_event_proxy_from_pool(cls, res):
        return get_xaquery_event_proxy(res)

    @classmethod
    def connect(
        cls, demo: bool = True,
    ):
        """
        Connect with Ebest secutiry server
        Args:
            demo (bool) <True>: True -> demo server / False -> real server
        """
        if cls.is_connected():
            cls.disconnect()

        url = "demo.ebestsec.co.kr" if demo else "hts.ebestsec.co.kr"
        port = 20001
        logger.info(f"connect attempt: {url}:{port}")
        cls.session.ConnectServer(url, port)

    @classmethod
    def disconnect(cls):
        """
        Disconnect with Ebest secutiry server
        """
        cls.session.DisconnectServer()

    @classmethod
    def is_connected(cls):
        return cls.session.IsConnected()

    @classmethod
    def get_servername(cls):
        """
        Return current connected server name
        """
        if cls.is_connected():
            servername = Xing.session.GetServerName()
            if servername.strip():
                return servername
            else:
                raise AssertionError("not yet login")
        else:
            raise AssertionError("not yet connected")

    @classmethod
    def is_demo(cls):
        """
        Return True if current connected server is demo server
        """
        if cls.get_servername().startswith("MIS"):
            return True
        else:
            return False

    @classmethod
    @callback
    def login(
        cls,
        demo: bool = True,
        secret_path: str = None,
        id_: str = None,
        pw: str = None,
        cert_pw: str = None,
    ):
        """
        Login to Ebest secutiry server
        Args:
            demo (bool) <True>: True -> demo server / False -> real server
            secret_path (str): path in which the secret file exists
            id_ (str): id
            pw (str): password
            cert_pw (str): password for certificate
        """
        logger.info("connection check")
        if not cls.is_connected():
            logger.warning("not yet connected")
            cls.connect(demo=demo)
        elif cls.is_login():
            if cls.is_demo() is not demo:
                logger.warning(f"alredy connected but server is different")
                cls.connect(demo=demo)
            else:
                logger.info("already login")
                post_quit()
                return
        logger.info("login attempt")
        secrets = get_secrets(secret_path)
        id_ = id_ or secrets["ID"]
        pw = pw or (secrets["DEMO_PW"] if demo else secrets["PW"])
        cert_pw = cert_pw or secrets["CERT_PW"]
        cls.session.Login(id_, pw, cert_pw, 0, False)

    @classmethod
    def is_login(cls):
        try:
            cls.get_servername()
        except AssertionError:
            return False
        else:
            return True

    @classmethod
    def get_account_count(cls):
        return cls.session.GetAccountListCount()

    @classmethod
    def get_account(cls, i):
        return cls.session.GetAccountList(i)

    @classmethod
    def get_account_name(cls, account_number):
        return cls.session.GetAccountName(account_number)

    @classmethod
    def get_account_detail_name(cls, account_number):
        return cls.session.GetAcctDetailName(account_number)

    @classmethod
    def get_account_nickname(cls, account_number):
        return cls.session.GetAcctNickname(account_number)

    @classmethod
    def get_error_message(cls, error_code):
        return cls.session.GetErrorMessage(error_code)

    @classmethod
    def get_last_error(cls, with_msg: bool = False):
        error_code = cls.session.GetLastError()
        if with_msg:
            return error_code, cls.get_error_message(error_code)
        return error_code

    @classmethod
    @callback
    def request(
        cls, res, in_block, i: Optional[int] = None,
    ):
        proxy = cls.get_xaquery_event_proxy_from_pool(res)

        @timeout()
        def set_field_data(key_, value_):
            proxy.SetFieldData(f"{res}InBlock{'' if i is None else i}", key_, 0, value_)

        for key, value in in_block.items():
            set_field_data(key, value)
        res = proxy.Request(0)
        if res < 0:
            logger.fatal(f"request fail: {res} -> {cls.get_error_message(res)}")
            post_quit()
            raise AssertionError(res)
        return res

    @classmethod
    def get(
        cls,
        res,
        fields: Union[list, str],
        i: Optional[int] = None,
        n: Optional[int] = None,
    ):

        proxy = cls.get_xaquery_event_proxy_from_pool(res)
        block_name = f"{res}OutBlock{'' if i is None else i}"
        block_count = proxy.GetBlockCount(block_name)
        n = n or block_count

        if not isinstance(fields, list):
            fields = [fields]

        return pd.DataFrame(
            {k: proxy.GetFieldData(block_name, k, i) for k in fields} for i in range(n)
        )

    @classmethod
    def help(cls, res, res_path=None, as_json=False):
        with open(find_res(res, res_path)) as f:
            parsed_res = ResParser.parse(f.read())["FUNC_BLOCK"]
            if as_json:
                return parsed_res
            else:
                parsed_res_string = parsed_res["__FUNC_META"][1] + "\n"
                for data_block in parsed_res["DATA_BLOCKS"]:
                    parsed_res_string += " ".join(data_block.pop("__DATA_META")) + "\n"
                    for field, value in data_block.items():
                        parsed_res_string += f"\t{field} {value['desc']} {value['type']} {value['size']}\n"
                return parsed_res_string

    @staticmethod
    def set_log_level(level):
        util.logger.set_level(level)
