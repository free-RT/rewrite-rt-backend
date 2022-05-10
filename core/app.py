# FreeRT - app.py
from sanic import Sanic, response, Request
from sanic.exceptions import SanicException

from sanic_mysql import ExtendMySQL
from orjson import dumps, loads
from miko.manager import Manager

from data import Secret

from typing import Union

from os.path import exists
from sys import argv

PATH = template_folder = "rt-frontend"
class TypedSanic(Sanic):
    pass


def l(tag: str="div", extends: str="", class_: str="", **kwargs) -> str:
    "複数言語対応用"
    return "".join(
        f'<{tag} class="language {key} {class_}" {extends} hidden>{value}</{tag}>'
        for key, value in kwargs.items()
    )

def cl(text: Union[str, dict[str, str]]) -> str:
    "渡されたやつが辞書ならlに渡す。"
    return l(**text) if isinstance(text, dict) else text

def layout(title: str, description: str, content: str, head: str=""):
    "一般のHTMLをレンダリングする関数です。"
    title = cl(title)
    description = cl(description)
    content = cl(content)
    return gapp.ctx.env.render(
        f"{template_folder}/layout.html", content=content,
        head=f"""<title>{title}</title>
        <meta name="description" content="{description}">
        {head}""", _=l
    )


def setup_app(app: TypedSanic):
    global gapp
    app.ctx.mysql = ExtendMySQL(app, **Secret["mysql"])
    app.ctx.env = app.ctx.miko = Manager(
        extends={
            "layout": layout,
            "app": app,
            "loads": loads,
            "dumps": dumps,
            "l": l
        }
    )
    gapp = app
    async def _template(path: str, **kwargs):
        kwargs["app"] = app
        return response.html(await app.ctx.miko.aiorender("{}{}".format(PATH, path), **kwargs))
    app.ctx.template = app.ctx.render = _template
    app.ctx.canary = argv[1] == "canary"
    
    @app.on_request
    async def response_content(request: Request):
        if (request.server_name == "localhost"
            or request.server_name == "free-rt.com"):
            if request.path == "/":
                return await app.ctx.template("/index.html", eloop=app.loop, _=l)
            if exists(f"{PATH}{request.path}"):
                if request.path.endswith(".html"):
                    return await app.ctx.template(request.path, eloop=app.loop, _=l)
                else:
                    return await response.file(f"{PATH}{request.path}")
            else:
                raise SanicException("あれ？ここどこだ？真っ白な壁がずっと続いているよ", status_code=404)
