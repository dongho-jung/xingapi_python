import os

import util.logger

logger = util.logger.get()


def find_res(res, res_path=None):
    res_path = res_path or "C:/eBEST/xingAPI/Res/"

    res_file_name = os.path.join(res_path, res + ".res")
    if not os.path.isfile(res_file_name):
        logger.fatal(f"can't find {res_file_name}")
        raise FileNotFoundError
    return res_file_name
