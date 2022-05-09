from orjson import load
from typing import TypedDict, Dict


class SecretType(TypedDict):
    mysql: dict
    sanic: dict
    
with open("secret.json") as f:
    Secret: SecretType = load(f)
