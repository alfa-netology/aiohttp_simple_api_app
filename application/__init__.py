from aiohttp import web
from aiohttp_apispec import setup_aiohttp_apispec
from gino import Gino

PG_DSN = f'postgres://alfa:prime@127.0.0.1:5432/aiohttp'

app = web.Application()
routes = web.RouteTableDef()
db = Gino()

from application.contexts import orm_context
app.cleanup_ctx.append(orm_context)

import application.routes

setup_aiohttp_apispec(app, title='Application', url='/docs/json', swagger_path='/docs')

