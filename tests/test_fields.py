from pytest import raises

from fxdc import Config, FxDCField, dumps, loads

from fxdc.exceptions import TypeCheckFailure, NullFailure, BlankFailure

@Config.add_class
class Person:
    username: FxDCField[str] = FxDCField(verbose_name="name", typechecking=True, null=False, blank=False)
    age: FxDCField[int] = FxDCField(verbose_name="age", typechecking=True, null=False, blank=False)
    
    def __init__(self, username: str, age: int = 18):
        self.username = username
        self.age = age

class PersonNoField:
    username: str
    age: int
    def __init__(self, username: str, age: int = 18):
        self.username = username
        self.age = age
        
def test_fields_typechecking():
    user = Person("john_doe", 30)
    user.age = "30"
    
    serialized = dumps(user)
    with raises(TypeCheckFailure):
        loads(serialized)
        
def test_fields_null():
    user = Person("john_doe", 30)
    user.age = None
    serialized = dumps(user)
    with raises((NullFailure, TypeCheckFailure )):
        loads(serialized)
        
def test_fields_blank():
    user = Person("john_doe", 30)
    user.username = ""
    serialized = dumps(user)
    with raises(BlankFailure):
        loads(serialized)
    
def test_field_verbose_name():
    user = Person("john_doe", 30)
    serialized = dumps(user)
    print(serialized)
    data = loads(serialized)
    assert data.original.username == "john_doe"
    assert data.original.age == 30
    assert data.original.__class__.__name__ == "Person"
    
    
def test_nofield_typechecking():
    Config.add_class(PersonNoField, typechecking=True)
    user = PersonNoField("john_doe", 30)
    user.age = "30"
    serialized = dumps(user)
    with raises(TypeCheckFailure):
        loads(serialized)
    
def test_nofield_null():
    Config.remove_class("PersonNoField")
    Config.add_class(PersonNoField, meta_data={"notnull": ["age"]})
    user = PersonNoField("john_doe", 30)
    user.age = None
    serialized = dumps(user)
    with raises(NullFailure):
        loads(serialized)
        
def test_nofield_blank():
    Config.remove_class("PersonNoField")
    Config.add_class(PersonNoField, meta_data={"notblank": ["username"]})
    user = PersonNoField("john_doe", 30)
    user.username = ""
    serialized = dumps(user)
    
    with raises(BlankFailure):
        loads(serialized)
    
def test_nofield_verbose_name():
    Config.remove_class("PersonNoField")
    Config.add_class(PersonNoField, meta_data={"verbose_name": {"username": "name", "age": "age"}})
    user = PersonNoField("john_doe", 30)
    serialized = dumps(user)
    data = loads(serialized)
    
    assert data.original.username == "john_doe"
    assert data.original.age == 30
    assert data.original.__class__.__name__ == "PersonNoField"
    
def test_nofield_seperate_typechecking():
    Config.remove_class("PersonNoField")
    Config.add_class(PersonNoField, meta_data={"typechecking": {"age": int}})
    user = PersonNoField("john_doe", 30)
    user.username = 30
    user.age = "30"
    serialized = dumps(user)
    print(serialized)
    with raises(TypeCheckFailure):
        loads(serialized)

def test_nofield_all_in_one():
    Config.remove_class("PersonNoField")
    Config.add_class(PersonNoField, meta_data={"typechecking": {"age": int}, "notnull": ["age"], "notblank": ["username"], "verbose_name": {"username": "name", "age": "age"}})
    user = PersonNoField("john_doe", 30)
    user.username = 30
    user.age = "30"
    serialized = dumps(user)
    print(serialized)
    with raises(TypeCheckFailure):
        loads(serialized)