from io import TextIOWrapper

from .config import Config
from .exceptions import FileNotReadable, InvalidExtension
from .misc import debug
from .parsedata import FxDCObject, Parser
from .parsedata.lexer import Lexer


def loads(data: str) -> FxDCObject:
    """Load the FXDC object from the string

    Args:
        data (str): string data of FedxD Data Container

    Raises:
        TypeError: if the data is not a string

    Returns:
        object: Returns the object from the string
    """
    if not isinstance(data, str):
        raise TypeError("Invalid data type. Required string")

    lexer = Lexer(data, Config.custom_classes_names)
    tokens = lexer.make_tokens()
    debug("Tokens:", tokens)
    parser = Parser(tokens)
    obj = parser.parse()
    debug("Object:", obj.__dict__)
    return obj


def load(file: TextIOWrapper | str) -> FxDCObject:
    """Load the FXDC object from the file

    Args:
        file (TextIOWrapper | str): file path or file object returned from `open()` function

    Raises:
        InvalidExtension: If the file extension is not `.fxdc`
        FileNotFoundError: If the file is not found
        FileNotReadable: If the file is not readable or permission denied
        TypeError: If the argument is not a string or file object

    Returns:
        object: Returns the object from the file
    """
    if isinstance(file, str):
        if not file.endswith(".fxdc"):
            raise InvalidExtension("Invalid Fxdc file")
        try:
            file = open(file, "r")
        except FileNotFoundError:
            raise FileNotFoundError("File not found")
        except PermissionError:
            raise FileNotReadable("Permission denied")
    elif not isinstance(file, TextIOWrapper):
        raise TypeError("Invalid Argument")

    data = file.read()
    if not isinstance(data, str):
        raise TypeError("Invalid data type. Required string")

    return loads(data)
