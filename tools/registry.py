from tools.image_tool import image_tool
from tools.audio_tool import audio_tool
from tools.math_tool import math_tool
from tools.web_search_tool import web_search_tool
from tools.tinyllama_tool import tinyllama_tool

def load_all_tools():
    return [
        image_tool,
        audio_tool,
        math_tool,
        tinyllama_tool,  
        web_search_tool
    ]
    