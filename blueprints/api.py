from sanic import Blueprint, Request

from core import response


bp = Blueprint("api")


@bp.get("/")
async def main(request: Request):
    return response.json({"url": "https://free-rt.com"}, message="本当にここは何もないよ、どこかに戻った方がいいよ")
