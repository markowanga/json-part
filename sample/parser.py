from pathlib import Path
from typing import AsyncGenerator, Any

from fastapi import FastAPI
from sse_starlette import EventSourceResponse
from starlette.responses import HTMLResponse

from json_part import fix_incomplete_json
from openai_sample import get_openai_stream_agenerator

app = FastAPI()


async def get_response_generator() -> AsyncGenerator[str, None]:
    accumulator = ""
    previous_json = None
    async for it in await get_openai_stream_agenerator():
        if it.choices[0].delta.tool_calls:
            accumulator += it.choices[0].delta.tool_calls[0].function.arguments
            json = fix_incomplete_json(accumulator)
            if previous_json != json:
                previous_json = json
                yield json
        else:
            break
    print('finish get_response_generator')


@app.get('/stream')
async def message_stream():
    return EventSourceResponse(get_response_generator())


@app.get("/", response_class=HTMLResponse)
async def read_items():
    return Path("index.html").read_text()
