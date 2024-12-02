from fxdc.config import Config

def int_to_alphabetic(n:int) -> str:
    """Convert an integer to an alphabetical sequence."""
    result = ""
    while n > 0:
        n -= 1  # Adjust because 'a' starts at 1, not 0
        remainder = n % 26
        result = chr(97 + remainder) + result  # 97 is the ASCII code for 'a'
        n //= 26
    return result

def debug(*values:object, sep:str=" ", end:str="\n") -> None:
    if Config.debug__:
        print(*values, sep=sep, end=end)