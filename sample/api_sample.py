from pathlib import Path
from typing import Any, AsyncGenerator, Optional

from fastapi import FastAPI
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk
from openai_sample import FUNCTION
from pydantic import BaseModel
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import HTMLResponse

from json_part import parse_incomplete_json

app = FastAPI()


class DescriptionEvent(BaseModel):
    is_finish: bool
    value: Optional[Any]


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


async def get_response_generator() -> AsyncGenerator[ServerSentEvent, None]:
    accumulator = ""
    previous_json = None
    async for it in await get_openai_stream_agenerator():
        if it.choices[0].delta.tool_calls:
            function = it.choices[0].delta.tool_calls[0].function
            assert function is not None
            accumulator += function.arguments or ""
            json = parse_incomplete_json(accumulator)
            if previous_json != json:
                previous_json = json
                yield ServerSentEvent(
                    DescriptionEvent(is_finish=False, value=json).json()
                )
        else:
            yield ServerSentEvent(DescriptionEvent(is_finish=True, value=None).json())


@app.get("/stream")
async def message_stream() -> EventSourceResponse:
    return EventSourceResponse(get_response_generator())


@app.get("/", response_class=HTMLResponse)
async def read_items() -> str:
    return Path("index.html").read_text()
