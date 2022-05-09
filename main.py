from core import TypedSanic, setup_app
from sanic import response
from data import Secret


app = TypedSanic("app")


@app.route("/api")
async def api(request):
    return response.json({"hello": "world"})


setup_app(app)

app.run(**Secret["sanic"])
