import sys
from typing import Optional


class _config:
    def __init__(self) -> None:
        self.custom_classes: list[str] = []
        self.debug__: bool = False

    def add_class(self, classname: Optional[str]=None, class_: Optional[type]=None):
        """
        Use:
            Add the class to the Config Object
            Can be used as a decorator or as a function
        Args:
            classname (Optional[str], optional): Class Name. Defaults to None.
            class_ (Optional[type], optional): Class Type. Defaults to None.
        Returns:
            Returns the class after adding to the Config Object
        """
        def wrapper(class_: type):
            if classname:
                setattr(self, classname, class_)
                self.custom_classes.append(classname)
            else:
                setattr(self, class_.__name__, class_)
                self.custom_classes.append(class_.__name__)
            return class_
        if not class_:
            return wrapper
        else:
            return wrapper(class_)
        
        
    def remove_class(self, classname: str):
        delattr(self, classname)
        self.custom_classes.remove(classname)

    def set_recursion_limit(self, limit: int = 1000):
        sys.setrecursionlimit(limit)

    def get_class_name(self, class_: type) -> str:
        for class_name in self.custom_classes:
            if getattr(self, class_name) == class_:
                return class_name
        return class_.__name__



Config = _config()
