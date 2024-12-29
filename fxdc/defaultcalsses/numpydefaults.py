from ..config import Config
from ..misc import debug
from typing import Any
try:
    import numpy as np
except ImportError:
    np = None
    debug("Numpy not found, Numpy Default Classes will not work")

if np:
        import json
        from numpy import ndarray, matrix
        def nd_array_to_data(nd_array: ndarray[Any, Any]) -> str:
            return str(nd_array)
        def nd_array_from_data(data: str) -> ndarray[Any, Any]:
            return np.array(data)
            
        def matrix_to_data(matrix_: matrix[Any, Any]) -> list:
            return json.loads((str(matrix_).replace(" ", ",")))
        
    def load():
        Config.add_class("NDArray", class_=ndarray, to_data=nd_array_to_data, from_data=nd_array_from_data)
        Config.add_class("Matrix", class_=matrix, to_data=matrix_to_data)
