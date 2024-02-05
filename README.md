# json-part

[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![Python package & deploy](https://github.com/markowanga/json-part/actions/workflows/python-publish.yml/badge.svg)](https://github.com/markowanga/json-part/actions/workflows/python-publish.yml)
[![PyPI version](https://badge.fury.io/py/json-part.svg)](https://badge.fury.io/py/json-part)
[![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)

`json-part` is a lightweight Python library designed to parse and
repair incomplete JSON strings. This library is particularly useful
for handling streaming JSON data, such as the responses from
OpenAI's Large Language Models (LLMs). By enabling the processing
of partial JSON responses, `json-part` enhances the user experience
by providing immediate, incremental results.

Currently, there is no standard for loading such data,
and the project has made many assumptions which, in my opinion,
were correct. A fully generic, flexible solution was not prepared.
The library code is simple and clear -- requests for contributions,
or ideas submitted as an Issue, will be met with
all efforts to create the best possible solution.

## Features

- **Parse Incomplete JSON:** Effortlessly convert partial JSON
  strings into usable Python dictionaries.
- **Fix Incomplete JSON:** Automatically repair and close
  open JSON structures to prevent parsing errors.
- **Stream-Friendly:** Ideal for applications that consume
  streaming JSON data, improving responsiveness and user interaction.

## Installation

To get started with `json-part`, simply install the package using pip:

```bash
pip install json-part
```

## Usage

The `json-part` library is straightforward to use, with functions
to parse and fix incomplete JSON strings. Here's a quick
example to demonstrate its capabilities:

```python
from json_part import parse_incomplete_json, fix_incomplete_json

if __name__ == '__main__':
    # Example of an incomplete JSON string
    SAMPLE_1 = """{"status": "o"""  # {"status": "o
    # Parse the incomplete JSON to a Python dictionary
    print(parse_incomplete_json(SAMPLE_1))  # Output: {'status': 'o'}
    # Fix the incomplete JSON string
    print(fix_incomplete_json(SAMPLE_1))  # Output: {"status": "o"}

    # Another example with a slightly more complex incomplete JSON string
    SAMPLE_2 = """{"status": "o", "mess"""  # {"status": "o", "mess
    # Parse and fix operations can handle more complex structures
    print(parse_incomplete_json(SAMPLE_2))  # Output: {'status': 'o'}
    print(fix_incomplete_json(SAMPLE_2))  # Output: {"status": "o"}
```

## Run samples

Samples require `OPENAI_API_KEY` env variable configured, and installed dependencies (command `poetry install`).

### Terminal sample

Print next values in terminal.

```bash
(json_part) markowanga@MacBook-Pro-Marcin sample % python sample/openai_sample.py          
{}
{'year': 1886}
{'year': 1886, 'inventor': ''}
{'year': 1886, 'inventor': 'K'}
{'year': 1886, 'inventor': 'Karl'}
{'year': 1886, 'inventor': 'Karl Benz'}
{'year': 1886, 'inventor': 'Karl Benz', 'keywords': ['']}
{'year': 1886, 'inventor': 'Karl Benz', 'keywords': ['car']}
{'year': 1886, 'inventor': 'Karl Benz', 'keywords': ['car', '']}
{'year': 1886, 'inventor': 'Karl Benz', 'keywords': ['car', 'transport']}

...
```

### Api sample

Website with dynamic fields in report.

```bash
(json_part) markowanga@MacBook-Pro-Marcin sample % cd sample && uvicorn api_sample:app          
INFO:     Started server process [43425]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

And next open http://127.0.0.1:8000 in your browser.

## Contributing

Contributions to `json-part` are welcome!
Whether it's reporting a bug, discussing improvements,
or submitting a pull request, all contributions
help make `json-part` better for everyone.

## License

`json-part` is released under the MIT License.
See the LICENSE file for more details.
