import os

import logging as _logging

ROOT = "xingapi"


def get(base="src", root=ROOT):
    base_path = os.path.normpath(__file__).rsplit(base, 1)[-1]
    logger_name = root + base_path.replace(os.sep, ".").rsplit(".", 1)[0]
    return _logging.getLogger(logger_name)


_logging.basicConfig(
    level=_logging.DEBUG,
    format="%(asctime)s    %(name)-12s    %(levelname)-8s    %(message)s",
    datefmt="%m-%d %H:%M",
)
