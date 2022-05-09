from sanic import Sanic, response, Request
from sanic.exceptions import SanicException
from sanic_mysql import ExtendMySQL
from data import Secret
from miko.manager import Manager
from os.path import exists

PATH = "rt-frontend"
class TypedSanic(Sanic):
    pass


def setup_app(app: TypedSanic):
    app.ctx.mysql = ExtendMySQL(**Secret["mysql"])
    app.ctx.miko = Manager()
    
    async def _template(path: str, **kwargs):
        return response.html(await app.ctx.miko.aiorender("{}/{}".format(PATH, path)))
    app.ctx.template = _template
    
    @app.on_request
    async def response_content(request: Request):
        if (request.host == "localhost"
            or request.host == "free-rt.com"):
            if exists(f"{PATH}/{request.path}"):
                return await app.ctx.template(request.path)
            else:
                raise SanicException("あれ？ここどこだ？真っ白な壁がずっと続いているよ", status_code=404)
