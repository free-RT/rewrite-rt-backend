from sanic import response
from orjson import dumps


def json(data: dict, *, message="", status: int=200):
    payload = {
        "status": status,
        "message": message,
        "data": data
    }
    return response.json(payload, status=status, dumps=dumps)
