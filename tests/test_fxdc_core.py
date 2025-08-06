import pytest
from fxdc import load, loads, dumps, to_json, Config
from fxdc.exceptions import FXDCException, InvalidData

def test_basic_primitives_roundtrip():
    example = 'name|str = "John"\nage|int = 23'
    obj = loads(example)
    data = obj.to_dict() if hasattr(obj, 'to_dict') else obj.original
    assert data == {"name": "John", "age": 23}

    round = dumps(data)
    assert 'name|str' in round and 'age|int' in round

def test_nested_structure():
    fxdc_str = '''
user:
    name = "Alice"
    age = 30
'''
    obj = loads(fxdc_str)
    data = obj.original
    assert isinstance(data["user"], dict)
    assert data["user"]["name"] == "Alice"
    assert data["user"]["age"] == 30

def test_list_parsing():
    fxdc_str = '''
items|list:
    str = "apple"
    int = 42
    float = 3.14
'''
    obj = loads(fxdc_str)
    data = obj.original
    assert isinstance(data["items"], list)
    assert data["items"] == ["apple", 42, 3.14]

def test_to_json_method():
    fxdc_str = 'a|int = 5\nb|float = 1.23'
    json_str = to_json(fxdc_str)
    import json
    parsed = json.loads(json_str)
    assert parsed == {"a": 5, "b": 1.23}

def test_invalid_data_raises():
    broken = 'name|int = "not-an-int"'
    with pytest.raises(InvalidData):
        loads(broken)

