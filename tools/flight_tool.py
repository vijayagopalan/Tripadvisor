import os
from tavily import TavilyClient
from dotenv import load_dotenv
from typing import TypedDict, Annotated
import operator
from llm import llm
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage
import requests
load_dotenv()


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

access_key = os.getenv("AVIATION_STACK_API_KEY")

class FlightState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

@tool
def get_weather(departure:str,destination:str)->dict:
    """Get the weather information about the departure location and destination location"""
    return {
        "departure" : tavily_client.search(f"weather in ${departure} city"),
        "destination" : tavily_client.search(f"weather in ${destination} city")
    }

@tool
def get_IATA_code(departure:str,destination:str):
    """Get the iata code information about the departure location and destination location"""
    return {
        "departure" : tavily_client.search(f"iata code for ${departure} city"),
        "destination" : tavily_client.search(f"iata code for ${destination} city")
    }


@tool
def get_location(departure:str,destination:str):
    """identify the depature and destination location from user query"""
    return {
            "departure" :departure,
            "destination" :destination
        }

@tool
def get_flights_data(dep_iata:str,arr_iata:str):
    """Get the available flights for the trip using iata code of the location of departure and arraival 
   """

    url = "https://api.apilayer.net/aviationstack/v1/flights"
    if not access_key:
        raise RuntimeError("AVIATION_STACK_API_KEY is not configured.")

    params = {
        "access_key": access_key,
        "limit": "100",
        "offset": "0",
        "dep_iata": dep_iata,
        "arr_iata": arr_iata
    }

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data["data"]


tools = [get_weather,get_IATA_code,get_flights_data,get_location]


llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

def call_model(state: FlightState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: FlightState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"

workflow = StateGraph(FlightState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"tools": "tools", "end": END}
)
workflow.add_edge("tools", "agent")

flightapp = workflow.compile()