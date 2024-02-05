from pathlib import Path
from typing import Any, AsyncGenerator, Optional

from fastapi import FastAPI
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk
from pydantic import BaseModel
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import HTMLResponse

from json_part import parse_incomplete_json

app = FastAPI()

FUNCTION = {
    "name": "person_details",
    "description": "Get the details about person, additional_info: please return fields in original order",
    "parameters": {
        "type": "object",
        "properties": {
            "nationality": {"type": "string", "description": "Nationality of person"},
            "year_born": {"type": "number"},
            "year_die": {"type": "number", "description": "Year of die or null"},
            "important_keywords": {
                "type": "array",
                "items": {"type": "string"},
            },
            "short_bio": {"type": "string", "description": "Short bio"},
            "description": {
                "type": "string",
                "description": "Person description",
            },
        },
        "required": [
            "nationality",
            "year_born",
            "year_die",
            "important_keywords",
            "short_bio",
            "description",
        ],
    },
}


class DescriptionEvent(BaseModel):
    is_finish: bool
    value: Optional[Any]

    def to_sse(self) -> ServerSentEvent:
        return ServerSentEvent(self.json())


async def get_openai_stream_agenerator() -> AsyncStream[ChatCompletionChunk]:
    client = AsyncOpenAI()
    messages = [
        {"role": "system", "content": "Return details about asking person"},
        {"role": "user", "content": "Iga Świątek"},
    ]
    response: AsyncStream[ChatCompletionChunk] = await client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=[{"type": "function", "function": FUNCTION}],
        tool_choice="auto",
        stream=True,
    )  # type: ignore
    return response


def get_delta_argument(chunk: ChatCompletionChunk) -> Optional[str]:
    if chunk.choices[0].delta.tool_calls:
        function = chunk.choices[0].delta.tool_calls[0].function
        assert function is not None
        return function.arguments
    else:
        return None


async def get_response_generator() -> AsyncGenerator[ServerSentEvent, None]:
    accumulator = ""
    previous_json = None
    async for it in await get_openai_stream_agenerator():
        # print(it)
        delta = get_delta_argument(it)
        # print(delta)
        if delta is not None:
            accumulator += delta
            json = parse_incomplete_json(accumulator)
            if previous_json != json:
                previous_json = json
                yield DescriptionEvent(is_finish=False, value=json).to_sse()
        else:
            yield DescriptionEvent(is_finish=True, value=None).to_sse()
        # yield DescriptionEvent(is_finish=False, value="json").to_sse()


@app.get("/", response_class=HTMLResponse)
async def read_items() -> str:
    return Path("index.html").read_text()


@app.get("/stream")
async def message_stream() -> EventSourceResponse:
    return EventSourceResponse(get_response_generator())
