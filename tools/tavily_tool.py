from tavily import TavilyClient
from dotenv import load_dotenv
load_dotenv()
import os


tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def tavily_search(search_query):
    response = tavily_client.search(search_query,max_results=5)
    results = []
    for i, r in enumerate(response["results"],1):
        title = r.get("title","unknown")
        url = r.get("url","")
        content = r.get("content","").strip()
        if len(content) > 300:
            content = content[:300] + "..."
        results.append(f"{i}. **{title}**\n{url}\n{content}")
    return results

def tavily_airport_search(search_query):
    response = tavily_client.search(search_query,max_results=5)
    results = []
    for i, r in enumerate(response["results"],1):
        title = r.get("title","unknown")
        url = r.get("url","")
        content = r.get("content","").strip()
        if len(content) > 300:
            content = content[:300] + "..."
        results.append(f"{i}. **{title}**\n{url}\n{content}")
    return results

