# Planner
import re


import re
from tools.math_tool import math_tool
from tools.web_search_tool import web_search_tool
from tools.tinyllama_tool import tinyllama_tool  # your local LLM wrapper
from tools.image_tool import ImageAnalyzer
import json
import uuid

TOOLS = {
    "calculator": math_tool,
    "web": web_search_tool,
    "image_gen": ImageAnalyzer, 
}

# Prompt templates
SYSTEM_PROMPT = """You are a helpful agent. You can use these tools:

- calculator[expression=...] → for math
- web[query=...] → for current facts
- image_gen[prompt=...] → to generate an image from a text description

Use this pattern when needed:
Action: tool_name[key=value]
Wait for an Observation before continuing. End with:
Final Answer: your final response.
"""
EXAMPLES = """Question: What is 5 * 7?
Thought: I need a tool for math calculations.
Action: calculator[expression=5*7]
Observation: 35
Final Answer: 5 times 7 is 35.

Question: What's the current weather in Paris?
Thought: I need to look up the weather online.
Action: web[query=weather in Paris]
Observation: It's currently 23°C in Paris.
Final Answer: The current weather in Paris is 23°C.

Question: Can you show me a fantasy landscape with a purple sky and floating islands?
Thought: I need to generate an image based on that description.
Action: image_gen[prompt=fantasy landscape with a purple sky and floating islands]
Observation: [Image generated successfully]
Final Answer: Here's a fantasy landscape with a purple sky and floating islands.
"""

# Parses lines like: Action: calculator[expression=1+1]
def parse_action(line):
    match = re.match(r"Action:\s*(\w+)\[(.*)\]", line)
    if not match:
        return None, None
    tool_name, args_str = match.groups()
    args = {}
    for pair in args_str.split(','):
        if '=' in pair:
            k, v = pair.split('=')
            args[k.strip()] = v.strip()
    return tool_name, args

def agentic_chatbot(question):
    history = f"{EXAMPLES}\nQuestion: {question}\n"
    full_prompt = f"{SYSTEM_PROMPT}\n\n{history}"
    
    while True:
        # LLM thinks
        response, _ = tinyllama_tool(full_prompt)
        print("🧠 Assistant:\n" + response + "\n")

        history += response + "\n"
        
        if "Final Answer:" in response:
            break
        
        # Look for tool call
        for line in response.split("\n"):
            if line.startswith("Action:"):
                tool_name, args = parse_action(line)
                if tool_name not in TOOLS:
                    observation = f"Observation: Error: Unknown tool '{tool_name}'"
                else:
                    try:
                        result, _ = TOOLS[tool_name](**args)
                        observation = f"Observation: {result}"
                    except Exception as e:
                        observation = f"Observation: Tool error: {e}"
                
                # Add observation and let LLM continue reasoning
                history += observation + "\n"
                full_prompt = f"{SYSTEM_PROMPT}\n\n{history}"
                break



def generate_subgoals(query):
   prompt = f"""
     You are a subgoal planner. Break down the task below into 1-5 subgoals, returning **ONLY** a valid JSON list with NO explanation or other text.

     Use this exact format:

     [
      {{"id": 1, "text": "subgoal text", "tool": "tool_name", "status": "pending"}},
     ...
     ]

     Available tools: calculator, web, image, audio, zephyr.

     Task: {query}
     """

    
   response, confidence = tinyllama_tool(prompt)
   
   ##if confidence < 0.5:
        ##return []

   try:
        subgoals = eval(response)  # if the model outputs valid Python/JSON
        return subgoals
   except Exception:
        return []


def update_subgoal_status(subgoals, observation):
    context = "\n".join(f"{sg['id']}. {sg['text']} (status: {sg['status']})" for sg in subgoals)
    
    prompt = f"""
Given the following subgoals and a new tool observation, update any subgoal that is now completed.

Subgoals:
{context}

Tool Observation:
{observation}

Return the updated list in this format:
[{{"id": 1, "text": "...", "tool": "...", "status": "done"}}]
"""
    response, confidence = tinyllama_tool(prompt)
    print("📤 Subgoal Prompt Sent:")
   
    ##if confidence < 0.5:
        ##return subgoals

    try:
        updated = eval(response)
        return updated
    except Exception:
        return subgoals


def get_next_subgoal(subgoals):
    for sg in subgoals:
        if sg["status"] == "pending":
            return sg
    
    return None

def all_subgoals_done(subgoals):
    return all(sg["status"] == "done" for sg in subgoals)



