from src.agent.graph import State, graph
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(
    title="API for openwebui-pipelines",
    description="API for openwebui-pipelines",
)


class Query(BaseModel):
    messages: str


@app.post("/generate")
async def generate_text(query: Query):
    response: Dict = graph.invoke(State(messages=[query.messages], city=""))
    return {"generated_text": response['messages'][-1]}
