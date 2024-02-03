# json-part

## Installation

```bash
pip install json-part
```

## Usage
```python
from json_part import parse_incomplete_json, fix_incomplete_json

if __name__ == '__main__':
    SAMPLE_1 = """{"status": "o"""  # {"status": "o
    print(parse_incomplete_json(SAMPLE_1))  # {'status': 'o'}
    print(fix_incomplete_json(SAMPLE_1))  # {"status": "o

    SAMPLE_2 = """{"status": "o", "mess"""  # {"status": "o", "mess
    print(parse_incomplete_json(SAMPLE_2))  # {'status': 'o'}
    print(fix_incomplete_json(SAMPLE_2))  # {'status': 'o'}
```
