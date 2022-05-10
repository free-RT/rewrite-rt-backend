from core import TypedSanic, setup_app
from sanic import response

from data import Secret

from os import listdir


app = TypedSanic("app")


@app.route("/api")
async def api(request):
    return response.json({"hello": "world"})


for name in os.listdir("blueprints"):
    pass


setup_app(app)

app.run(**Secret["sanic"])
