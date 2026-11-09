from psycopg_pool import AsyncConnectionPool

async def fetch_table_data(pool: AsyncConnectionPool, table_name: str):
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f'SELECT * FROM "{table_name}";')
            rows = await cur.fetchall()
            columns = [desc[0] for desc in cur.description] if cur.description else []
            return {"columns": columns, "data": rows}