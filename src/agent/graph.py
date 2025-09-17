"""Simple agent graph example using LangGraph Prebuilt components.
"""

from __future__ import annotations
from langchain import hub
from langgraph.prebuilt import create_react_agent
from langgraph.graph.message import add_messages
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

from dotenv import load_dotenv
from langchain_community.utilities import OpenWeatherMapAPIWrapper
from langchain_ollama import ChatOllama
from typing import Annotated
from typing_extensions import TypedDict


load_dotenv()
# Tool for Agent
weather = OpenWeatherMapAPIWrapper()
# Define LLM Model
llm = ChatOllama(model="llama3.2")


class State(TypedDict):
    messages: Annotated[list, add_messages]
    city: str


def agent(state):
    # Extract the latest user message
    user_input = state["messages"][-1].content

    res = llm.invoke(f"""
    You are given one question and you have to extract the city name from it.
    Respond ONLY with the city name. If you cannot find a city, respond with an empty string.

    Here is the question:
    {user_input}
    """)

    if isinstance(
            res.content, str):
        city_name = res.content.strip()

    if not city_name:
        return {"messages": [AIMessage(content="I couldn't find a city name in your question.")]}

    return {"messages": [AIMessage(content=f"Extracted city: {city_name}")], "city": city_name}


def weather_tool(state):
    city_name = state.get("city", "").strip()  # Retrieve city name from state

    if not city_name:
        return {"messages": [AIMessage(content="No city name provided. Cannot fetch weather.")]}

    weather_info = weather.run(city_name)
    return {"messages": [AIMessage(content=weather_info)]}


memory = MemorySaver()
workflow = StateGraph(State)

# **Define Transitions Between Nodes**
workflow.add_edge(START, "agent")
# **Add Nodes**
workflow.add_node("agent", agent)
workflow.add_node("weather", weather_tool)

# **Connect Nodes**
workflow.add_edge("agent", "weather")
workflow.add_edge("weather", END)

# **Compile Workflow with Memory Checkpointer**
app = workflow.compile()

# Define the graph
graph = (
    app
)
