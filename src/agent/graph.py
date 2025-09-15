"""Simple agent graph example using LangGraph Prebuilt components.
"""

from __future__ import annotations

from langgraph.prebuilt import create_react_agent

# Tool for Agent
def get_weather(city: str) -> str:  
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

# Create Agent
agent = create_react_agent(
    model="ollama:llama3.2",  
    tools=[get_weather],  
    prompt="You are a helpful assistant"  
)

# Define the graph
graph = (
    agent
)
