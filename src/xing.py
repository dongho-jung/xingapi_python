from util.deco import callback
from util.get_credential import secrets
from com.XASession import get_session
import util.logger

logger = util.logger.get()

Session = get_session()


class Xing:
    @staticmethod
    @callback
    def login(demo=True, id_=None, pw=None, cert_pw=None):
        url = "demo.ebestsec.co.kr" if demo else "hts.ebestsec.co.kr"
        port = 20001
        Session.ConnectServer(url, port)

        logger.info(f"Login attempt: {url}:{port}")
        id_ = id_ or secrets["ID"]
        pw = pw or (secrets["DEMO_PW"] if demo else secrets["PW"])
        cert_pw = cert_pw or secrets["CERT_PW"]
        Session.Login(id_, pw, cert_pw, 0, False)
