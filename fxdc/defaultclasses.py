from typing import Any, Optional
from .config import Config
from .misc import debug
import json
__all__ = ["load_default_classes"]
try:
    import numpy as np
except ImportError:
    np = None
    debug("Numpy not found, Numpy Default Classes will not work")
try:
    import pandas as pd
except ImportError:
    pd = None
    debug("Pandas not found, Pandas Default Classes will not work")
from datetime import date, datetime, time, timedelta

def load_default_classes():
    
    ## Python Built-in Classes
    def set_to_data(set_: set[Any]) -> list[Any]:
        return list(set_)
    def set_from_data(data: list[Any]) -> set[Any]:
        return set(data)
    Config.add_class("set", class_=set, to_data=set_to_data, from_data=set_from_data)


    

    def date_to_data(date_: date) -> str:
        return str(date_)
    def date_from_data(data: str, *, years: int = 0, months: int = 0, days: int = 0) -> date:
        if data:
            years = int(data.split("-")[0])
            months = int(data.split("-")[1])
            days = int(data.split("-")[2])
        return date(years, months, days)
    Config.add_class("Date", class_=date, to_data=date_to_data, from_data=date_from_data)
    
    def datetime_to_data(datetime_: datetime) -> str:
        return str(datetime_)
    def datetime_from_data(data: str, *, years: int = 0, months: int = 0, days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0, microseconds: int = 0) -> datetime:
        if data:
            years = int(data.split("-")[0])
            months = int(data.split("-")[1])
            days = int(data.split("-")[2].split(" ")[0])
            hours = int(data.split(" ")[1].split(":")[0])
            minutes = int(data.split(" ")[1].split(":")[1])
            seconds = int(data.split(" ")[1].split(":")[2].split(".")[0])
            microseconds = int(data.split(" ")[1].split(":")[2].split(".")[1]) if "." in data.split(" ")[1].split(":")[2] else 0
        return datetime(years, months, days, hours, minutes, seconds, microseconds)
    Config.add_class("DateTime", class_=datetime, to_data=datetime_to_data, from_data=datetime_from_data)

    def time_to_data(time_: time) -> str:
        return str(time_)
    def time_from_data(data: str, *, hours: int = 0, minutes: int = 0, seconds: int = 0, microseconds: int = 0) -> time:
        if data:
            hours = int(data.split(":")[0])
            minutes = int(data.split(":")[1])
            seconds = int(data.split(":")[2].split(".")[0])
            microseconds = int(data.split(":")[2].split(".")[1]) if "." in data.split(":")[2] else 0
        return time(hours, minutes, seconds, microseconds)
    
    Config.add_class("Time", class_=time, to_data=time_to_data, from_data=time_from_data)
    
    def timedelta_to_data(timedelta_: timedelta) -> str:
        return str(timedelta_)
    def timedelta_from_data(data: str, *, days: int = 0, seconds: int = 0, microseconds: int = 0, milliseconds: int = 0, minutes: int = 0, hours: int = 0, weeks: int = 0) -> timedelta:
        if data:
            days = int(data.split("days,")[0])
            hours = int(data.split(",")[1].split(":")[0])
            minutes = int(data.split(",")[1].split(":")[1])
            seconds = int(data.split(",")[1].split(":")[2].split(".")[0])
            microseconds = int(data.split(",")[1].split(":")[2].split(".")[1]) if "." in data.split(",")[1].split(":")[2] else 0
        return timedelta(days, seconds, microseconds, milliseconds, minutes, hours, weeks)
    Config.add_class("TimeDelta", class_=timedelta, to_data=timedelta_to_data, from_data=timedelta_from_data)
    
    if np:
        from numpy import ndarray, matrix
        def nd_array_to_data(nd_array: ndarray[Any, Any]) -> str:
            return str(nd_array)
        def nd_array_from_data(data: str) -> ndarray[Any, Any]:
            return np.array(data)
            
        Config.add_class("NDArray", class_=ndarray, to_data=nd_array_to_data, from_data=nd_array_from_data)
        def matrix_to_data(matrix_: matrix[Any, Any]) -> list:
            return json.loads((str(matrix_).replace(" ", ",")))
        Config.add_class("Matrix", class_=matrix, to_data=matrix_to_data)  
        
    if pd:
        from pandas import DataFrame
        def data_frame_to_data(data_frame: DataFrame) -> str:
            return json.loads(data_frame.to_json())
        def data_frame_from_data(**data:Any) -> DataFrame:
            return pd.read_json(json.dumps(data))
        Config.add_class("DataFrame", class_=DataFrame, to_data=data_frame_to_data, from_data=data_frame_from_data)
