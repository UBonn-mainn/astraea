# Planner
import re
from tools.math_tool import math_tool
from tools.web_search_tool import web_search_tool
from tools.tinyllama_tool import tinyllama_tool

def decide_tool(query):
    if re.search(r"\d[\d\s\*\+\-/\.]+\d", query):
        return "calculator"
    elif any(x in query.lower() for x in ["current", "latest", "now", "today", "news", "weather", "stock"]):
        return "web"
    else:
        return "tinyllama"


# Agent loop
def agentic_chatbot(query):
    tool = decide_tool(query)
    # tool = llm_decide_tool(query)
    
    if tool == "calculator":
        response, confidence = math_tool.run(query)
    elif tool == "web":
        response, confidence = web_search_tool(query)
    elif tool == "tinyllama":
        response, confidence = tinyllama_tool(query)
    else:
        return "I don't know."

    if confidence < 0.5:
        return "I don't know."
    return response