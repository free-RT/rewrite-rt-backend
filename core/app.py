from sanic import Sanic
from sanic_mysql import ExtendMySQL
from data import Secret


class TypedSanic(Sanic):
    pass


def setup_app(app: TypedSanic):
    app.ctx.mysql = ExtendMySQL(**Secret["mysql"])
    
    @app.on_request
    async def response_content(request):
        if (request.host == "localhost"
            or request.host == "free-rt.com"):
            pass
        
