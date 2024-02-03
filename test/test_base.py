from json_part import parse_incomplete_json

BIG_JSON_SAMPLE = """
{"string":"wartość_tekstowa","number":123,"boolean":true,"null_value":null,
"array":[1,"dwie",false,{"klucz":"wartość"}],"object":{"key1":"value1",
"key2":456,"key3":false,"key4":["a","b","c"],"key5":{"nested_key":"nested_value"}}}

""".strip()

BIG_JSON_PARSED = {
    "string": "wartość_tekstowa",
    "number": 123,
    "boolean": True,
    "null_value": None,
    "array": [1, "dwie", False, {"klucz": "wartość"}],
    "object": {
        "key1": "value1",
        "key2": 456,
        "key3": False,
        "key4": ["a", "b", "c"],
        "key5": {"nested_key": "nested_value"},
    },
}


def test_number_array_1() -> None:
    assert parse_incomplete_json("[1, 2, 3") == [1, 2, 3]


def test_number_array_2() -> None:
    assert parse_incomplete_json("[1, 2, 3, 4.1") == [1, 2, 3, 4.1]


def test_bool_none_array_1() -> None:
    assert parse_incomplete_json("[null, true, false, tr") == [None, True, False, True]


def test_object_1() -> None:
    part = """{"count": 2, "ddd"""
    assert parse_incomplete_json(part) == {"count": 2}


def test_object_2() -> None:
    part = """{"count": 2, "ddd": "frevf"""
    assert parse_incomplete_json(part) == {"count": 2, "ddd": "frevf"}


def test_big_json() -> None:
    assert parse_incomplete_json(BIG_JSON_SAMPLE) == BIG_JSON_PARSED
