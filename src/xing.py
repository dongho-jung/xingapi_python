from util.deco import callback
from util.get_credential import get_secrets
from com.XASession import get_session
import util.logger

logger = util.logger.get()
Session = get_session()


class Xing:
    @staticmethod
    @callback
    def login(
        demo: str = True,
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
        url = "demo.ebestsec.co.kr" if demo else "hts.ebestsec.co.kr"
        port = 20001
        Session.ConnectServer(url, port)

        logger.info(f"Login attempt: {url}:{port}")
        secrets = get_secrets(secret_path)
        id_ = id_ or secrets["ID"]
        pw = pw or (secrets["DEMO_PW"] if demo else secrets["PW"])
        cert_pw = cert_pw or secrets["CERT_PW"]
        Session.Login(id_, pw, cert_pw, 0, False)
