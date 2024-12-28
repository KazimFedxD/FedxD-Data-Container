from types import NoneType
from typing import Any, Optional

from fxdc.exceptions import InvalidJSONKey
from ..misc import debug
from ..config import Config

class ParseObject:
    def __init__(self, data: object):
        self.data = data

    def convertobject(
        self, data: object = None
    ) -> tuple[str, dict[str, Any] | Any]:
        """Convert the object to string

        Returns:
            str: Returns the string from the object
        """
        type_ = Config.get_class_name(data.__class__)
        try:
            convertedobject = getattr(Config, type_).return_data(data)
        except:

            try:
                convertedobject = data.to_data()
            except AttributeError:
                try:
                    convertedobject = data.__dict__
                except AttributeError or TypeError:
                    try:
                        if isinstance(data, (list, dict, str)):
                            raise TypeError()
                        iterable = iter(data)
                        convertedobject = [i for i in iterable]
                    except TypeError:
                        convertedobject = data

        debug("Converted Object:", convertedobject, 'Type:', type_)
        return type_, convertedobject

    def parse(self, tab_count: int = 0, dataobject: object = None) -> str:
        """Parse the object to string

        Returns:
            str: Returns the string from the object
        """
        str_ = ""
        _, data_ = self.convertobject(dataobject or self.data)
        for obj in data_:
            debug("Object:", obj)
            if obj.isnumeric():
                raise InvalidJSONKey("JSON Key cannot be an integer")
            type_, data = self.convertobject(data_[obj])
            if isinstance(data, dict):
                if len(data) == 0:
                    continue
                objstr = "\t" * tab_count + f"{obj}|{type_}:\n"
                objstr += self.parse(tab_count + 1, data)
            elif isinstance(data, list):
                if len(data) == 0:
                    continue
                objstr = "\t" * tab_count + f"{obj}|{type_}:\n"
                objstr += self.parse_list(data, tab_count + 1)
            else:
                if isinstance(data, str):
                    data = f'"{data}"'
                if isinstance(data,  (NoneType, bool)):
                    data = f'"{data}"'
                    type_ = "bool"
                objstr = "\t" * tab_count + f"{obj}|{type_}={data}\n"
            str_ += objstr
            debug("Object String:", objstr)
        return str_

    def parse_list(self, datalist: list[Any], tab_count: int = 1) -> str:
        """Parse the object to string

        Returns:
            str: Returns the string from the object
        """
        str_ = ""
        for i, obj in enumerate(datalist, 1):
            type_, data = self.convertobject(obj)
            if isinstance(data, dict):
                if len(data) == 0:
                    continue
                debug("Data:", data)
                objstr = "\t" * tab_count + f"{type_}:\n"
                objstr += self.parse(tab_count + 1, data)
            elif isinstance(data, list):
                if len(data) == 0:
                    continue
                objstr = "\t" * tab_count + f"{type_}:\n"
                objstr += self.parse_list(data, tab_count + 1)
            else:
                if isinstance(data, str):
                    data = f'"{data}"'
                if isinstance(data, (NoneType, bool)):
                    data = f'"{data}"'
                    type_ = "bool"
                objstr = "\t" * tab_count + f"{type_}={data}\n"
            str_ += objstr
        return str_
