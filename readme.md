# FedxD Data Container (FxDC)

## Preview

#### It is used to  convert a FxDC string to FxDC object than can be parsed

### FxDC String
```py
name|str = "John"
age|int = 23
address|dict:
	street|str = "123 Main St"
	city|str = "New York"
phone|list:
	a|str = "555-1234"
	b|str = "555-4567"
```

#### It Can be Converted To a FxDC class Object or a Json Supported Dictionary

### Converted Json Dictionary
```json
{
    "name": "John",
    "age": 23,
    "address": {
        "street": "123 Main St",
        "city": "New York"
    },
    "phone": [
        "555-1234",
        "555-4567"
    ]
}
```
## Get Started


1. install the  python pacakge 
	`pip install fxdc`
2. import fxdc `import fxdc`
3. Enjoy

#
# Syntax
## Basic Syntax

```py
name="John"
age=12
salary=1000.00
```

## Type Hinting Syntax
```py
name|str="John"
age|int=12
is_male|bool=1
salary|float=1000.00
```

### Some Types Can Only Be Accessed By Type Hinting Like Bool, List And Custom Classes

## MultiLine Variable
```py
mydict:
	name|str="John"
	age|int=12
```

### Multi Line Variables Without Type Hinting Is a Python Dict. Indentation Is Required to Diffrentiate B/w variables

## List Syntax
### List Syntax is a Bit More Complicated. The Variable Name is ignored when using list and only the value and type is noted
```py
mylist|list:
	a=100
	b="john"
	c=1203.323
	d|bool="False"
```
### Python Output
```py
[100, "john", 1203.323, False]
```

## Nested Variables

```py
members|list:
	a|dict:
		name="John"
		age=10
	b:
		name="Micheal"
		age = 120
```
### Python Output
```py
[
	{
		"name": "John",
		"age": 10
	},
	{
		"name": "Micheal",
		"age": 120
	}
]
```

## Custom Class Types

### Class
```py
class MyClass:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	def __repr__(self):
		return f"<{self.name}: {self.age}>"
```
### FxDC File
```py
main|MyClass:
	name="john"
	age=23
```

### In Order To Make Bot Use Custom Class U Need To Add The Class To Config
```py
from fxdc import Config

Config.add_class("MyClass", MyClass) #Name of Class, Class
```
### This Will Ensure The Initializing Of The Class When Loading the FxDC container
#### You Can Have a to_data() function and from_data() function to get and put information to make the class object. from_data() should be of @staticmethod
```py
class MyClass:
	def __init__(self, name, age):
		self.name = name
		self.age = age
		self.salary = age * 2
	def __repr__(self):
		return f"<{self.name}: {self.age}>"
	def to_data(self) -> dict:
		return {
			"name": self.name,
			"age": self.age
		}
	@staticmethod
	def from_data(**kwargs) -> "MyClass":
		return MyClass(kwargs["name"], kwargs["age"])
```

#
# Usage

## Converting FxDC to Class Object

### From File

```py
import fxdc

fxdcobject = fxdc.load("main.fxdc") #Name of the File
```

### OR

```py
import fxdc

with open("main.fxdc", "w") as f:
	fxdcobject = fxdc.load(f)
```

### From String

```py
fxdcstring = """
name|str = "John"
age|int = 23
address|dict:
	street|str = "123 Main St"
	city|str = "New York"
phone|list:
	a|str = "555-1234"
	b|str = "555-4567"
"""

from fxdc import loads

fxdcobject = loads(fxdcstring)
```

## Converting Class Object To FxDC

#### You Can Put Any Type of object to convert to FxDC including strings and custom objects


### Class Object

```py
class MyClass:
	def __init__(self, name:str, age:int):
		self.name = name
		self.age = age

	def __repr__(self):
		return f"{self.name}: {self.age}"
	
from fxdc import dumps

obj = MyClass("John", 23)

fxdcstring = dumps(obj)
print(fxdcstring)
```
```
main|MyClass:
        name|str="John"
        age|int=20
```
#### It Also Inputs The Same Class And Can Auto Convert To That Class

# Credits
### All Packages Made And Manages by FedxD



