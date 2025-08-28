from json import load
import os
import sys
from collections.abc import Callable
from types import NoneType
from typing import (Any, Optional, Protocol, TypeAlias, TypeVar, get_args,
                    get_origin, overload)

from fxdc.exceptions import (BlankFailure, ClassAlreadyInitialized, FieldError, NoConfigFound,
                             NullFailure, TypeCheckFailure, ClassNotLoaded)
from fxdc.fields import Field

T = TypeVar("T", bound=type)


class IdentityDeco(Protocol):
    def __call__(self, arg: T, /) -> T: ...


TB = TypeVar("TB", bound=type)

AcceptableTypes: TypeAlias = (
    int | float | str | bool | list[Any] | dict[str, Any] | NoneType
)

DEFAULT_TYPES = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "list": list,
    "dict": dict,
}

class _customclass:
    def __init__(
        self,
        classname: str,
        class_: type[TB],
        meta_data: dict[str, dict[str, Any]],
        from_data: Optional[Callable[..., TB]] = None,
        to_data: Optional[Callable[[object], dict[str, AcceptableTypes]]] = None,
    ) -> None:
        self.classname = classname
        self.class_ = class_
        self.from_data = from_data
        self.meta_data = meta_data
        if not from_data:
            if hasattr(class_, "__fromdata__"):
                self.from_data = class_.__fromdata__
        self.to_data = to_data
        if not to_data:
            if hasattr(class_, "__todata__"):
                self.to_data = class_.__todata__

    def __call__(self, *args: Any, **kwargs: Any) -> object:
        # Convert Verbose Names to kwargs
        newkwargs = {}
        for key, value in kwargs.items():
            for original_name, verbose_name in self.meta_data.get(
                "verbose_name", {}
            ).items():
                if key == verbose_name:
                    newkwargs[original_name] = value
                    break
            else:
                newkwargs[key] = value

        # Add Defaults
        for key, value in self.meta_data.get("default", {}).items():
            if key not in newkwargs:
                newkwargs[key] = value

        # CHECKS
        for key, value in newkwargs.items():
            # Check Type Checking
            if key in self.meta_data.get("typechecking", {}):
                expected_type = self.meta_data["typechecking"][key]
                if not isinstance(value, expected_type):
                    raise TypeCheckFailure(
                        f"Expected type {expected_type} for {key}, got {type(value)}"
                    )

            # Check Nullability
            if key in self.meta_data.get("notnull", []):
                if value is None:
                    raise NullFailure(f"Field {key} cannot be None")

            # Check Blankness
            if key in self.meta_data.get("notblank", []):
                if value == "":
                    raise BlankFailure(f"Field {key} cannot be blank")

        for key in self.meta_data.get("notnull", []):
            if key not in newkwargs:
                raise NullFailure(f"Field {key} cannot be None")

        if self.from_data:
            return self.from_data(*args, **newkwargs)
        return self.class_(*args, **newkwargs)

    def __repr__(self) -> str:
        return self.classname

    def return_data(self, obj: object) -> dict[str, Any]:
        if self.to_data:
            data = self.to_data(obj)
        else:
            data = obj.__dict__
        # Convert verbose names to keys
        if isinstance(data, dict):
            new_data: dict[str, Any] = {}
            for key, value in data.items():
                if key in self.meta_data.get("verbose_name", {}):
                    new_data[self.meta_data["verbose_name"][key]] = value
                else:
                    new_data[key] = value

            # Add defaults
            for key, value in self.meta_data.get("default", {}).items():
                if key not in new_data:
                    new_data[key] = value
        else:
            new_data = data
        descriptions: dict[str, str] = {}
        for key, value in self.meta_data.get("description", {}).items():
            if key in self.meta_data.get("verbose_name", {}):
                descriptions[self.meta_data["verbose_name"][key]] = value
            else:
                descriptions[key] = value

        if not descriptions:
            descriptions = None

        if isinstance(new_data, dict):
            return new_data, descriptions

        return new_data, {}

    def __str__(self) -> str:
        return "Custom Class: " + self.classname

    def __eq__(self, o: object) -> bool:
        if isinstance(o, _customclass):
            return self.classname == o.classname
        elif isinstance(o, str):
            return self.classname == o
        return False


class _config:
    def __init__(self) -> None:
        self.custom_classes: list[_customclass] = []
        self.custom_classes_names: list[str] = []
        self.debug__: bool = False
    

    @overload
    def add_class(
        self,
        *,
        name: Optional[str] = None,
        from_data: Optional[Callable[..., object]] = None,
        to_data: Optional[Callable[..., dict[str, AcceptableTypes]]] = None,
        typechecking: bool = False,
    ) -> IdentityDeco:
        """Decorator to add a class to the config

        Args:
            name (Optional[str], optional): Name of the class. Defaults to None.
            from_data (Optional[Callable[..., object]], optional): Function to convert data to class. Defaults to None.
            to_data (Optional[Callable[..., dict[str, AcceptableTypes]]], optional): Function to convert class to data. Defaults to None.
            typechecking (bool, optional): Whether to enable type checking. Defaults to False.

        Returns:
            IdentityDeco: Decorator to add a class to the config

        Usage:
            ```py
            @Config.add_class(name="MyClass", from_data=my_from_data, to_data=my_to_data, typechecking=True)
            class MyClass:
                pass
            ```
        """
        ...

    @overload
    def add_class(
        self,
        class_: T,
        *,
        name: Optional[str] = None,
        from_data: Optional[Callable[..., object]] = None,
        to_data: Optional[Callable[..., dict[str, AcceptableTypes]]] = None,
        typechecking: bool = False,
        meta_data: Optional[dict[str, Any]] = None,
    ) -> T:
        """Add a class to the config

        Args:
            class_ (Optional[T], optional): The class to add. Defaults to None.
            name (Optional[str], optional): The name of the class. Defaults to None.
            from_data (Optional[Callable[..., object]], optional): Function to convert data to class. Defaults to None.
            to_data (Optional[Callable[..., dict[str, AcceptableTypes]]], optional): Function to convert class to data. Defaults to None.
            typechecking (bool, optional): Whether to enable type checking. Defaults to False.
            meta_data (Optional[dict[str, dict[str, Any]]], optional): Metadata for the class. Defaults to None.

        Returns:
            T: _description_
        """
        ...

    def add_class(
        self,
        class_: Optional[object] = None,
        *,
        name: Optional[str] = None,
        from_data: Optional[Callable[..., object]] = None,
        to_data: Optional[Callable[..., dict[str, AcceptableTypes]]] = None,
        typechecking: bool = False,
        meta_data: Optional[dict[str, Any]] = None,
    ) -> object:
        """Add a custom class to the config

        Args:
            classname (Optional[str], optional): Name For The Class. Defaults to `class_.__name__`.
            from_data (Optional[Callable[..., object]], optional): Function to convert data to class. Defaults to class_.__fromdata__ if it exists. or class_.__init__ or class.__new__
            to_data (Optional[Callable[..., dict[str, Any]]], optional): Function to convert class to data. Defaults to class_.__todata__ if it exists. or class_.__dict__
            class_ (Optional[type], optional): Class to add. If not provided, it will return a decorator.
            typechecking (bool, optional): Whether to enable type checking. Defaults to False.
            meta_data (Optional[dict[str, dict[str, Any]]], optional): Metadata for the class. Defaults to None.
        Returns:
            if Class_ is provided, it will add and return the class
            if class_ is not provided, it will return a decorator to add on top of the class

        Usage:
            ```py
            @Config.add_class
            class MyClass:
                def __init__(self, data):
                    self.data = data
            ```
            OR
            ```py
            class MyClass:
                def __init__(self, data):
                    self.data = data


            Config.add_class("MyClass", class_=MyClass)"""

        def generate_meta_data(class_: type) -> dict[str, dict[str, Any]]:
            if not meta_data:
                data = {
                    "typechecking": {},
                    "verbose_name": {},
                    "default": {},
                    "notnull": [],
                    "notblank": [],
                    "description": {},
                }
            else:
                data = meta_data
                data.setdefault("typechecking", {})
                data.setdefault("verbose_name", {})
                data.setdefault("default", {})
                data.setdefault("notnull", [])
                data.setdefault("notblank", [])
                data.setdefault("description", {})
            if typechecking:
                for name, annotated_type in class_.__annotations__.items():
                    origin = get_origin(annotated_type)
                    args = get_args(annotated_type)
                    if origin is Field and args:
                        data["typechecking"][name] = args[0]
                    else:
                        data["typechecking"][name] = annotated_type
            for name, field in class_.__dict__.items():
                if isinstance(field, Field):
                    if field.typechecking and not typechecking:
                        annotation = class_.__annotations__.get(name, None)
                        if not annotation:
                            raise FieldError(
                                f"Field {name} is typechecked but no type annotation found"
                            )
                        if get_origin(annotation) is Field:
                            data["typechecking"][name] = (
                                get_args(annotation)[0]
                                if get_origin(get_args(annotation)[0]) is None
                                else get_origin(get_args(annotation)[0])
                            )
                        else:
                            data["typechecking"][name] = (
                                annotation
                                if get_origin(annotation) is None
                                else get_origin(annotation)
                            )
                    if field.verbose_name:
                        data["verbose_name"][name] = field.verbose_name
                    if field.default is not None:
                        data["default"][name] = field.default
                    if not field.null:
                        data["notnull"].append(name)
                    if not field.blank:
                        data["notblank"].append(name)
                    if field.desc:
                        data["description"][name] = field.desc
            return data

        def wrapper(class_: T) -> T:
            if self.get_class_name(class_) in self.custom_classes_names:
                raise ClassAlreadyInitialized(
                    f"Class {self.get_class_name(class_)} already exists"
                )

            meta = generate_meta_data(class_)
            c: _customclass = _customclass(
                name or class_.__name__, class_, meta, from_data, to_data
            )
            self.custom_classes_names.append(c.classname)
            self.custom_classes.append(c)
            setattr(self, c.classname, c)
            return class_

        if class_:
            return wrapper(class_)
        return wrapper

    def remove_class(self, classname: str) -> None:
        delattr(self, classname)
        self.custom_classes.pop(self.custom_classes_names.index(classname))
        self.custom_classes_names.remove(classname)

    def set_recursion_limit(self, limit: int = 1000) -> None:
        sys.setrecursionlimit(limit)

    def get_class_name(self, class_: type) -> str:
        for customclass in self.custom_classes:
            if customclass.class_ is class_:
                return customclass.classname
        return class_.__name__

    def get_class(self, classname: str) -> Optional[_customclass]:
        for customclass in self.custom_classes:
            if customclass.classname == classname:
                return customclass
        return None

    def export_config(self, file: str = "config.fxdc"):
        """
        Exports All The MetaData Of Every Class Loaded Into The Config
        Converts To a FxDC String and Writes to `config.fxdc`
        """
        config = {}
        for customclass in self.custom_classes:
            print(f"Exporting {customclass.classname} to config")
            if any(len(x) > 0 for x in customclass.meta_data.values()):
                print(f"Meta Data: {customclass.meta_data}")
                meta = customclass.meta_data.copy()
                meta["typechecking"] = {}
                if len(customclass.meta_data["typechecking"]) > 0:
                    print("TypeChecking: ", customclass.meta_data["typechecking"])
                    for key, value in customclass.meta_data["typechecking"].items():
                        meta["typechecking"][key] = value.__name__

                config["Config_"+customclass.classname] = meta

        if not config:
            raise NoConfigFound("No classes to export in the config")
        from fxdc import dumps
        config_str = "!CONFIG FILE!\n\n" + dumps(config)
        with open(file, "w") as f:
            f.write(config_str)
        print("Config exported to config.fxdc")
    
    def import_config(self, file: str = "config.fxdc") -> None:
        """
        Imports Config From a FxDC File
        Reads the file and adds the classes to the config
        """
        from fxdc.read import loads
        if not os.path.exists(file):
            raise NoConfigFound("Config Not Found")
        with open(file, "r") as f:
            data = f.read()
        if not data.startswith("!CONFIG FILE!"):
            raise NoConfigFound("Invalid config file format")
        
        data:dict[str, dict] = loads(data).original
        for classname, meta_data in data.items():
            classname = classname[7:]
            if classname not in self.custom_classes_names:
                raise ClassNotLoaded(
                    f"Class {classname} is not loaded in the config"
                )
            customclass = self.get_class(classname)
            meta = meta_data.copy()
            meta["typechecking"] = {}
            if meta_data.get("typechecking", None):
                for key, value in meta_data["typechecking"].items():
                    if value in DEFAULT_TYPES:
                        class_ = DEFAULT_TYPES[value]
                    else:
                        loadedclass = self.get_class(value)
                        if not loadedclass:
                            raise ClassNotLoaded(
                                f"The Class {value} is not loaded into the config"
                            )
                        class_ = loadedclass.class_
                    meta["typechecking"][key] = class_
            customclass.meta_data = meta
                    
        print(f"Config imported from {file}")
    


Config = _config()
