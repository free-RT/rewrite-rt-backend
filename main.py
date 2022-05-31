from core import TypedSanic, setup_app
from sanic import response

from data import Secret

from os import listdir
from importlib import import_module


app = TypedSanic("app")


@app.route("/api")
async def api(request):
    return response.json({"hello": "world"})


for name in listdir("blueprints"):
    lib = import_module("blueprints.{}".format(name.replace(".py", "")))
    if hasattr(lib, "bp"):
        app.blueprint(lib.bp)
    elif hasattr(lib, "setup"):
        lib.setup(app)


setup_app(app)

app.run(**Secret["sanic"])
