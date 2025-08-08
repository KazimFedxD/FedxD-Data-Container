from types import NoneType
from typing import Any

from fxdc.exceptions import InvalidJSONKey

from ..config import Config
from ..misc import debug


class ParseObject:
    def __init__(self, data: object) -> None:
        self.data = data

    def convertobject(
        self, data: object = None
    ) -> tuple[str, dict[str, Any] | Any, Any]:
        """Convert the object to string

        Returns:
            str: Returns the string from the object
        """
        type_ = Config.get_class_name(data.__class__)
        class_ = None
        descriptions: dict[str, str] = {}
        debug(type_)
        try:
            class_ = getattr(Config, type_)
            convertedobject, descriptions = class_.return_data(data)
        except:
            try:
                convertedobject = data.__todata__()
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

        debug("Converted Object:", convertedobject, "Type:", type_)
        return type_, convertedobject, descriptions

    def parse(
        self,
        tab_count: int = 0,
        dataobject: object = None,
        descs: dict[str, str] = None,
    ) -> str:
        """Parse the object to string

        Returns:
            str: Returns the string from the object
        """
        str_ = ""
        type_, data_, descriptions = self.convertobject(dataobject or self.data)
        for obj in data_:
            if descs:
                desc = descs.get(obj, None)
            else:
                desc = None
            debug("Object:", obj, "Description:", desc)
            if obj.isnumeric():
                raise InvalidJSONKey("JSON Key cannot be an integer")
            type_, data, descriptions_ = self.convertobject(data_[obj])

            if isinstance(data, dict):
                if len(data) == 0:
                    continue
                objstr = (
                    "\t" * tab_count + f"{obj}|{type_}({desc}):\n"
                    if desc
                    else "\t" * tab_count + f"{obj}|{type_}:\n"
                )
                objstr += self.parse(tab_count + 1, data, descriptions_)
            elif isinstance(data, list):
                if len(data) == 0:
                    continue
                objstr = (
                    "\t" * tab_count + f"{obj}|{type_}({desc}):\n"
                    if desc
                    else "\t" * tab_count + f"{obj}|{type_}:\n"
                )
                objstr += self.parse_list(data, tab_count + 1)
            else:
                if isinstance(data, str):
                    data = f'"{data}"'
                if isinstance(data, (NoneType, bool)):
                    data = f'"{data}"'
                    type_ = "bool"
                objstr = (
                    "\t" * tab_count + f"{obj}|{type_}({desc})={data}\n"
                    if desc
                    else "\t" * tab_count + f"{obj}|{type_}={data}\n"
                )
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
            type_, data, descriptions = self.convertobject(obj)
            if isinstance(data, dict):
                if len(data) == 0:
                    continue
                debug("Data:", data)
                objstr = "\t" * tab_count + f"{type_}:\n"
                objstr += self.parse(tab_count + 1, data, descriptions)
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
