import sys


class _config:
    def __init__(self) -> None:
        self.custom_classes: list[str] = []
        self.debug__: bool = False

    def add_class(self, classname: str, class_: object):
        setattr(self, classname, class_)
        self.custom_classes.append(classname)

    def remove_class(self, classname: str):
        delattr(self, classname)
        self.custom_classes.remove(classname)

    def set_recursion_limit(self, limit: int = 5000):
        sys.setrecursionlimit(limit)

    def get_class_name(self, class_: type) -> str:
        for class_name in self.custom_classes:
            if getattr(self, class_name) == class_:
                return class_name
        return class_.__name__

Config = _config()
Config.set_recursion_limit()
