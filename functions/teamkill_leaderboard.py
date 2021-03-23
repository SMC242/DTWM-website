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


def limited_flatten(gen:  AsyncGenerator[None, Any]):
    async def limited_flatten_inner(limit: int) -> AsyncGenerator[None, Any]:
        return [await gen.__anext__() for i in range(limit)]
    return limited_flatten_inner


def query_factory(collection: str):
    def query_factory_inner(**kwargs):
        def query_factory_inner_2(joins: List[str] = None):
            joins = joins or []
            query = Query(collection, service_id=API_KEY, **kwargs)
            query.limit(1000)
            for join_collection in joins:
                query.create_join(join_collection)
            return query
        return query_factory_inner_2
    return query_factory_inner


def query_outfit(outfit_id: int):
    return query_factory("outfit_member")(outfit_id=outfit_id)()


def get_outfit_members(outfit_id: int):
    async def get_kills_per_char_inner(client: auraxium.Client):
        query = query_outfit(outfit_id)
        result = await client.request(query)
        return result["outfit_member_list"]
    return get_kills_per_char_inner


def chars_to_ids(chars: List[dict]):
    return [c["character_id"] for c in chars]


get_outfit_char_ids = pipe_async(get_outfit_members(DTWM_ID), chars_to_ids)


def get_single_char(client: auraxium.Client):
    async def get_single_char_inner(char_id: int):
        q = query_factory("single_character_by_id")(
            character_id=char_id)()
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
    return kills / time_played * 60


def kpm_from_char(client) -> Awaitable[ps2.Character]:
    return pipe_async(
        get_single_char(client),
        get_single_char_stats,
        to_kpm,
        lambda kpm: round(kpm, 3)
    )


def kpm_generator(client):
    def kpm_generator_inner(char_ids: List[int]):
        return map_async(kpm_from_char(client))(char_ids)
    return kpm_generator_inner


async def chunked_kpms(client: auraxium.Client, char_ids: List[int], chunk_size: int = 5, pause_seconds: float = 10.0):
    def next_(gen): return gen.__anext__()
    chunk = []
    gen = kpm_generator(client)(char_ids)
    for i in range(len(char_ids)):
        # Force a delay to prevent rate limit
        if i != 0 and i % chunk_size == 0:
            yield chunk
            chunk = []
            await asyncio.sleep(pause_seconds)
        chunk.append(await next_(gen))


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        ids = await get_outfit_char_ids(client)
        async for chunk in chunked_kpms(client, ids):
            print([k for k in chunk])


asyncio.get_event_loop().run_until_complete(main())
