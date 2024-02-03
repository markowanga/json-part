import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, TypeVar, Tuple, Optional

_T = TypeVar("_T")


@dataclass
class ParserResult:
    value: Any
    rest_of_string: str


class Parser(ABC):
    @abstractmethod
    def parse(self, str_input: str) -> ParserResult:
        pass


class ArrayParser(Parser):

    def parse(self, str_input: str) -> ParserResult:
        temp_str = str_input[1:]  # skip [
        result = []
        temp_str = temp_str.lstrip()
        while temp_str:
            if temp_str[0] == "]":
                temp_str = temp_str[1:].lstrip()  # skip ]
                break
            item_result = AnyParser().parse(temp_str)
            res = item_result.value
            temp_str = item_result.rest_of_string
            result.append(res)
            temp_str = temp_str.lstrip()
            if temp_str.startswith(","):
                temp_str = temp_str[1:].lstrip()
        return ParserResult(result, temp_str)


class ObjectParser(Parser):

    def parse(self, str_input: str) -> ParserResult:
        temp_str = str_input[1:]  # skip {
        result: Dict[str, Optional[Any]] = {}
        temp_str = temp_str.lstrip()
        while temp_str:
            if temp_str[0] == "}":
                temp_str = temp_str[1:]  # skip }
                break

            key, temp_str = self.key_parse(temp_str)

            if not temp_str:
                break

            temp_str = self.skip_colon(temp_str)

            # Handle case where value is missing or incomplete
            if not temp_str:
                result[key] = None
                break

            value, temp_str = self.value_parse(temp_str)

            result[key] = value
            temp_str = self.skip_possible_comma(temp_str.lstrip())
        return ParserResult(result, temp_str)

    @staticmethod
    def skip_colon(str_input: str) -> str:
        temp_str = str_input.lstrip()
        if temp_str[0] != ":":
            raise Exception("No ':' after key")
        temp_str = temp_str[1:]
        return temp_str.lstrip()

    @staticmethod
    def skip_possible_comma(str_input: str) -> str:
        if str_input.startswith(","):
            return str_input[1:].lstrip()
        else:
            return str_input

    @staticmethod
    def key_parse(str_input: str) -> Tuple[str, str]:
        key_parse_result = StringParser().parse(str_input)
        return key_parse_result.value, key_parse_result.rest_of_string.lstrip()

    @staticmethod
    def value_parse(str_input: str) -> Tuple[Any, str]:
        value_parse_result = AnyParser().parse(str_input)
        return value_parse_result.value, value_parse_result.rest_of_string.lstrip()


class StringParser(Parser):
    def parse(self, str_input: str) -> ParserResult:
        end = str_input.find('"', 1)
        while end != -1 and str_input[end - 1] == "\\":  # Handle escaped quotes
            end = str_input.find('"', end + 1)
        if end == -1:
            # Return the incomplete string without the opening quote
            return ParserResult(str_input[1:], "")
        str_val = str_input[: end + 1]
        s = str_input[end + 1:]
        return ParserResult(json.loads(str_val), s)


class TrueParser(Parser):

    def parse(self, str_input: str) -> ParserResult:
        return ParserResult(True, str_input[4:])


class FalseParser(Parser):

    def parse(self, str_input: str) -> ParserResult:
        return ParserResult(False, str_input[5:])


class NullParser(Parser):

    def parse(self, str_input: str) -> ParserResult:
        return ParserResult(None, str_input[4:])


class NumberParser(Parser):
    def parse(self, str_input: str) -> ParserResult:
        i = 0
        while i < len(str_input) and str_input[i] in "-.0123456789":
            i += 1
        num_str = str_input[:i]
        s = str_input[i:]
        if not num_str or num_str.endswith(".") or num_str.endswith("-"):
            return ParserResult(num_str, "")  # Return the incomplete number as is
        num = (
            float(num_str)
            if "." in num_str or "e" in num_str or "E" in num_str
            else int(num_str)
        )
        return ParserResult(num, s)


class AnyParser(Parser):

    def parse(self, str_input: str) -> ParserResult:
        parser = self.find_parser(str_input)
        return parser.parse(str_input.lstrip())

    @staticmethod
    def find_parser(str_input: str) -> Parser:
        parsers: Dict[str, Parser] = {
            "[": ArrayParser(),
            "{": ObjectParser(),
            '"': StringParser(),
            "t": TrueParser(),
            "f": FalseParser(),
            "n": NullParser(),
        }
        number_parser = NumberParser()
        for c in "-0123456789.":
            parsers[c] = number_parser
        return parsers[str_input.lstrip()[0]]


class JsonPartParser:
    @staticmethod
    def parse(s: str) -> Any:
        if len(s) >= 1:
            result = AnyParser().parse(s)
            return json.loads(json.dumps(result.value))
        else:
            return json.loads("{}")
