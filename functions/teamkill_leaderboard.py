import requests as r
from json import dumps, loads
from typing import List


def pipe(*funcs):
    def inner(*args):
        result = funcs[0](*args)
        for func in funcs[1:]:
            result = func(result)
        return result
    return inner


def get_data(url): return r.get(url)
def to_indexable(data): return loads(data.content)
def prettify(data): return dumps(data, indent=4, sort_keys=True)
def pretty_print(data): return print(prettify(data))


get_dict = pipe(get_data, to_indexable)


def get_keys(keys: List[str]):
    def get_keys_inner(data: dict):
        key, *extra = keys
        print(key)
        value = data[key]
        if extra:
            return get_keys(extra)(value)
        return value
    return get_keys_inner


def get_keys_from_url(url: str):
    def get_keys_from_url_inner(keys: List[str]):
        return pipe(get_dict, get_keys(keys))(url)
    return get_keys_from_url_inner


def get_members():
    url = ("https://census.daybreakgames.com/get/ps2:v2/outfit/"
           + "?alias=DTWM&c:resolve=member_character(name,type.faction)")
    return get_keys_from_url(url)(["outfit_list", 0, "members"])


pretty_print(get_members())
