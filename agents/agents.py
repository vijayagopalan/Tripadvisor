from state.state import TravelState
from langchain_core.messages import (
    AIMessage,
)


def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = []

    return {
        "fligh_results":flight_data,
        "messages": [
           AIMessage(content = "flight results fetched") 
        ]
    }