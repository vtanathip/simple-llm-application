from src.agent.graph import graph

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="API for openwebui-pipelines",
    description="API for openwebui-pipelines",
)


class Query(BaseModel):
    prompt: str
    model: str = "llama3.2"


class Conversation(BaseModel):
    id: str
    messages: List[Dict[str, str]] = []


conversations: Dict[str, Conversation] = {}


@app.post("/generate")
async def generate_text(query: Query):
    response: Dict = graph.invoke(query)
    return {"generated_text": response['messages'][-1]}
