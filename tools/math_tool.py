from langchain.tools import Tool
import math
import re

def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, math.__dict__)
        return str(result), 1.0
    except Exception as e:
        return f"Calculation error: {str(e)}", 0.0

math_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Evaluates a math expression."
)