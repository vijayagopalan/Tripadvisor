from state.state import TravelState
from langchain_core.messages import (
    AIMessage,
    SystemMessage,
    HumanMessage
)
from tools.tavily_tool import tavily_search, tavily_airport_search
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
)



def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = tavily_airport_search(query)

    return {
        "flight_results":str(flight_data) ,
        "messages": [
           AIMessage(content = "flight results fetched") 
        ]
    }

def hotel_agent(state: TravelState):
    query = f"Best Hotels for {state["user_query"]}"
    hotel_results = tavily_search(search_query=query)
    return{
        "hotel_results":hotel_results,
        "messages": [
           AIMessage(content = "hotel results fetched") 
        ]
    }

def itinerary_agent(state: TravelState):
    prompt = f"""
    Create a complete travel itinerary.
    User Query:
    {state['user_query']}
    Flight Results:
    {state['flight_results']}
    Hotel Results:
    {state['hotel_results']}
    Make the itinerary practical, budget-aware, and easy to follow.
    """

    response = llm.invoke([
        SystemMessage(content="You are an expert travel planner."),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response]
    }

def final_agent(state: TravelState):
    final_prompt = f"""
        Generate the final travel response for the user.

        User Request:
        {state['user_query']}

        Flights:
        {state['flight_results']}

        Hotels:
        {state['hotel_results']}

        Itinerary:
        {state['itinerary']}

        Format the final answer beautifully using these sections:

        1. Trip Summary
        2. Flight Information
        3. Hotel Suggestions
        4. Day-by-Day Itinerary
        5. Estimated Budget
        6. Final Recommendations

        Important:
        - Be clear and practical.
        - Mention that live flight API may not provide ticket prices if pricing is unavailable.
        - Keep the response useful for real travel planning.
        """

    response = llm.invoke([
        SystemMessage(content="You are a professional AI travel booking assistant."),
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response]
    }

graph = StateGraph(TravelState)

graph.add_node("flight_agent",flight_agent)
graph.add_node("hotel_agent",hotel_agent)
graph.add_node("itinerary_agent",itinerary_agent)
graph.add_node("final_agent",final_agent)


graph.add_edge(START,"flight_agent")
graph.add_edge("flight_agent","hotel_agent")
graph.add_edge("hotel_agent","itinerary_agent")
graph.add_edge("itinerary_agent","final_agent")
graph.add_edge("final_agent",END)

travel_graph= graph.compile()


def travel_agent(user_input:str,thread_id: str | None = None):
    config={
        "configurable":{
            "thread_id": thread_id
        }
    }

    result = travel_graph.invoke(
        {
        "messages":[
            HumanMessage(content=user_input)
        ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
        },
        config=config
    )

    final_answer = result["messages"][-1].content
    
    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "itinerary": result.get("itinerary", ""),
        "llm_calls": result.get("llm_calls", 0),
    }