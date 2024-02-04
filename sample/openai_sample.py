"""
That's the mos simple example, without additional dependencies.
"""

from openai import OpenAI, Stream, AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk

from json_part import parse_incomplete_json

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


def get_openai_stream_generator() -> Stream[ChatCompletionChunk]:
    client = OpenAI()
    messages = [
        {"role": "system", "content": "Return details about asking person"},
        {"role": "user", "content": "Iga Świątek"},
    ]
    return client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=[{"type": "function", "function": FUNCTION}],
        tool_choice="auto",
        stream=True,
    )  # type: ignore


async def get_openai_stream_agenerator() -> AsyncStream[ChatCompletionChunk]:
    client = AsyncOpenAI()
    messages = [
        {"role": "system", "content": "Return details about asking person"},
        {"role": "user", "content": "Iga Świątek"},
    ]
    return await client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=[{"type": "function", "function": FUNCTION}],
        tool_choice="auto",
        stream=True,
    )  # type: ignore


def openai_sample() -> None:
    response = get_openai_stream_generator()
    json_accumulator = ""
    for it in response:
        if it.choices[0].delta.tool_calls:
            json_accumulator += it.choices[0].delta.tool_calls[0].function.arguments
            print(parse_incomplete_json(json_accumulator))


if __name__ == "__main__":
    openai_sample()
