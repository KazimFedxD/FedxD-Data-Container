from .config import Config
from .defaultcalsses import load_default_classes
from .json import fxdc_to_json as to_json
from .parsedata import *
from .read import load, loads
from .write import dump, dumps
from .writedata import ParseObject

__all__ = [
    "load",
    "loads",
    "FxDCObject",
    "Config",
    "Parser",
    "ParseObject",
    "dumps",
    "dump",
    "to_json",
]

load_default_classes()
