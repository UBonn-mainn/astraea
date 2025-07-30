


import re

from tools.web_search_tool import web_search_tool
from tools.tinyllama_tool import tinyllama_tool  # your local LLM wrapper
from tools.image_tool import ImageAnalyzer
from tools.math_tool import  math_tool

TOOLS = {
    "Web": web_search_tool,
    "Calculator": math_tool,  
}


# Prompt templates
SYSTEM_PROMPT = """You are a helpful assistant that reasons and acts in a step-by-step way.
Only perform one step of reasoning unless multiple steps are clearly required.
Do not invent extra steps or questions beyond what the user asked.
YOU are only soving one question one at a time.
You use this format:
Thought: reason about the task
Action: tool_name[parameter=value, ...]
Observation: 
...

Final Answer: your final conclusion

Available tools:
- Calculator[expression: str] → Use this for math expressions (e.g., "2 + 3", "sqrt(144)")
- Web[city: str] → Use this to look up current weather information
"""

EXAMPLES = """
Example 1:
Question: What is 12*12?
Thought: I need to calculate 12 times 12.
Action: Calculator[expression=12*12]

---

"""



def parse_action(line):
    match = re.match(r"Action:\s*(\w+)\[(.*)\]", line)
    if not match:
        return None, None
    tool_name, args_str = match.groups()
    args = {}
    for pair in args_str.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            args[k.strip()] = v.strip().strip('"')
    return tool_name, args

 

def agentic_chatbot(question):
    history = f"{EXAMPLES}\nQuestion: {question}\n"
    full_prompt = f"{SYSTEM_PROMPT}\n\n{history}"

    while True:
        # reponse
        response, _ = tinyllama_tool(full_prompt)
        print("MODEL RESPONSE:\n", response)

        # add to history
        history += response + "\n"
        full_prompt = f"{SYSTEM_PROMPT}\n\n{history}"

        # 如果包含 Final Answer，直接退出
        if "Final Answer:" in response:
            print("Model returned Final Answer, stopping.")
            break

        # tools
        action_found = False
        for line in response.split("\n"):
            line = line.strip()
            if line.startswith("Action:"):
                print("DEBUG: original line =", line)
                tool_name, args = parse_action(line)
                print("Parsed tool_name:", tool_name, "args:", args)
                if not tool_name:
                    observation = "Observation: Failed to parse action line."
                elif tool_name not in TOOLS:
                    observation = f"Observation: Error: Unknown tool {tool_name}"
                else:
                    tool_output = TOOLS[tool_name](**args)
                    result = tool_output[0] if isinstance(tool_output, tuple) else tool_output
                    print("Tool used:", tool_name, "with args", args, "→ result:", result)
                    observation = f"Observation: {result}"


                # add Observation 
                history += observation + "\n"
                full_prompt = f"{SYSTEM_PROMPT}\n\n{history}"
                print("MODEL RESPONSE:\n", history)
                action_found = True
                break  

        if not action_found:
            print("No tool action found and no final answer; stopping.")
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



