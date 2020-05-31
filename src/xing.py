from functools import lru_cache
from typing import Union

from util.deco import callback, post_quit
from util.secrets import get_secrets
from com.XASession import get_session
from com.XAQuery import get_xaquery_event_proxy
import util.logger

logger = util.logger.get()


class Xing:
    session = get_session()

    @classmethod
    @lru_cache(maxsize=32)
    def get_event_from_pool(cls, res):
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
        Login into Ebest secutiry server
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
    @callback
    def request(cls, res, in_block):
        proxy = cls.get_event_from_pool(res)
        for key, value in in_block.items():
            proxy.SetFieldData(f"{res}InBlock", key, 0, value)

        proxy.Request(0)

    @classmethod
    def get(cls, res, fields: Union[list, str]):
        proxy = cls.get_event_from_pool(res)
        if isinstance(fields, str):
            return proxy.GetFieldData(f"{res}OutBlock", fields, 0)
        else:
            return {k: proxy.GetFieldData(f"{res}OutBlock", k, 0) for k in fields}
