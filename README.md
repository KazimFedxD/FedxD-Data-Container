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
Config.add_class(class_=MyClass)
```

### Or Using a Decorator

```python
@Config.add_class
class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

> You can register your classes with FxDC either manually using `Config.add_class()` or by applying it as a decorator.

### Entering Custom Name
FxDC Config add_class() also supports custom names for distinguishing b/w different classes with same name

> ⚠️ **Warning:** Using different name that the class will result in different name in the fxdc file. During Loading the FxDC File If the Name in the Config is changed or is assigned to a different class it will lead to failure

```py
from queue import Queue

# Registering Queue class with FxDC as "Queue"
Config.add_class("Queue", class_=Queue)

from multiprocessing import Queue

# Registering multiprocessing Queue class with FxDC as "MultiprocessingQueue"
Config.add_class("MultiprocessingQueue", class_=Queue)
```

This example shows that you can add classes that have the same name and load it to the config with different names.

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

## 🧰 Advanced Class Integration

FxDC now supports enhanced **type checking** and rich metadata for class variables via the `FxDCField` helper. This feature enables automatic validation, default values, and improved documentation generated from your class definitions, making your data models more robust and user-friendly.

### Declaring Fields with `FxDCField`

Use `FxDCField` to declare variables with additional metadata and validation options:

- **desc**: A textual description of the field, which will be included in the FxDC output to help document the data.
- **verbose_name**: A human-friendly or display name for the field, used in the FxDC output instead of the actual variable name for clarity.
- **default**: A default value assigned to the field if it is missing in the input data during loading.
- **typechecking**: Enables type validation when loading the FxDC data.
- **null**: Indicates whether the field can accept `None` as a value.
- **blank**: Indicates whether the field can be omitted or left empty.

---

### Verbose Name

The `verbose_name` parameter allows you to specify a human-friendly or display name for a field. This name will be used in the FxDC output instead of the variable name, making the data file easier to read and understand for end users or documentation purposes. It is especially helpful when variable names are abbreviated, technical, or not descriptive enough on their own.

Example:

```python
from fxdc import FxDCField, Config

@Config.add_class
class User:
    name: FxDCField[str] = FxDCField(verbose_name="username")
    age: int
```

**FxDC output:**

```fxdc
main|User:
    username|str = "JohnDoe"
    age|int = 30
```

---

### Default Value

The `default` parameter provides a fallback value for a field if it is missing from the FxDC input during loading. This is useful for ensuring that your data objects always have valid values, even when the input is incomplete. It helps prevent errors caused by missing data and simplifies your data validation logic by centralizing defaults within the class definition.

Example:

```python
@Config.add_class
class User:
    name: FxDCField[str] = FxDCField(default="Guest")
    age: int
```

If the `name` field is not present in the FxDC data, it will automatically be set to `"Guest"` after loading. The output data might look like this:

```fxdc
main|User:
    age|int = 25
    name|str = "Guest"
```

This mechanism makes your FxDC-defined classes more robust and easier to maintain, especially when working with optional or evolving data schemas.

---

### Field Descriptions in FxDC Output

You can provide a descriptive `desc` for each field, which will be included in parentheses next to the type in the FxDC output for better documentation and clarity:

```python
@Config.add_class
class User:
    username: FxDCField[str] = FxDCField(desc="The username of the user")
    age: FxDCField[int] = FxDCField(desc="The age of the user")
```

**FxDC output:**

```fxdc
main|User:
    username|str(The username of the user) = "john_doe"
    age|int(The age of the user) = 30
```

---

### Enabling Type Checking Globally for a Class

You can enable type checking for all variables declared in a class by passing the `typechecking=True` argument to `Config.add_class()`. This enforces type validation on every field during FxDC parsing.

```python
@Config.add_class(typechecking=True)
class User:
    name: FxDCField[str] = FxDCField(desc="User's full name")
    age: FxDCField[int] = FxDCField(desc="User's age")
```

---

### Manual Per-Variable Type Checking

Alternatively, you can control type checking on a per-variable basis by setting the `typechecking` parameter individually in `FxDCField`. This provides fine-grained control even if global class type checking is disabled or enabled.

```python
@Config.add_class
class Product:
    name: FxDCField[str] = FxDCField(typechecking=True, desc="Product name")
    price: FxDCField[float] = FxDCField(typechecking=False, desc="Price without validation")
```

In this example, `name` will be type-checked during loading, but `price` will bypass type validation.

---

### Manual Metadata Configuration for Imported or External Classes

For advanced use cases—such as integrating third-party or imported classes that you cannot modify—you can manually provide metadata to `Config.add_class()` using the `meta_data` argument. This dictionary allows you to specify all field metadata externally, including type checking, descriptions, verbose names, default values, and null/blank constraints.

Example:

```python
from fxdc import Config, FxDCField

class User:
    username: FxDCField[str] = FxDCField(desc="The username of the user")
    age: FxDCField[int] = FxDCField(desc="The age of the user")

    def __init__(self, username: str, age: int):
        self.username = username
        self.age = age

User = Config.add_class(User, meta_data={
    "typechecking": {
        "username": str,
        "age": int
    },
    "description": {
        "username": "The username of the user",
        "age": "The age of the user"
    },
    "verbose_name": {
        "username": "name",
    },
    "default": {
        "username": "default_user",
    },
    "notnull": {
        "username": True,
        "age": True
    },
    "notblank": {
        "username": False,
        "age": False
    }
})
```

This approach gives you full control over field behavior and validation even when working with classes that lack built-in FxDC metadata.

---

## ⚙️ Configuration Export & Import  

From this update onward, **FxDC** can now **save** and **reload** all your class metadata using **configuration files**!  
Think of it as a **blueprint** for your classes — portable, sharable, and always ready to reload. 🚀  

---

### ⚠️ Important Warning  
> **All classes present in the configuration file _must_ be loaded into `Config` before importing it.**  
> If a class in the config file isn’t already registered with `Config`, the import will fail.  
> This ensures FxDC can correctly link metadata to the right classes.  

---

### 📦 What Gets Saved?  
When you export a config, FxDC will keep:  
- 🏷 **Type definitions** → `username` must be `str`, `age` must be `int`  
- 📝 **Descriptions** → for better understanding  
- 🪪 **Verbose names** → human-friendly labels  
- 🎯 **Default values** → pre-set starting data  
- ✅ **Constraints** → like `notnull` or `notblank`  

💡 **In short:** Everything needed to recreate your class exactly as you defined it — without touching a single line of code again.  

---

### 📤 Exporting Configurations  

```python
Config.export_config()
```
- Saves **all registered classes** into `config.fxdc` by default.  
- Want a custom file name? No problem:  
```python
Config.export_config("user_data_config.fxdc")
```

---

### 📥 Importing Configurations  

```python
Config.import_config()
```
- Loads `config.fxdc` by default.  
- Want to load a different file? Easy:  
```python
Config.import_config("user_data_config.fxdc")
```

---

### 💻 Full Example  

```python
from fxdc import Config, FxDCField

@Config.add_class
class User:
    username: FxDCField[str] = FxDCField(desc="The username of the user")
    age: FxDCField[int] = FxDCField(desc="The age of the user")

# Save the configuration
Config.export_config("user_config.fxdc")

# ... Later or in another project ...
Config.import_config("user_config.fxdc")

# ✅ Metadata is instantly available!
```

---

### 🗂 Example Config File  

```plaintext
!CONFIG FILE!

Config_User|dict:
	typechecking|dict:
		username|str="str"
		age|str="int"
	verbose_name|dict:
		username|str="name"
	default|dict:
		username|str="guest"
	notnull|list:
		str="username"
	notblank|list:
		str="username"
	description|dict:
		username|str="name of the user"
		age|str="age of the user"
```

---

### 🌟 Why You’ll Love This  
- 🔄 **Reusable** — no more redefining metadata in every file.  
- 📂 **Portable** — move configs between projects effortlessly.  
- 🤝 **Collaboration-friendly** — share with teammates for consistent setups.  
- ⏱ **Time-saving** — load everything in one command.  

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

FxDC includes **custom exceptions** to provide better error handling and debugging support when loading, dumping, parsing, or working with typed objects and classes.  
All custom exceptions inherit from the base **`FXDCException`** *(not intended to be raised directly)*.

---

### 🏛 **Base Exception**
- **`FXDCException`** *(base class)* — 🏷 The root of all FxDC exceptions.  
  🚫 **Cannot** be raised directly.

---

### 📂 **File & Extension Errors**
- **`InvalidExtension`** — 📄 Raised if `load()` receives a file without the **`.fxdc`** extension.  
- **`FileNotReadable`** — 🚫 Raised when a file cannot be read due to **permissions** or other I/O errors.  
- **`FileNotWritable`** — ✏ Raised during `dump()` if the provided path **cannot be edited** or written to.

---

### 📜 **Data & Parsing Errors**
- **`InvalidData`** — 🛑 Raised during **lexing or parsing** when:
  - The FxDC structure is invalid or mismatches the configuration.  
  - A required class is missing from `Config.add_class()`.  
  - A variable name conflicts with a registered class name.
- **`InvalidJSONKey`** — 🔑 Raised when a dictionary contains an **invalid JSON key**.
- **`ClassNotLoaded`** — 📦 Raised when a **referenced class** in an FxDC or config file is not loaded into the configuration.  
- **`NoConfigFound`** — 📁 Raised when the **configuration file is missing**, invalid, or corrupted.

---

### 🏗 **Field Validation Errors**
- **`FieldError`** — ⚠ Raised when there’s an error **creating a field**, e.g.:
  - No type specified for type checking.  
  - Description too long.
- **`TypeCheckFailure`** — 📏 Raised when a field’s **value type** does not match the expected type.  
- **`NullFailure`** — 🚫 Raised when a **non-null** field contains a `null` (`None`) value.  
- **`BlankFailure`** — ❌ Raised when a **non-blank** field is empty or contains only whitespace.

---

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

@Config.add_class
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

## 🤝 Contributions

We welcome contributions to improve FxDC — from fixing typos to adding new features or optimizing performance.  
Whether you’re a developer, tester, or just an enthusiastic user, your help is valuable.  

---

### 🛠 How to Contribute
1. **Fork** the repository.
2. **Create** a feature branch (`git checkout -b feature-name`).
3. **Commit** your changes with clear messages.
4. **Push** to your branch.
5. **Open a Pull Request** with details about your changes.

💡 Please follow the existing code style and write clear commit messages.

---

### 🧪 Beta Testers
Beta testers are crucial for ensuring **FxDC’s stability** before public releases.  
They help by:
- Testing **new features** before official release.
- Reporting bugs, crashes, and performance issues.
- Suggesting **improvements** for the user experience.

📋 **Current Beta Testers**
- *FedxD* — 🏆 Lead Developer/Creator & Initial Tester
- *(Add contributors here as they join)*

> ⚠ **Note:** Beta versions may contain **unfinished features** and **experimental changes**.  
> They are **not recommended** for production environments.

---

### 📜 Contributor Recognition
All contributors are **credited in the README** and changelog.  
Significant contributions will be mentioned in **release notes**.

---


## 🙌 Credits

Made with ❤️ by **Kazim Abbas (FedxD)** GitHub: [KazimFedxD](https://github.com/KazimFedxD)

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
