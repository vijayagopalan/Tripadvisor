import psycopg
from psycopg_pool import AsyncConnectionPool

async def fetch_transaction_data(pool: AsyncConnectionPool, table_name: str):
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f'SELECT * FROM "Transaction";')
            rows = await cur.fetchall()
            return {"data": rows}
        
async def create_transaction(pool: AsyncConnectionPool, message: str, type: str):
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    'INSERT INTO "Transaction" (trans_message, trans_type) VALUES (%s, %s)',
                    (message, type),
                )
        return {"message": "row added successfully"}
    except psycopg.Error as error:
        return {"message": "failed to add row", "error": str(error)}