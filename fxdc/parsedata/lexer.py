from typing import Optional
from ..exceptions import InvalidData


## TOKENS


class Token:
    def __init__(
        self, type: str, value: Optional[str] = None, line: Optional[int] = None
    ):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return (
            f"{self.type}" + f":{self.value}" if self.value != None else f"{self.type}"
        )


TT_NUMBER = "NUMBER"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_EOF = "EOF"
TT_NEWLINE = "NEWLINE"
TT_INDENT = "INDENT"
TT_DEVIDER = "DEVIDER"
TT_EQUAL = "EQUAL"
TT_COLON = "COLON"

NUMS = "0123456789"
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
LETTERS_DIGITS = LETTERS + NUMS


KEYWORDS = [
    "str",
    "int",
    "float",
    "bool",
    "list",
    "dict",
]


class Lexer:
    def __init__(self, text: str, classes: list[str] = []):
        self.text = text
        self.pos = -1
        self.line = 1
        self.current_char = None
        self.KEYWORDS = KEYWORDS + classes
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self) -> list[Token]:
        tokens: list[Token] = []
        while self.current_char != None:
            if self.current_char in " \t":
                tokens.append(Token(TT_INDENT, line=self.line))
                self.advance()
            elif self.current_char in "\n":
                self.line += 1
                tokens.append(Token(TT_NEWLINE, line=self.line))
                self.advance()
            elif self.current_char in NUMS+"-":
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char in "'\"":
                tokens.append(self.make_string())
            elif self.current_char in "=":
                tokens.append(Token(TT_EQUAL, line=self.line))
                self.advance()
            elif self.current_char in ":":
                tokens.append(Token(TT_COLON, line=self.line))
                self.advance()
            elif self.current_char in "|":
                tokens.append(Token(TT_DEVIDER, line=self.line))
                self.advance()
            elif self.current_char in "#":
                self.skip_comments()

            else:
                char = self.current_char
                self.advance()
                raise InvalidData(f"Invalid character {char} at line {self.line}")

        tokens.append(Token(TT_EOF, line=self.line))
        return tokens

    def make_number(self) -> Token:
        num_str = ""
        dot_count = 0
        while self.current_char != None and self.current_char in NUMS + ".-":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            elif self.current_char == "-":
                if len(num_str) > 0:
                    raise InvalidData(f"Invalid character '-' at line {self.line}")
                num_str += "-"
            else:
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_NUMBER, num_str, line=self.line)
        else:
            return Token(TT_FLOAT, num_str, line=self.line)

    def make_identifier(self) -> Token:
        id_str = ""
        while self.current_char != None and self.current_char in LETTERS_DIGITS + ".":
            id_str += self.current_char
            self.advance()
        if id_str in self.KEYWORDS:
            return Token(TT_KEYWORD, id_str, line=self.line)
        return Token(TT_IDENTIFIER, id_str, line=self.line)

    def make_string(self) -> Token:
        quote = self.current_char
        escapeseq = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            "b": "\b",
            "f": "\f",
            "\\": "\\",
            "'": "'",
            '"': '"',
        }
        self.advance()
        string = ""
        while self.current_char != None and self.current_char != quote:
            if self.current_char == "\\":
                self.advance()
                if self.current_char in escapeseq:
                    string += escapeseq[self.current_char]
                else:
                    string += "\\" + self.current_char
            else:
                string += self.current_char
            self.advance()
        self.advance()
        return Token(TT_STRING, string, line=self.line)

    def skip_comments(self):
        while self.current_char != "\n":
            self.advance()
        self.advance()
