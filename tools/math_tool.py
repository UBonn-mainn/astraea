from langchain.tools import Tool
import math

def calculator(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": {}}, math.__dict__)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"

math_tool = Tool(
    name="Calculator",
    func=calculator,
    description="Evaluates a math expression."
)