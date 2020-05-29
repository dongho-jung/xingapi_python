import json
import pathlib

with open(pathlib.Path(__file__).parent / ".secrets.json") as f:
    secrets = json.load(f)
