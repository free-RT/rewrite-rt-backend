from sanic import Sanic
from inspect import getmembers


def route(*args, **kwargs):
    def decorator(coro):
        coro._route = (args, kwargs)
        return coro
    return decorator


class Cog:
    """discord.pyのcogみたいにroute登録できます。
    Example:
        from core import Cog, route
        from sanic import response
        
        class cog(Cog):
            def __init__(self, app):
                self.app = app
                
            @route("/")
            async def main(request):
                return response.text("hello, world")"""
    def _inject(self, app: Sanic):
        for name, func in getmembers(self):
            if hasattr(func, "_route"):
                args, kwargs = func._route
                app.add_route(func, **args, **kwargs)
