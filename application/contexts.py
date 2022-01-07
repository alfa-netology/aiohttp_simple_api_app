from application import PG_DSN
from application import db

async def orm_context(app):
    await db.set_bind(PG_DSN)
    print('orm created')
    yield
    await db.pop_bind().close()
