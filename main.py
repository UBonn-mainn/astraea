# main.py

# from agent.loop import run_agent
# from tools.registry import load_all_tools
# from agent.memory import create_memory
# from modules.subgoals import SubgoalTracker

from agent.loop import agentic_chatbot

if __name__ == "__main__":
    while True:
        query = input("User: ")
        if query.lower() in ["exit", "quit"]: break
        print("Agent:", agentic_chatbot(query))
