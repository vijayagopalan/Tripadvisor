from fastapi import APIRouter, Request

from database.dbqueries import fetch_transaction_data, create_transaction

router = APIRouter()


@router.get("/gettransactiondata")
async def get_sample_table(request: Request):
    pool = request.app.state.pool
    result = await fetch_transaction_data(pool)
    return result

@router.get("/createtransaction")
async def get_flights(request: Request):
    pool = request.app.state.pool
    message = request.body.message
    type =  request.body.type
    result = await create_transaction(pool,message,type)
    return result