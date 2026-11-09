import sys
from dotenv import load_dotenv
load_dotenv()
import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from database.dbconnection import lifespan
from flightsapi.flights_api import router as flights_router
from pydantic import BaseModel
from agents.agents import travel_agent
from database.dbqueries import create_transaction

app = FastAPI(lifespan=lifespan)

class Travel_Request(BaseModel):
    message : str
    thread_id : str | None = None


app.include_router(flights_router)


@app.get("/")
async def healthz():
    return "healthy upstream"


@app.post("/api/travel")
async def travel_planner(request: Request,request_data:Travel_Request):
    try:
        user_message = request_data.message.strip()
        pool = getattr(request.app.state, "pool", None)
        if pool is not None:
            await create_transaction(pool, user_message, "HUMAN")
        result = travel_agent(
            user_input=user_message,
            thread_id=request_data.thread_id
        )
        if pool is not None:
            await create_transaction(pool, result["answer"], "AGENT")
        return JSONResponse(
            content={
                "success": True,
                "thread_id": result["thread_id"],
                "answer": result["answer"],
                "flight_results": result["flight_results"],
                "hotel_results": result["hotel_results"],
                "itinerary": result["itinerary"],
                "llm_calls": result["llm_calls"],
            }
        )
    except Exception as e:
        print("Error ", e)



if __name__ == "__main__":
    loop_setting = "asyncio:SelectorEventLoop" if sys.platform == "win32" else "auto"
    uvicorn.run(app=app, host="0.0.0.0", port=8080, loop=loop_setting)