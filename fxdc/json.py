from __future__ import annotations
from .parsedata.parsedata import Parser
from .parsedata.lexer import Lexer
from .config import Config

def fxdc_to_json(fxdc_string: str):
    """Convert FedxD string to JSON string

    Args:
        fxdc_string (str): FedxD string to convert
    """
    lexer = Lexer(fxdc_string, Config.custom_classes_names)
    tokens = lexer.make_tokens()
    
    parser = Parser(tokens)
    fxdc_obj = parser.parse(preserve_type=False)
    return fxdc_obj.json()

