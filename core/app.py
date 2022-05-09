from sanic import Sanic, response, Request
from sanic.exceptions import SanicException
from sanic_mysql import ExtendMySQL
from orjson import dumps, loads
from data import Secret
from miko.manager import Manager
from os.path import exists

PATH = "rt-frontend"
class TypedSanic(Sanic):
    pass


def l(tag="div", extends="", class_="", **kwargs) -> str:
    "複数言語対応用"
    return "".join(
        f'<{tag} class="language {key} {class_}" {extends} hidden>{value}</{tag}>'
        for key, value in kwargs.items()
    )

def cl(text: Union[str, dict[str, str]]) -> str:
    "渡されたやつが辞書ならlに渡す。"
    return l(**text) if isinstance(text, dict) else text

def layout(title, description, content, head=""):
    "一般のHTMLをレンダリングする関数です。"
    title = cl(title)
    description = cl(description)
    content = cl(content)
    return app.ctx.env.render(
        f"{template_folder}/layout.html", content=content,
        head=f"""<title>{title}</title>
        <meta name="description" content="{description}">
        {head}""", _=l
    )


def setup_app(app: TypedSanic):
    app.ctx.mysql = ExtendMySQL(app, **Secret["mysql"])
    app.ctx.miko = Manager(
        extends={
            "layout": layout,
            "app": app,
            "loads": loads,
            "dumps": dumps,
            "1": t
        }
    )
    
    async def _template(path: str, **kwargs):
        return response.html(await app.ctx.miko.aiorender("{}{}".format(PATH, path), **kwargs))
    app.ctx.template = _template
    
    @app.on_request
    async def response_content(request: Request):
        if (request.server_name == "localhost"
            or request.server_name == "free-rt.com"):
            if exists(f"{PATH}{request.path}"):
                return await app.ctx.template(request.path, eloop=app.loop, _=l)
            else:
                raise SanicException("あれ？ここどこだ？真っ白な壁がずっと続いているよ", status_code=404)
