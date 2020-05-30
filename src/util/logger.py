import os

import logging as _logging

ROOT = "xingapi"


def get(base: str = "src", root: str = ROOT):
    """
    return a new logger with a name based on the module path
    Args:
        base (str) <src>: least common path for the name excluding itself.
                          e.g. xingapi/src/util/get_credential -> util/credential
        root (str) <ROOT>: root name.
                          e.g. xingapi/src/util/get_credential -> {ROOT}.util.get_credential
    Returns (logging.Logger)
    """
    base_path = os.path.normpath(__file__).rsplit(base, 1)[-1]
    logger_name = root + base_path.replace(os.sep, ".").rsplit(".", 1)[0]
    return _logging.getLogger(logger_name)


_logging.basicConfig(
    level=_logging.DEBUG,
    format="%(asctime)s    %(name)-12s    %(levelname)-8s    %(message)s",
    datefmt="%m-%d %H:%M",
)
