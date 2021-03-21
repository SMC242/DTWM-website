import asyncio
import auraxium
from typing import AsyncGenerator, Coroutine, List, Union, Callable, Any
from auraxium import ps2
from auraxium.census import Query
from json import dumps
from inspect import iscoroutinefunction as is_coro
from enum import Enum
from functools import partial

# constants


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


API_KEY = read_file("PS2_API_KEY.txt")[0]
DTWM_ID = 37566723466738093


def call_func(func: Union[Coroutine, Callable]):
    async def call_func_inner(args):
        if is_coro(func):
            return await func(*args)
        return func(*args)
    return call_func_inner


def pipe_async(*funcs: List[Union[Coroutine, Callable]]):
    async def pipe_async_inner(*args):
        result = await call_func(funcs[0])(args)
        for func in funcs[1:]:
            result = await call_func(func)([result])
        return result
    return pipe_async_inner


def with_debug(func):
    async def with_debug_inner(*args):
        print(f"Arguments for function {func} were: {args}")
        result = await call_func(func)(args)
        print(f"Output: {result}")
        return result
    return with_debug_inner


def prettify(data): return dumps(data, sort_keys=True, indent=4)


def pretty_print(data: dict) -> dict:
    print(prettify(data))
    return data


def map_async(f: Callable):
    async def map_async_inner(data: List[Any]) -> AsyncGenerator[None, dict]:
        for x in data:
            yield await f(x)
    return map_async_inner


def query_outfit(outfit_id: int):
    return Query("outfit_member", outfit_id=outfit_id).limit(1000)


def with_character_query(query: Query):
    query.create_join("character")
    return query


get_characters_query = pipe_async(
    query_outfit, with_character_query)


def get_chars(outfit_id: int):
    async def get_kills_per_char_inner(client: auraxium.Client):
        query = await get_characters_query(outfit_id)
        result = await client.request(query)
        return result["outfit_member_list"]
    return get_kills_per_char_inner


def kills_query(char: ps2.Character):
    query = Query("event",
                  type="KILL").limit(1000)
    query.create_join("attacker_character_id=character_id")
    return query


def do_kills_query(client):
    async def do_kills_query_inner(char: ps2.Character):
        return await client.request(kills_query(char))
    return do_kills_query_inner


class Faction(Enum):
    VS = 1
    NC = 2
    TR = 3


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        chars = await get_chars(DTWM_ID)(client)
        outfit_kills = map_async(do_kills_query(client))(chars)
        i = 0
        async for kills_list in outfit_kills:
            if i == 3:
                break
            print(f"----\n{i}\n----")
            pretty_print(kills_list)
            i += 1


asyncio.get_event_loop().run_until_complete(main())
