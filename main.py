import sys
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import uvicorn
from database.dbconnection import lifespan
from flightsapi.flights_api import router as flights_router
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(lifespan=lifespan)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

app.include_router(flights_router)


@app.get("/")
async def healthz():
    return "healthy upstream"

if __name__ == "__main__":
    loop_setting = "asyncio:SelectorEventLoop" if sys.platform == "win32" else "auto"
    uvicorn.run(app=app, host="0.0.0.0", port=8080, loop=loop_setting)