import requests
import os
from typing import List, Union, Generator, Iterator, Optional
from pydantic import BaseModel, Field


class Pipeline:
    class Valves(BaseModel):
        API_URL: Optional[str] = Field(
            default="http://host.docker.internal:8000/generate",
            description="Langgraph API URL"
        )

    def __init__(self):
        self.id = "LangGraph Agent"
        self.name = "LangGraph Agent"
        # Initialize valve paramaters
        self.valves = self.Valves(
            **{k: os.getenv(k, v.default) for k, v in self.Valves.model_fields.items()}
        )

    async def on_startup(self):
        print(f"on_startup: {__name__}")
        pass

    async def on_shutdown(self):
        print(f"on_shutdown: {__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:

        last_user_message = messages[-1]["content"]
        url = self.valves.API_URL
        if not url:
            raise ValueError(
                "API_URL is not configured. Please set it in the pipeline settings.")

        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            "messages": last_user_message
        }

        response = requests.post(url, json=data, headers=headers, stream=True)
        for line in response.iter_lines():
            if line:
                yield line.decode() + '\n'
