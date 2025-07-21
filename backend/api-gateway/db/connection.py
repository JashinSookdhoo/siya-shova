import os
import asyncpg

db_pool = None

async def connect_to_db():
    global db_pool
    db_pool = await asyncpg.create_pool(dsn=os.environ["DATABASE_URL"])

async def disconnect_from_db():
    global db_pool
    if db_pool:
        await db_pool.close()