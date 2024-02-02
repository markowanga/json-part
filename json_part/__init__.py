from typing import Any

from json_part.parser import JsonPartParser


def parse_incomplete_json(string_input: str) -> Any:
    return JsonPartParser().parse(string_input)
