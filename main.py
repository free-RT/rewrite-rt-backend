from core import TypedSanic, setup_app
from data import Secret


app = TypedSanic("app")


setup_app(app)

app.run(**Secret["sanic"])
