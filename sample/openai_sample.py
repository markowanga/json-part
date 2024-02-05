"""
That's the mos simple example, without additional dependencies.
"""
from typing import Optional

from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk

from json_part import parse_incomplete_json

FUNCTION = {
    "name": "item_invention_details",
    "description": "Info about invention",
    "parameters": {
        "type": "object",
        "properties": {
            "year": {"type": "number", "description": "Nationality of person"},
            "inventor": {"type": "string", "description": "Full name of inventor"},
            "keywords": {
                "type": "array",
                "items": {"type": "string"},
            },
            "description": {
                "type": "string",
                "description": "How it was invented",
            },
        },
        "required": ["year", "inventor", "keywords", "description"],
    },
}


def get_openai_stream_generator() -> Stream[ChatCompletionChunk]:
    client = OpenAI()
    messages = [
        {"role": "system", "content": "Return details about invention"},
        {"role": "user", "content": "car"},
    ]
    response: Stream[ChatCompletionChunk] = client.chat.completions.create(
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


def openai_sample() -> None:
    response = get_openai_stream_generator()
    previous_value = None
    json_accumulator = ""
    for it in response:
        delta = get_delta_argument(it) or ""
        json_accumulator += delta
        new_value = parse_incomplete_json(json_accumulator)
        if new_value != previous_value:
            print(new_value)
            previous_value = new_value


if __name__ == "__main__":
    openai_sample()
