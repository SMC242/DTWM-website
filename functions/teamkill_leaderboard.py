import asyncio
import auraxium
from typing import AsyncGenerator, Awaitable, Coroutine, List, Union, Callable, Any, Optional
from auraxium import ps2
from auraxium.census import Query
from json import dumps
from inspect import iscoroutinefunction as is_coro_func, iscoroutine as is_coro


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


# constants
API_KEY = read_file("PS2_API_KEY.txt")[0]
DTWM_ID = 37566723466738093


def call_func(func: Union[Coroutine, Callable]):
    async def call_func_inner(args):
        if is_coro(func):
            return await func
        elif is_coro_func(func):
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


def get_keys(keys: Union[List[str], str]):
    def get_keys_inner(data: dict):
        if isinstance(keys, str):
            head, tail = keys, None
        else:
            head, *tail = keys
        value = data[head]
        if tail:
            return get_keys(tail)(value)
        return value
    return get_keys_inner


def map_async(f: Callable):
    async def map_async_inner(data: List[Any]) -> AsyncGenerator[None, Any]:
        for x in data:
            yield await f(x)
    return map_async_inner


async def flatten(gen: AsyncGenerator) -> List[Any]:
    return [e async for e in gen]


def limited_flatten(gen: AsyncGenerator) -> List[Any]:
    async def limited_flatten_inner(limit: int):
        stop_signal = "STOP_NOW"

        async def inner_iter(index: int) -> Union[Any, str]:
            if index == limit:
                return stop_signal
            return await next(gen)

        results = []
        for i in range(limit):
            res = await inner_iter(i)
            if res == stop_signal:
                return results
            results.append(res)
        return results
    return limited_flatten_inner


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


def total_kills_query(char: ps2.Character):
    query = Query("event",
                  type="KILL").limit(1000)
    query.create_join(f"attacker_character_id={char['character_id']}")
    return query


def do_total_kills_query(client):
    async def do_total_kills_query_inner(char: ps2.Character):
        return await client.request(total_kills_query(char))
    return do_total_kills_query_inner


def get_single_char(client: auraxium.Client):
    async def get_single_char_inner(char):
        q = Query("single_character_by_id", character_id=char["character_id"])
        return await client.request(q)
    return get_single_char_inner


def get_single_char_stats(data: dict):
    keys = [
        "single_character_by_id_list",
        0,
        "stats",
        "stat_history",
    ]
    return get_keys(keys)(data)


def get_stats(keys: List[List[str]]):
    def get_stat_inner(stats: dict):
        return [get_keys(key_list)(stats) for key_list in keys]
    return get_stat_inner


def to_kpm(stats: dict):
    raw = get_stats([["kills", "all_time"], ["time", "all_time"]])(stats)
    kills, time_played = list(
        map(int, raw))
    return kills / time_played


def kpm_from_char(client) -> Awaitable[ps2.Character]:
    return pipe_async(
        get_single_char(client),
        get_single_char_stats,
        to_kpm
    )


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        chars = await get_chars(DTWM_ID)(client)
        kpms = await flatten(map_async(kpm_from_char(client))(chars))

        print(kpms)
        # chars = await get_chars(DTWM_ID)(client)
        # res = await experimental(client)(chars[0])
        # pretty_print(res)
        # with open("dump.json", "w") as f:
        #    f.write(dumps(res))
        # https://census.daybreakgames.com/s:PS2Damagerequest/get/ps2:v2/single_character_by_id?character_id=5428926375525123617
        # That endpoint has probably everything I need
        #outfit_kills = map_async(do_total_kills_query(client))(chars)


asyncio.get_event_loop().run_until_complete(main())
