from typing import Any

import json


class FxDCObject:
    """
    FxDC Object class
    -----------------
    Contains All the Data Extracted from the FxDC File
    """

    
    def dict(self):
        """
        Convert the Object to a Dictionary
        """
        return self.__dict__


    def json(self):
        """
        Convert the Object to a JSON
        """
        return json.dumps(self.__dict__, indent=4)

    def __getitem__(self, key: str):
        return getattr(self, key)

    def __setitem__(self, key: str, value: Any):
        setattr(self, key, value)
        
    def __contains__(self, key: str):
        return hasattr(self, key)

    def __iter__(self):
        return iter(self.__dict__.items())

    @property
    def original(self) -> object:
        """
        Get the Original Object
        """
        if len(self.__dict__) == 0:
            raise ValueError("The Object is Empty")
        if len(self.__dict__) == 1:
            if "main" in self.__dict__:
                return self.__dict__["main"]
        return self.__dict__
    
    @original.setter
    def original(self, value: Any):
        """
        Set the Original Object
        """
        self.__dict__["original"] = value
