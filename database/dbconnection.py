import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from psycopg_pool import AsyncConnectionPool

pool: AsyncConnectionPool | None = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global pool
    db_url = os.getenv("DB_URL")
    if not db_url:
        raise RuntimeError("DB_URL environment variable is not set")

    # Only create ONE pool, and let `async with` open and close it
    async with AsyncConnectionPool(conninfo=db_url) as p:
        pool = p
        yield