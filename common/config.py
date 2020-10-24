import json
from types import SimpleNamespace


def read_config():
    with open('config.json', 'r') as f:
        return json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
