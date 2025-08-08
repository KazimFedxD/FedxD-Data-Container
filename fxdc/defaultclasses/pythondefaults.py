from typing import Any

from _collections_abc import dict_items, dict_keys, dict_values

from ..config import Config


def dict_items_from_data(data: list[tuple[Any, Any]]) -> dict_items:
    return {k: v for k, v in data}.items()


def dict_keys_from_data(data: list[Any]) -> dict_keys:
    return {k: None for k in data}.keys()


def dict_values_from_data(data: list[Any]) -> dict_values:
    k = range(len(data))
    return {k[i]: data[i] for i in k}.values()


def range_from_data(data: list[int]) -> range:
    start = data[0]
    stop = data[-1] + 1
    step = data[1] - data[0]
    return range(start, stop, step)


def zip_from_data(data: list[tuple[Any, Any]]) -> zip:
    n_lists = len(data[0])
    n_items = len(data)
    lists: list[list[Any]] = []
    for i in range(n_lists):
        l: list[Any] = []
        for j in range(n_items):
            l.append(data[j][i])
        lists.append(l)
    return zip(*lists)


def map_from_data(data: list[Any]) -> map:
    return map(lambda x: x, data)


def filter_from_data(data: list[Any]) -> filter:
    return filter(lambda x: True if x else False, data)


def enumerate_from_data(data: list[tuple[int, Any]]) -> enumerate:
    sorted(data, key=lambda x: x[0])
    start = data[0][0]
    data = [x[1] for x in data]
    return enumerate(data, start=start)


def load() -> None:
    Config.add_class(name="set", class_=set)
    Config.add_class(
        name="dict_items", class_=dict_items, from_data=dict_items_from_data
    )
    Config.add_class(name="dict_keys", class_=dict_keys, from_data=dict_keys_from_data)
    Config.add_class(
        name="dict_values", class_=dict_values, from_data=dict_values_from_data
    )
    Config.add_class(name="range", class_=range, from_data=range_from_data)
    Config.add_class(
        name="zip",
        class_=zip,
        from_data=zip_from_data,
    )
    Config.add_class(
        name="map", class_=map, from_data=map_from_data, to_data=lambda x: list(x)
    )
    Config.add_class(name="filter", class_=filter, from_data=filter_from_data)
    Config.add_class(name="enumerate", class_=enumerate, from_data=enumerate_from_data)
    Config.add_class(name="bytearray", class_=bytearray)
    Config.add_class(name="bytes", class_=bytes)
    Config.add_class(name="tuple", class_=tuple)
