import json
import os


def get_secrets(path: str = None):
    """
    Args:
        path (str) <{workingdir/.secrets.json}>: path in which a secret file exists
    Returns (dict): secret context
    """
    path = path or os.path.join(os.getcwd(), ".secrets.json")
    with open(path) as f:
        return json.load(f)
