def web_search_tool(query):
    # Stub: Replace with real search API like SerpAPI or Tavily
    if "stock" in query.lower() or "weather" in query.lower():
        return f"[Web] Pretend result for '{query}'", 0.8
    return "", 0.0