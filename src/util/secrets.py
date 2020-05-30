import util.logger

import json
import os

logger = util.logger.get()


def get_secrets(path: str = None):
    """
    Args:
        path (str) <{workingdir/.secrets.json}>: path in which a secret file exists
    Note:
        if there's no secret file, it searches environment variable
    Returns (dict): secret context
    """
    try:
        path = path or os.path.join(os.getcwd(), ".secrets.json")
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        logger.warn(f"can't find secret file: {e}")
        try:
            return {
                "ID": os.environ["XING_ID"],
                "PW": os.environ["XING_PW"],
                "DEMO_PW": os.environ["XING_DEMO_PW"],
                "CERT_PW": os.environ["XING_CERT_PW"],
            }
        except KeyError as e:
            logger.fatal(f"can't find secret information: {e}")
            raise AssertionError
