from types import NoneType
from typing import Any, Optional
from ..misc import int_to_alphabetic, debug
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
        try:
            dict_ = data.to_data()
        except AttributeError:
            try:
                dict_ = data.__dict__
            except AttributeError:
                dict_ = data
            except SyntaxError:
                dict_ = data
        debug(dict_)
        type_ = Config.get_class_name(data.__class__)
        return type_, dict_

    def parse(self, tab_count: int = 0, dataobject: object = None) -> str:
        """Parse the object to string

        Returns:
            str: Returns the string from the object
        """
        str_ = ""
        _, data_ = self.convertobject(dataobject or self.data)
        for obj in data_:
            debug(obj)
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
            debug(objstr)
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
                objstr = "\t" * tab_count + f"{int_to_alphabetic(i)}|{type_}:\n"
                objstr += self.parse(tab_count + 1, data)
            elif isinstance(data, list):
                if len(data) == 0:
                    continue
                objstr = "\t" * tab_count + f"{int_to_alphabetic(i)}|{type_}:\n"
                objstr += self.parse_list(data, tab_count + 1)
            else:
                if isinstance(data, str):
                    data = f'"{data}"'
                if isinstance(data, (NoneType, bool)):
                    data = f'"{data}"'
                    type_ = "bool"
                objstr = "\t" * tab_count + f"{int_to_alphabetic(i)}|{type_}={data}\n"
            str_ += objstr
        return str_
