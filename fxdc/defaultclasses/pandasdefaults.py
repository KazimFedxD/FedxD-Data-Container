from typing import Any

from ..config import Config
from ..misc import debug

try:
    import pandas as pd
except ImportError:
    pd = None
    debug("Pandas not found, Pandas Default Classes will not work")

if pd:
    import json

    from pandas import DataFrame

    def data_frame_to_data(data_frame: DataFrame) -> dict[str, Any]:
        data = data_frame.to_dict()
        returndata:dict[str, Any] = {}
        for key, value in data.items():
            returndata[key] = list(value.values())
        return returndata

    def data_frame_from_data(**data: Any) -> DataFrame:
        inputdata: dict[str, Any] = {}
        for key, value in data.items():
            inputdata[key] = {k: v for k, v in enumerate(value)}
        return DataFrame.from_dict(inputdata)

    def load() -> None:
        Config.add_class(
            name="DataFrame",
            class_=DataFrame,
            to_data=data_frame_to_data,
            from_data=data_frame_from_data,
        )
