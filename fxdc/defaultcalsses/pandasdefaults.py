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
        return json.loads(data_frame.to_json())

    def data_frame_from_data(**data: Any) -> DataFrame:
        return pd.read_json(json.dumps(data))

    def load() -> None:
        Config.add_class(
            "DataFrame",
            class_=DataFrame,
            to_data=data_frame_to_data,
            from_data=data_frame_from_data,
        )
