import json

from json_part.parser import JsonPartParser

JSON = """
{"glossary": {"title": "example glossary", "GlossDiv": {"title": "S", "GlossList": 
{"GlossEntry": {"ID": "SGML", "SortAs": "SGML", "GlossTerm": "Standard Generalized Markup Language", 
"Acronym": "SGML", "Abbrev": "ISO 8879:1986", "GlossDef": {"para": "A meta-markup language, 
used to create markup languages such as DocBook.", "GlossSeeAlso": ["GML", "XML"]}, 
"GlossSee": "markup"}}}}}

""".strip()
if __name__ == "__main__":
    TEST = "[1, 2, 3"
    print(JsonPartParser().parse(TEST))
    TEST = "[null, true, false, tr"
    print(JsonPartParser().parse(TEST))
    TEST = """
    {"count": 2, "ddd
    """
    print(JsonPartParser().parse(TEST))
    TEST = """
    {"count": 2, "ddd": "frevf
    """
    print(JsonPartParser().parse(TEST))
    print("#############")
    JSON = json.dumps(json.loads(JSON))
    for it in range(len(JSON)):
        part = JSON[0 : it + 1]
        print(part)
        print(JsonPartParser().parse(part))
        print()
    print()
