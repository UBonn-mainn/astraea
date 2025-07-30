from langchain.tools import Tool
import math
import re

import math

def math_tool(expression: str):
    """
    Evaluate a math expression safely and return the result.

    Supported:
    - Basic arithmetic: +, -, *, /
    - Functions: sqrt, log, sin, cos, etc. (from math module)
    """
    try:
        # Define a safe environment
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        
        # Optional: add custom functions/constants
        allowed_names["abs"] = abs
        allowed_names["pow"] = pow

        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return round(result, 5), None
    except Exception as e:
        return f"Error evaluating expression: {e}", None