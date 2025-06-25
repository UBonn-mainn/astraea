from tools.image_tool import image_tool
from tools.audio_tool import audio_tool
from tools.math_tool import math_tool

def load_all_tools():
    return [
        image_tool,
        audio_tool,
        math_tool,
    ]
