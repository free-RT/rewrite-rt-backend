from sanic import Blueprint, Request, response


bp = Blueprint("api")


@bp.get("/")
async def main(request: Request):
    return response.json(
        {
            "status": 200
        }
    )
