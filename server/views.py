import typing as t

from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/traders/")
async def traders(request: web.Request) -> web.Response:
    return web.Response(text="OK")
