from ..config import Config
from typing import Any
from _collections_abc import dict_items, dict_keys, dict_values

def dict_items_from_data(data: list[tuple[Any, Any]]) -> dict_items[Any, Any]:
    return {k: v for k, v in data}.items()

def dict_keys_from_data(data: list[Any]) -> dict_keys[Any, Any]:
        return {k: None for k in data}.keys()

def dict_values_from_data(data: list[Any]) -> dict_values[Any, Any]:
        k = range(len(data))
        return {k[i]: data[i] for i in k}.values()

def range_from_data(data: list[int]) -> range:
        start = data[0]
        stop = data[-1]
        step = data[1] - data[0]
        return range(start, stop, step)

def zip_from_data(data: list[tuple[Any, Any]]) -> zip[tuple[Any, Any]]:
        n_lists = len(data[0])
        n_items = len(data)
        lists:list[list[Any]] = []
        for i in range(n_lists):
                l:list[Any] = []
                for j in range(n_items):
                        l.append(data[j][i])
                lists.append(l)
        return zip(*lists)

def map_from_data(data: list[Any]) -> map[Any]:
        return map(lambda x: x, data)

def filter_from_data(data: list[Any]) -> filter[Any]:
        return filter(lambda x: True if x else False, data)

def enumerate_from_data(data: list[tuple[int, Any]]) -> enumerate[Any]:
        sorted(data, key=lambda x: x[0])
        start = data[0][0]
        data = [x[1] for x in data]
        return enumerate(data, start=start)

def load():
        Config.add_class("set", class_=set)
        Config.add_class("dict_items", class_=dict_items, from_data=dict_items_from_data)
        Config.add_class("dict_keys", class_=dict_keys, from_data=dict_keys_from_data)
        Config.add_class("dict_values", class_=dict_values, from_data=dict_values_from_data)
        Config.add_class("range", class_=range, from_data=range_from_data)
        Config.add_class("zip", class_=zip, from_data=zip_from_data)
        Config.add_class("map", class_=map, from_data=map_from_data)
        Config.add_class("filter", class_=filter, from_data=filter_from_data)
        Config.add_class("enumerate", class_=enumerate, from_data=enumerate_from_data)
        Config.add_class("bytearray", class_=bytearray)
        Config.add_class("bytes", class_=bytes)
        

        


