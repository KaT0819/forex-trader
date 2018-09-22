import typing as t

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/")
async def health_check(request: web.Request) -> web.Response:
    return web.Response(text="OK")
