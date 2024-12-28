from typing import Any
from .lexer import *
from .fxdcobject import FxDCObject
from ..exceptions import InvalidData
from ..config import Config
from ..misc import debug

## NODES

BASIC_TYPES = [
    "str",
    "int",
    "bool",
    "list",
    "dict",
]


class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        debug("Current Token:", self.current_token, " At Position:", self.pos)
        return self.current_token

    def get_indent_count(self):
        count = 0
        while self.current_token.type == TT_INDENT:
            count += 1
            self.advance()

        return count

    def parse(self):
        obj = FxDCObject()
        while self.current_token.type != TT_EOF:
            while self.current_token.type == TT_NEWLINE:
                self.advance()
            if self.current_token.type == TT_INDENT:
                self.advance()
                if self.current_token.type not in (TT_EOF, TT_NEWLINE):
                    raise InvalidData(f"Unexpected indent")
            if self.current_token.type == TT_EOF:
                break
            if self.current_token.type != TT_IDENTIFIER:
                raise InvalidData(
                    f"Expected identifier, got {self.current_token} at line {self.current_token.line}"
                )
            key = self.current_token.value
            type_ = None
            self.advance()
            self.get_indent_count()
            if self.current_token.type == TT_DEVIDER:
                self.advance()
                self.get_indent_count()
                if self.current_token.type != TT_KEYWORD:
                    raise InvalidData(
                        f"Expected keyword class, got {self.current_token} at line {self.current_token.line}\nMake sure you have imported the class in the config file"
                    )
                type_ = self.current_token.value
                self.advance()
            self.get_indent_count()
            if self.current_token.type not in (TT_EQUAL, TT_COLON):
                raise InvalidData(
                    f"Expected equal sign/colon, got {self.current_token} at line {self.current_token.line}"
                )

            if self.current_token.type == TT_COLON:
                self.advance()
                self.get_indent_count()
                if self.current_token.type != TT_NEWLINE:
                    raise InvalidData(
                        f"Expected new line, got {self.current_token} at line {self.current_token.line}"
                    )
                self.advance()
                indentcount = self.get_indent_count()
                debug(f"Indent Count Of {key}:", indentcount)
                if indentcount == 0:
                    raise InvalidData(
                        f"Expected indented block, got {self.current_token} at line {self.current_token.line}"
                    )
                while self.current_token.type == TT_NEWLINE:
                    self.advance()
                    self.get_indent_count()
                if self.current_token.type == TT_IDENTIFIER:
                    newobj = self.parse_indented(indentcount)
                    if not type_ or type_ == "dict":
                        setattr(obj, key, newobj.__dict__)
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        try:
                            setattr(obj, key, class_(**newobj.__dict__))
                        except TypeError:
                            raise InvalidData(f"Invalid arguments for class {type_}")
                else:
                    newobj = self.parse_list(indentcount)
                    if not type_ or type_ == "list":
                        setattr(obj, key, newobj)
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        try:
                            setattr(obj, key, class_(newobj))
                        except TypeError:
                            raise InvalidData(f"Invalid arguments for class {type_}")
                
                            
            else:
                self.advance()
                self.get_indent_count()
                if self.current_token.type not in (TT_STRING, TT_NUMBER, TT_FLOAT):
                    raise InvalidData(
                        f"Expected value, got {self.current_token} at line {self.current_token.line}"
                    )

                value = self.current_token.value
                if type_:
                    if type_ == "str":
                        if not self.current_token.type == TT_STRING:
                            raise InvalidData(
                                f"Expected string, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        value = str(value)
                    elif type_ == "int":
                        if not self.current_token.type == TT_NUMBER:
                            raise InvalidData(
                                f"Expected number, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        try:
                            value = int(value)
                        except ValueError:
                            raise InvalidData(f"Invalid value for int type")
                    elif type_ == "float":
                        if not self.current_token.type == TT_FLOAT:
                            raise InvalidData(
                                f"Expected float, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        try:
                            value = float(value)
                        except ValueError:
                            raise InvalidData(f"Invalid value for float type")
                    elif type_ == "bool":
                        if self.current_token.type in ("True", 1):
                            value = True
                        elif self.current_token.type in ("False", 0):
                            value = False
                        elif self.current_token.value in ("None", "Null"):
                            value = None
                        else:
                            raise InvalidData(f"Invalid value for bool type")
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        if self.current_token.type == TT_STRING:
                            value = str(value)
                        elif self.current_token.type == TT_NUMBER:
                            value = int(value)
                        elif self.current_token.type == TT_FLOAT:
                            value = float(value)
                        else:
                            raise InvalidData(f"Invalid value for basic type")
                        value = class_(value)
                else:
                    if self.current_token.type == TT_STRING:
                        value = str(value)
                    elif self.current_token.type == TT_NUMBER:
                        value = int(value)
                    elif self.current_token.type == TT_FLOAT:
                        value = float(value)
                    else:
                        raise InvalidData(f"Invalid value for basic type")
                setattr(obj, key, value)
                self.advance()
                self.get_indent_count()
        return obj

    def parse_indented(self, indentcount: int) -> FxDCObject:
        obj = FxDCObject()
        self.indent = indentcount
        while self.current_token.type != TT_EOF or self.indent >= indentcount:
            while self.current_token.type == TT_NEWLINE:
                self.advance()
                self.get_indent_count()
            if self.current_token.type == TT_EOF:
                break
            if self.indent < indentcount:
                break
            if self.current_token.type != TT_IDENTIFIER:
                raise InvalidData(
                    f"Expected identifier, got {self.current_token} at line {self.current_token.line}"
                )
            key = self.current_token.value
            type_ = None
            self.advance()
            self.get_indent_count()
            if self.current_token.type == TT_DEVIDER:
                self.advance()
                if self.current_token.type != TT_KEYWORD:
                    raise InvalidData(
                        f"Expected keyword class, got {self.current_token} at line {self.current_token.line}"
                    )
                type_ = self.current_token.value
                self.advance()
                self.get_indent_count()

            if self.current_token.type not in (TT_EQUAL, TT_COLON):
                raise InvalidData(
                    f"Expected equal sign/colon, got {self.current_token} at line {self.current_token.line}"
                )

            if self.current_token.type == TT_COLON:
                self.advance()
                self.get_indent_count()
                if self.current_token.type != TT_NEWLINE:
                    raise InvalidData(
                        f"Expected new line, got {self.current_token} at line {self.current_token.line}"
                    )
                self.advance()
                self.indent = self.get_indent_count()
                if self.indent <= indentcount:
                    raise InvalidData(
                        f"Expected indented block, got {self.current_token} at line {self.current_token.line}"
                    )
                while self.current_token.type == TT_NEWLINE:
                    self.advance()
                    self.get_indent_count()
                if self.current_token.type == TT_IDENTIFIER:
                    newobj = self.parse_indented(self.indent)
                    if not type_ or type_ == "dict":
                        setattr(obj, key, newobj.__dict__)
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        try:
                            setattr(obj, key, class_(**newobj.__dict__))
                        except TypeError:
                            raise InvalidData(f"Invalid arguments for class {type_}")
                else:
                    newobj = self.parse_list(self.indent)
                    if not type_ or type_ == "list":
                        setattr(obj, key, newobj.__dict__)
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        try:
                            setattr(obj, key, newobj.__dict__)
                        except TypeError:
                            raise InvalidData(f"Invalid arguments for class {type_}")
            else:
                self.advance()
                self.get_indent_count()
                if self.current_token.type not in (TT_STRING, TT_NUMBER, TT_FLOAT):
                    raise InvalidData(
                        f"Expected value, got {self.current_token} at line {self.current_token.line}"
                    )

                value = self.current_token.value
                if type_:
                    if type_ == "str":
                        if not self.current_token.type == TT_STRING:
                            raise InvalidData(
                                f"Expected string, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        value = str(value)
                    elif type_ == "int":
                        if not self.current_token.type == TT_NUMBER:
                            raise InvalidData(
                                f"Expected number, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        try:
                            value = int(value)
                        except ValueError:
                            raise InvalidData(f"Invalid value for int type")
                    elif type_ == "float":
                        if not self.current_token.type == TT_FLOAT:
                            raise InvalidData(
                                f"Expected float, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        try:
                            value = float(value)
                        except ValueError:
                            raise InvalidData(f"Invalid value for float type")
                    elif type_ == "bool":
                        if self.current_token.type in ("True", 1):
                            value = True
                        elif self.current_token.type in ("False", 0):
                            value = False
                        elif self.current_token.value in ("None", "Null"):
                            value = None
                        else:
                            raise InvalidData(f"Invalid value for bool type")
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        if self.current_token.type == TT_STRING:
                            value = str(value)
                        elif self.current_token.type == TT_NUMBER:
                            value = int(value)
                        elif self.current_token.type == TT_FLOAT:
                            value = float(value)
                        else:
                            raise InvalidData(f"Invalid value for basic type")
                        value = class_(value)
                else:
                    if self.current_token.type == TT_STRING:
                        value = str(value)
                    elif self.current_token.type == TT_NUMBER:
                        value = int(value)
                    elif self.current_token.type == TT_FLOAT:
                        value = float(value)
                    else:
                        raise InvalidData(f"Invalid value for basic type")
                setattr(obj, key, value)
                self.advance()
                self.get_indent_count()
                if (
                    self.current_token.type != TT_NEWLINE
                    and self.current_token.type != TT_EOF
                ):
                    raise InvalidData(
                        f"Expected new line, got {self.current_token} at line {self.current_token.line}"
                    )
                self.advance()
                self.indent = self.get_indent_count()
                debug(f"Indent Count Of {key}:", self.indent, "Expected:", indentcount)
                if self.indent < indentcount:
                    break
        return obj
    
    def parse_list(self, indentcount:int) -> list[Any]:
        l:list[Any] = []
        self.indent = indentcount
        while self.current_token.type != TT_EOF or self.indent >= indentcount:
            type_ = None
            while self.current_token.type == TT_NEWLINE:
                self.advance()
                self.get_indent_count()
            if self.current_token.type == TT_EOF:
                break
            if self.indent < indentcount:
                break
            if self.current_token.type == TT_KEYWORD:
                type_ = self.current_token.value
                self.advance()
                self.get_indent_count()
            if self.current_token.type not in (TT_EQUAL, TT_COLON):
                raise InvalidData(
                    f"Expected equal sign/colon, got {self.current_token} at line {self.current_token.line}"
                )
            if self.current_token.type == TT_COLON:
                self.advance()
                self.get_indent_count()
                if self.current_token.type != TT_NEWLINE:
                    raise InvalidData(
                        f"Expected new line, got {self.current_token} at line {self.current_token.line}"
                    )
                self.advance()
                self.indent = self.get_indent_count()
                if self.indent <= indentcount:
                    raise InvalidData(
                        f"Expected indented block, got {self.current_token} at line {self.current_token.line}"
                    )
                
                while self.current_token.type == TT_NEWLINE:
                    self.advance()
                    self.get_indent_count()
                if self.current_token.type == TT_IDENTIFIER:
                    newobj = self.parse_indented(self.indent)
                    if not type_ or type_ == "dict":
                        l.append(newobj.__dict__)
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        try:
                            l.append(class_(**newobj.__dict__))
                        except TypeError:
                            raise InvalidData(f"Invalid arguments for class {type_}")
                else:
                    newobj = self.parse_list(self.indent)
                    if not type_ or type_ == "list":
                        l.append(newobj)
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        try:
                            l.append(class_(newobj))
                        except TypeError:
                            raise InvalidData(f"Invalid arguments for class {type_}")
            else:
                self.advance()
                self.get_indent_count()
                if self.current_token.type not in (TT_STRING, TT_NUMBER, TT_FLOAT):
                    raise InvalidData(
                        f"Expected value, got {self.current_token} at line {self.current_token.line}"
                    )

                value = self.current_token.value
                if type_:
                    if type_ == "str":
                        if not self.current_token.type == TT_STRING:
                            raise InvalidData(
                                f"Expected string, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        value = str(value)
                    elif type_ == "int":
                        if not self.current_token.type == TT_NUMBER:
                            raise InvalidData(
                                f"Expected number, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        try:
                            value = int(value)
                        except ValueError:
                            raise InvalidData(f"Invalid value for int type")
                    elif type_ == "float":
                        if not self.current_token.type == TT_FLOAT:
                            raise InvalidData(
                                f"Expected float, got {self.current_token.type} at line {self.current_token.line}"
                            )
                        try:
                            value = float(value)
                        except ValueError:
                            raise InvalidData(f"Invalid value for float type")
                    elif type_ == "bool":
                        if self.current_token.value in ("True", "1"):
                            value = True
                        elif self.current_token.value in ("False", "0"):
                            value = False
                        elif self.current_token.value in ("None", "Null"):
                            value = None
                        else:
                            raise InvalidData(f"Invalid value for bool type")
                    else:
                        class_ = getattr(Config, type_, None)
                        if not class_:
                            raise InvalidData(f"Invalid class type {type_}")
                        if self.current_token.type == TT_STRING:
                            value = str(value)
                        elif self.current_token.type == TT_NUMBER:
                            value = int(value)
                        elif self.current_token.type == TT_FLOAT:
                            value = float(value)
                        else:
                            raise InvalidData(f"Invalid value for basic type")
                        value = class_(value)
                else:
                    if self.current_token.type == TT_STRING:
                        value = str(value)
                    elif self.current_token.type == TT_NUMBER:
                        value = int(value)
                    elif self.current_token.type == TT_FLOAT:
                        value = float(value)
                    else:
                        raise InvalidData(f"Invalid value for basic type")
                l.append(value)
                self.advance()
                self.get_indent_count()
                if (
                    self.current_token.type != TT_NEWLINE
                    and self.current_token.type != TT_EOF
                ):
                    raise InvalidData(
                        f"Expected new line, got {self.current_token} at line {self.current_token.line}"
                    )
                self.advance()
                self.indent = self.get_indent_count()
                debug(f"Indent Count Of List:", self.indent, "Expected:", indentcount)
                if self.indent < indentcount:
                    break
        return l