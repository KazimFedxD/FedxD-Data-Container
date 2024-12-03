from typing import Any, Optional
from ..misc import int_to_alphabetic, debug

class ParseObject:
    def __init__(self, data:object):
        self.data = data
    
    def convertobject(self, data:Optional[object]=None) -> tuple[str ,dict[str, Any]|Any]:
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
        return data.__class__.__name__, dict_
    def parse(self, tab_count:int=0, dataobject:object=None) -> str:
        """Parse the object to string
        
        Returns:
            str: Returns the string from the object
        """
        str_ = ""
        _, data_ = self.convertobject(dataobject or self.data)
        for obj in data_:
            debug(obj)
            type_, data = self.convertobject(data_[obj])
            if type(data) == dict:
                objstr = "\t"*tab_count + f"{obj}|{type_}:\n"
                objstr += self.parse(tab_count+1, data)
            elif type(data) == list:
                objstr = "\t"*tab_count + f"{obj}|{type_}:\n"
                objstr += self.parse_list(data, tab_count+1)
            else:
                if type(data) == str:
                    data = f'"{data}"'
                objstr = "\t"*tab_count + f"{obj}|{type_}={data}\n"
            str_ += objstr
            debug(objstr)
        return str_
    
    def parse_list(self, datalist:list[Any], tab_count:int=1) -> str:
        """Parse the object to string
        
        Returns:
            str: Returns the string from the object
        """
        str_ = ""
        for i, obj in enumerate(datalist, 1):
            type_, data = self.convertobject(obj)
            if type(data) == dict:
                objstr = self.parse(tab_count+1)
            elif type(data) == list:
                objstr = self.parse_list(data, tab_count+1)
            else:
                if type(data) == str:
                    data = f'"{data}"'
                objstr = "\t"*tab_count + f"{int_to_alphabetic(i)}|{type_}={data}\n"
            str_ += objstr
        return str_
    
                
    