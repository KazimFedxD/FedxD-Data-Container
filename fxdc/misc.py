from .config import Config

def debug(*values: object, sep: str = " ", end: str = "\n") -> None:
    if Config.debug__:
        print(*values, sep=sep, end=end)
