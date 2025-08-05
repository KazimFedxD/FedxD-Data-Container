# 📦 FedxD Data Container (FxDC)

FxDC (FedxD Data Container) is a custom lightweight data format and parser for Python. It offers a clean, readable, and type-safe syntax for defining structured data using indentation-based blocks, type hints, and support for nested dicts, lists, and even custom Python classes.

It can parse this structure into:

* Python dictionaries or lists
* Class objects (including custom types)
* JSON-compatible structures

---

## 🛠 Use Cases

FxDC is especially useful in scenarios where data readability and structure matter, such as:

* **Config Files** – cleaner and more expressive than JSON or YAML. Unlike JSON, FxDC supports comments, multiline values, and type hints natively. Compared to YAML, FxDC has a more Pythonic and predictable parsing behavior.
* **Data Serialization** – convert Python objects into a human-readable format without the verbosity of XML or the strictness of JSON.
* **Object Mapping** – easily restore serialized objects back into custom Python classes using type metadata and nested structures.

---

## 🔧 Installation

Install the package via pip:

```bash
pip install fxdc
```

---

## 📘 FxDC Syntax

### ▶ Basic Variables (with or without type hinting)

Type hinting in FxDC allows you to explicitly declare the type of a variable using the `|` symbol. This improves data validation and enables automatic parsing of certain types (like `bool`, `list`, or custom classes) that may otherwise be ambiguous or misinterpreted. It also helps ensure compatibility when converting to typed Python objects or JSON.

For example:

```py
name|str = "John"
age|int = 25
salary|float = 1000.50
```

#### Output:

```json
{
  "name": "John",
  "age": 25,
  "salary": 1000.5
}
```

> Type hinting is optional for primitives, but **required** for certain types like `bool`, `list`, and custom classes.

---

### ▶ Multiline Dictionaries

Multiline dictionaries in FxDC allow you to define grouped key-value pairs using indentation. This structure is especially useful when you want to represent nested or hierarchical data clearly.

By default, a block using `:` and indentation will be treated as a Python `dict`. You can optionally use `|dict` to be explicit about the type. Both forms are supported equally, and type hinting is not strictly required unless you are dealing with more complex structures or want better type enforcement.

```py
user|dict:
    name = "Alice"
    age = 30
```

Or without type hinting:

```py
user:
    name = "Alice"
    age = 30
```

#### Output:

```json
{
  "user": {
    "name": "Alice",
    "age": 30
  }
}
```

---

### ▶ Lists (Untyped and Typed)

FxDC supports both typed and untyped list definitions using indentation and special markers. For a value to be interpreted as a list, you must use the `|list` type hint. Without it, the structure may default to another type like a dictionary or be parsed incorrectly.

Lists can contain values using `=` or `:` and support nesting. You can mix primitive types and compound structures like dictionaries within the same list. When using type hints for items inside the list, there's no need to prefix with `|`; instead, the type name followed by `=` or `:` is enough.

This makes list creation in FxDC both flexible and strongly typed when needed.

#### Example List (Typed or Untyped — Identical Structure)

Whether you use explicit type hinting inside the list or not, the resulting structure can remain the same. The important part is declaring the list itself using `|list`. This example demonstrates a consistent list structure.

```py
mylist|list:
    = "apple"
    = 5
    = 3.14
    dict:
        name = "John"
        age = 23
```

In a typed form:

```py
mylist|list:
    str = "apple"
    int = 5
    float = 3.14
    dict:
        name = "John"
        age = 23
```

#### Output:

```json
{
  "mylist": [
    "apple",
    5,
    3.14,
    {
      "name": "John",
      "age": 23
    }
  ]
}
```

---

### ▶ Nested Structures

FxDC supports deeply nested data using indentation, making it intuitive to represent hierarchies like teams, organizations, or other structured data. Nested structures combine dictionaries and lists to allow rich data representation while remaining human-readable.

In the following example, a list of team members is defined. Each member is represented as a `dict` with their own fields. The `:` symbol is used to separate multiple entries in the list. You must use `|list` to indicate the outer container is a list.

FxDC also supports deeply nested combinations, such as lists within dictionaries, dictionaries within lists, and even recursive structures (limited by Python's recursion limit).

```py
team|list:
    dict:
        name = "John"
        age = 28
    :
        name = "Jane"
        age = 32
```

#### Output:

```json
{
  "team": [
    {
      "name": "John",
      "age": 28
    },
    {
      "name": "Jane",
      "age": 32
    }
  ]
}
```

---

## 🩩 Custom Class Integration

### Define and Register a Class

FxDC allows dynamic integration of your Python classes for seamless deserialization. Once registered, FxDC will automatically map data fields to constructor arguments.

You can also provide custom `fromdata` and `todata` methods during registration via `Config.add_class()` instead of defining them within the class. This is useful when you want to decouple the serialization logic or override class-defined methods.

```python
class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

from fxdc import Config
Config.add_class("MyClass", class_=MyClass)
```

### Or Using a Decorator

```python
@Config.add_class("MyClass")
class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

> You can register your classes with FxDC either manually using `Config.add_class()` or by applying it as a decorator.

### Advanced Serialization (Optional)

FxDC supports custom serialization and deserialization for complex Python classes through `__todata__` and `__fromdata__` methods. These special methods allow you to control how an object is converted to and from raw data, which is especially useful when dealing with custom data representations or when the class structure does not align exactly with the data.

The `__todata__` method should return a representation of the instance's state, which can be any serializable Python type — such as a dictionary, list, string, integer, or float — not just a dictionary. This allows for maximum flexibility when determining how the object should be serialized. The `__fromdata__` method (marked as `@staticmethod`) should take keyword arguments or a single argument (depending on how the data was stored) and return a new instance of the class.

Additionally, if you want to avoid modifying the class directly, you can pass custom `todata` and `fromdata` functions as arguments to `Config.add_class()` during registration. These methods, if provided explicitly, will override the class-defined versions. The `todata` function can return any basic Python type, including `dict`, `list`, `str`, `int`, or `float`, depending on how you want the object to be represented. The corresponding `fromdata` method should accept that structure as input and use it to reconstruct the original object. This means the structure returned by `todata` must match the input expected by `fromdata`, ensuring round-trip serialization and deserialization is consistent and reliable.

This makes it flexible to control object serialization logic without polluting class definitions, which is ideal for working with third-party classes or maintaining clean separation of concerns.

```python
class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __todata__(self):
        return {"name": self.name, "age": self.age}

    @staticmethod
    def __fromdata__(**kwargs):
        return MyClass(kwargs["name"], kwargs["age"])
```

---

## 🔁 Loading & Dumping Data

Loading and dumping data with FxDC is straightforward and mirrors Python's standard file and object serialization workflows. You can either load FxDC-formatted data from a file or directly from a string, and likewise dump your data structures or objects back into FxDC format as a string. These methods are ideal for storing configuration files, exchanging structured data, or serializing objects into a custom readable format.

### Load from File

Loading a `.fxdc` file using `fxdc.load()` returns an instance of `FxDCObject`. This object retains a reference to the original parsed data, including any custom class it may represent. If the loaded data was originally a class-serialized object, you can retrieve the actual object instance using the `.original` property of the returned `FxDCObject`. This is particularly helpful when working with deserialized custom classes registered through `Config.add_class()`.

```python
import fxdc
obj = fxdc.load("data.fxdc")
```

### Load from String

```python
from fxdc import loads

fxdc_string = '''
name|str = "John"
age|int = 23
'''
obj = loads(fxdc_string)
```

### Dump to FxDC Format

```python
from fxdc import dumps

obj = {"name": "John", "age": 23}
fxdc_string = dumps(obj)
print(fxdc_string)
```

### Load as JSON-Compatible Output

FxDC includes a method called `to_json()` which converts a raw FxDC-formatted string directly into a valid JSON string. This method streamlines the process of converting structured FxDC data into a JSON string without the need to deserialize it into Python objects first and then re-serialize it again into JSON. This not only reduces memory usage but also saves time and avoids the overhead of class reconstruction and object mapping.

The `to_json()` method is especially useful in scenarios where the primary objective is to export or store structured data, and there is no intention of reconstructing custom Python classes from it.

> ⚠️ **Warning:** The `to_json()` method completely discards any class metadata or custom class references. If your FxDC string contains serialized custom class data, using this method will result in a JSON output that **cannot** be converted back into those classes.

```python
from fxdc import to_json

fxdc_str = """
name|str = "John"
age|int = 23
"""
json_str = to_json(fxdc_str)
print(json_str)
```

---

## 🔁 Recursive Depth Control

FxDC uses recursive loading. If parsing fails due to recursion errors (especially with deeply nested structures), you can increase the limit:

```python
from fxdc import Config
Config.set_recursion_limit(10000)  # Default is 1000
```

> This is useful for very deeply nested data structures where Python's default recursion limit may be exceeded.

---

## ❗ Exceptions

FxDC includes custom exceptions to provide better error handling and debugging support when loading, dumping, parsing, or working with typed objects and classes. All custom exceptions inherit from the base `FXDCException`, which itself is not intended to be raised directly.

Here are the primary exceptions:

* **FXDCException** *(base class)*: The root of all FxDC exceptions. Cannot be raised directly.

* **InvalidExtension**: Raised if the `load()` function receives a file that does not have the `.fxdc` extension.

* **FileNotReadable**: Raised when a file cannot be read, either due to permission issues or other I/O errors.

* **FileNotWritable**: Raised during `dump()` if the provided file path cannot be edited or written to.

* **InvalidData**: Raised during lexing or parsing if the structure of the FxDC data is incorrect, does not match the expected configuration, or if a required class was not registered using `Config.add_class()`. This can also occur if a variable shares a name with a registered class, potentially generating incorrect tokens during parsing.

* **InvalidJSONKey**: Raised when a dictionary contains an invalid JSON key.

* **ClassAlreadyInitialized**: Raised when attempting to add a class to the configuration using a name that already exists or is already registered.

---

## 🧩 Default Custom Classes

FxDC includes several default Python and third-party classes that are pre-initialized and available for immediate use. These classes are registered by default with `Config`, which means you can use them in your `.fxdc` files without any additional setup or registration. This makes it easy to serialize and deserialize common types without writing custom logic.

If you attempt to use one of these classes but the required external library (like NumPy or Pandas) is not installed, FxDC will skip initialization for that specific class and continue without raising an error. This ensures compatibility while avoiding crashes in environments where optional libraries are not available.

The following built-in classes are supported:

### 🐍 Native Python Classes:

* `set`
* `dict_items`, `dict_keys`, `dict_values`
* `range`
* `map`, `filter`, `enumerate`, `zip`
* `tuple`
* `bytes`, `bytearray`

### 📊 Data Libraries:

* **Pandas**:

  * `DataFrame`

* **NumPy**:

  * `NDArray`
  * `Matrix`

### 🕒 Datetime:

* `Date`
* `Time`
* `DateTime`
* `TimeDelta`

These classes are commonly used in data science, scripting, and backend development. By default, they are handled efficiently by FxDC, so you don't need to write boilerplate class registration code.

> ⚠️ For requests to include support for other classes, feel free to open an issue or suggestion on the project's [GitHub repository](https://github.com/KazimFedxD/FedxD-Data-Container/issues).

---

## 🧪 Example: Object <-> FxDC

### Python Class

```python
from fxdc import dumps, Config

@Config.add_class()
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

user = User("John", 23)
fxdc_str = dumps(user)
print(fxdc_str)
```

### Output FxDC

```py
main|User:
    name|str = "John"
    age|int = 23
```

---

## 📋 Future Plans / TODO

* FxDC has the potential to replace formats like YAML or JSON when you want to retain Python class structures without the need to manually serialize or deserialize objects.
* This is especially helpful for developers who want to avoid boilerplate conversion logic and prefer a structured, Pythonic way to store, load, and share data.
* Feedback and suggestions are welcome! If you have any ideas or concerns, please open an issue or contribute via a pull request on the [GitHub repository](https://github.com/KazimFedxD/FedxD-Data-Container).

---

## 🙌 Credits

Made with ❤️ by **Kazim Abbas (FedxD)** GitHub: [KazimFedxD](https://github.com/KazimFedxD)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
