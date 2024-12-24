from io import TextIOWrapper
from .parsedata.fxdcobject import FxDCObject
from .writedata import ParseObject
from .exceptions import FileNotWritable, InvalidExtension

def dumps(data: object) -> str:
    """Dump the FXDC object to the string

    Args:
        data (object): Any Class Object
    Returns:
        str: Returns the string from the object
    """
    if type(data) != dict:
        data = {"main": data}
    parser = ParseObject(data)
    return parser.parse()


def dump(data: object, file: str | TextIOWrapper) -> None:
    """Dump the FXDC object to the file

    Args:
        data (object): Any Class Object
        file (str): File Path
    Returns:
        None
    Raises:
        FileNotWritable: If the file is not writable or permission denied
        InvalidExtension: If the file extension is not `.fxdc`
    """
    if isinstance(file, TextIOWrapper):
        try:
            file.write(dumps(data))
        except Exception as e:
            raise FileNotWritable(f"Error while writing the file: {e}")
    else:
        if not file.endswith(".fxdc"):
            raise InvalidExtension("Invalid Fxdc file")
        with open(file, "w") as f:
            f.write(dumps(data))

