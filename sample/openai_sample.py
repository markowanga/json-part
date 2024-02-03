from openai import OpenAI

from json_part import parse_incomplete_json


def openai_sample():
    client = OpenAI()
    messages = [{"role": "system", "content": "Return details about asking person"},
                {"role": "user", "content": "Iga Świątek"}]
    function = {
        "name": "person_details",
        "description": "Get the details about person",
        "parameters": {
            "type": "object",
            "properties": {
                "nationality": {
                    "type": "string",
                    "description": "Nationality of person"
                },
                "year_born": {
                    "type": "number"
                },
                "year_die": {
                    "type": "number",
                    "description": "Year of die or null"
                },
                "important_keywords": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                },
                "short_bio": {
                    "type": "string",
                    "description": "Short bio"
                },
                "description": {
                    "type": "string",
                    "description": "Large person description and bio"
                }
            },
            "required": [
                "nationality",
                "year_born",
                "year_die",
                "important_keywords",
                "short_bio",
                "description"
            ]
        }
    }

    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=messages,
        tools=[{"type": "function", "function": function}],
        tool_choice="auto",
        stream=True
    )
    json_accumulator = ""
    for it in response:
        if it.choices[0].delta.tool_calls:
            json_accumulator += it.choices[0].delta.tool_calls[0].function.arguments
            print(parse_incomplete_json(json_accumulator))


if __name__ == '__main__':
    openai_sample()
