from orjson import loads
from typing import TypedDict, Dict


class SecretType(TypedDict):
    mysql: dict
    sanic: dict
    hcaptcha: str
    discord: dict
    
with open("secret.json") as f:
    Secret: SecretType = loads(f.read())
