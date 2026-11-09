from fastapi import APIRouter, Request

from database.dbqueries import fetch_table_data

router = APIRouter()


@router.get("/getsampledata")
async def get_sample_table(request: Request):
    pool = request.app.state.pool
    result = await fetch_table_data(pool, table_name="Sample")
    return result

@router.get("/getflight")
async def get_flights(request: Request):
    pool = request.app.state.pool
    result = await fetch_table_data(pool, table_name="Sample")
    return result