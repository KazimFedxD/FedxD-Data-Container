import json
from typing import Any


class FxDCObject:
    """
    FxDC Object class\n
    Contains All the Data Extracted from the FxDC File
    """

    def to_dict(self):
        """
        Convert the Object to a Dictionary
        """
        return self.__dict__

    def to_json(self):
        """
        Convert the Object to a JSON
        """
        return json.dumps(self.__dict__, indent=4)

    def __getitem__(self, key: str):
        return self.__getattribute__(key)

    def __setitem__(self, key: str, value: Any):
        self.__setattr__(key, value)

    def __contains__(self, key: str):
        return key in self.__dict__

    def __iter__(self):
        return iter(self.__dict__.items())

    def get_original(self) -> object:
        """
        Get the Original Object
        """
        try:
            return self.main
        except AttributeError:
            return self.__dict__
