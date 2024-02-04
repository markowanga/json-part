import json
from typing import Any

from json_part.json_part_parser import JsonPartParser


def parse_incomplete_json(string_input: str) -> Any:
    return JsonPartParser().parse(string_input)


def fix_incomplete_json(string_input: str) -> Any:
    return json.dumps(parse_incomplete_json(string_input))
