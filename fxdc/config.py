import sys
from typing import Any, Callable, Optional

class _customclass:
    def __init__(self,
                classname: str,
                class_: type,
                from_data: Optional[Callable[..., object]]=None,
                to_data: Optional[Callable[..., dict[str, Any]]]=None,
                ) -> None:
        self.classname = classname
        self.class_ = class_
        self.from_data = from_data
        if not from_data:
            if hasattr(class_, "from_data"):
                self.from_data = class_.from_data
        self.to_data = to_data
        if not to_data:
            if hasattr(class_, "to_data"):
                self.to_data = class_.to_data
        

    def __call__(self, *args:Any,**kwargs:Any) -> object:
        if self.from_data:
            return self.from_data(*args, **kwargs)
        return self.class_(*args, **kwargs)
    
    def __repr__(self) -> str:
        return self.classname
    
    def return_data(self, obj: object) -> dict[str, Any] :
        if self.to_data:
            return self.to_data(obj)
        return obj.__dict__
    
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

    def add_class(self, classname:Optional[str]=None,
                  *,  from_data: Optional[Callable[..., object]]=None,
                  to_data: Optional[Callable[..., dict[str, Any]]]=None,
                  class_: Optional[type]=None):
        """Add a custom class to the config

        Args:
            classname (Optional[str], optional): Name For The Class. Defaults to `class_.__name__`.
            from_data (Optional[Callable[..., object]], optional): Function to convert data to class. Defaults to class_.from_data if it exists. or class_.__init__
            to_data (Optional[Callable[..., dict[str, Any]]], optional): Function to convert class to data. Defaults to class_.to_data if it exists. or class_.__dict__
            class_ (Optional[type], optional): Class to add. If not provided, it will return a decorator.
        Returns:
            if Class_ is provided, it will add and return the class
            if class_ is not provided, it will return a decorator to add on top of the class
        
        Usage:
            ```py
            @Config.add_class("MyClass")
            class MyClass:
                def __init__(self, data: dict[str, Any]):
                    self.data = data
            ```
            OR
            ```py
            class MyClass:
                def __init__(self, data: dict[str, Any]):
                    self.data = data
            Config.add_class("MyClass", class_=MyClass)
        """
        def wrapper(class_: type):
            if self.get_class_name(class_) in self.custom_classes_names:
                raise ValueError(f"Class {classname} already exists")
            
            c:_customclass = _customclass(classname or class_.__name__, class_, from_data, to_data)
            self.custom_classes_names.append(c.classname)
            self.custom_classes.append(c)
            setattr(self, c.classname, c)
            return class_

        if class_:
            return wrapper(class_)
        return wrapper
        
    def remove_class(self, classname: str):
        delattr(self, classname)
        self.custom_classes.pop(self.custom_classes_names.index(classname))

    def set_recursion_limit(self, limit: int = 1000):
        sys.setrecursionlimit(limit)

    def get_class_name(self, class_: type) -> str:
        for customclass in self.custom_classes:
            if customclass.class_ == class_:
                return customclass.classname
        return class_.__name__


Config = _config()


