# modules/ranking.py

from typing import List
from tools.tinyllama_tool import tinyllama_tool

def build_ranking_prompt(prompt: str, responses: List[str]) -> str:
    """Format ranking prompt with fixed Option letters."""
    options = ""
    for i, resp in enumerate(responses):
        label = chr(65 + i)  # A, B, C, ...
        options += f"Option {label}: {resp.strip()}\n"

    return f"""You are a helpful judge. Rank the following answers based on helpfulness, correctness, and completeness.

Question: {prompt}

{options}

Please reply with only the best option letter (e.g., 'A').
"""

def rank_responses(prompt: str, responses: List[str]) -> str:
    """Uses TinyLLaMA to select the best response letter, maps to corresponding string."""
    label_map = {chr(65 + i): resp for i, resp in enumerate(responses)}  # {'A': ..., 'B': ..., ...}
    
    judge_prompt = build_ranking_prompt(prompt, responses)
    result, _ = tinyllama_tool(judge_prompt)
    result = result.strip().upper()

    # Debug output (optional)
    print(f"[Judge LLM returned]: {result}")

    for char in result:
        if char in label_map:
            return label_map[char]

    return responses[0]  # Fallback
