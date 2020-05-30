from util.deco import callback
from util.get_credential import get_secrets
from com.XASession import get_session
import util.logger

logger = util.logger.get()


class Xing:
    session = get_session()

    @classmethod
    def connect(
        cls, demo: str = True,
    ):
        """
        Connect with Ebest secutiry server
        Args:
            demo (str) <True>: True -> demo server / False -> real server
        """
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
        return Xing.session.GetServerName()

    @classmethod
    def is_demo(cls):
        """
        Return True if current connected server is demo server
        """
        if cls.get_servername().startswith("MIS"):
            return False
        else:
            return True

    @classmethod
    @callback
    def login(
        cls,
        demo=None,
        secret_path: str = None,
        id_: str = None,
        pw: str = None,
        cert_pw: str = None,
    ):
        """
        Login into Ebest secutiry server
        Args:
            demo (str) <True>: True -> demo server / False -> real server
            secret_path (str): path in which the secret file exists
            id_ (str): id
            pw (str): password
            cert_pw (str): password for certificate
        """
        logger.info("connection check")
        if not cls.is_connected():
            cls.connect(demo=demo)

        logger.info("login attempt")
        secrets = get_secrets(secret_path)
        id_ = id_ or secrets["ID"]
        pw = pw or (secrets["DEMO_PW"] if cls.is_demo() else secrets["PW"])
        cert_pw = cert_pw or secrets["CERT_PW"]
        cls.session.Login(id_, pw, cert_pw, 0, False)

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
