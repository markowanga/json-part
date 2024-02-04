from pathlib import Path
from typing import AsyncGenerator, Any, Optional, Dict

from fastapi import FastAPI
from pydantic import BaseModel
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import HTMLResponse

from json_part import parse_incomplete_json
from openai_sample import get_openai_stream_agenerator

app = FastAPI()


class DescriptionEvent(BaseModel):
    is_finish: bool
    value: Optional[Any]


async def get_response_generator() -> AsyncGenerator[ServerSentEvent, None]:
    accumulator = ""
    previous_json = None
    async for it in await get_openai_stream_agenerator():
        if it.choices[0].delta.tool_calls:
            accumulator += it.choices[0].delta.tool_calls[0].function.arguments
            json = parse_incomplete_json(accumulator)
            if previous_json != json:
                previous_json = json
                yield ServerSentEvent(DescriptionEvent(is_finish=False, value=json).json())
        else:
            yield ServerSentEvent(DescriptionEvent(is_finish=True, value=None).json())


@app.get('/stream')
async def message_stream():
    return EventSourceResponse(get_response_generator())


@app.get("/", response_class=HTMLResponse)
async def read_items():
    return Path("index.html").read_text()
