import sys
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request
import uvicorn
from database.dbconnection import lifespan
from database.dbqueries import fetch_table_data
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(lifespan=lifespan)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)

@app.get("/")
async def healthz():
    return "healthy upstream"


@app.get("/getdata")
async def get_sample_table(request: Request):
    pool = request.app.state.pool
    result = await fetch_table_data(pool, table_name="Sample")
    return result

if __name__ == "__main__":
    loop_setting = "asyncio:SelectorEventLoop" if sys.platform == "win32" else "auto"
    uvicorn.run(app=app, host="0.0.0.0", port=8080, loop=loop_setting)