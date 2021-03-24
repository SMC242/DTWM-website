import asyncio
import auraxium
from typing import AsyncGenerator, Tuple, Coroutine, List, Union, Callable, Any, Optional
from auraxium import ps2
from auraxium.census import Query
from json import dumps
from inspect import iscoroutinefunction as is_coro_func, iscoroutine as is_coro
from functools import reduce


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


def pipe(*funcs: Tuple[Callable]):
    def pipe_inner(*args):
        result = funcs[0](*args)
        for func in funcs[1:]:
            result = func(result)
        return result
    return pipe_inner


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
        data = await client.request(q)
        return get_keys(["single_character_by_id_list", 0])(data)
    return get_single_char_inner


def char_gen(client: auraxium.Client):
    def char_gen_inner(char_ids: List[int]) -> AsyncGenerator[None, dict]:
        f = get_single_char(client)
        return map_async(f)(char_ids)
    return char_gen_inner


def get_single_char_stats(char: dict):
    """Get the stat history of a character.
    This is useful for getting total stats like total kills"""
    keys = [
        "stats",
        "stat_history",
    ]
    return get_keys(keys)(char)


def get_stats(keys: List[List[str]]):
    def get_stat_inner(stats: dict):
        return [get_keys(key_list)(stats) for key_list in keys]
    return get_stat_inner


def get_stat_dict_from_char(char: dict):
    return get_keys(["stats", "stat_by_faction"])(char)


def get_kill_records(stat_records: dict):
    def is_kills(record):
        return record["stat_name"] == "kills"
    return list(filter(is_kills, stat_records))


def enemy_kills_from_record(record: dict) -> int:
    return int(record["value_forever_vs"]) + int(record["value_forever_tr"])


def total_enemy_kills(kill_records: List[dict]) -> int:
    def kills_from_record(acc, record): return acc + \
        enemy_kills_from_record(record)
    return reduce(kills_from_record, kill_records, 0)


total_enemy_kills_from_char = pipe(
    get_stat_dict_from_char,
    get_kill_records,
    total_enemy_kills
)


def total_kills_stat(char: dict) -> int:
    stats = get_single_char_stats(char)
    return int(get_keys(["kills", "all_time"])(stats))


def teamkills(enemy_kills: int):
    def teamkills_inner(total_kills: int) -> int:
        return enemy_kills - total_kills
    return teamkills_inner


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        ids = await get_outfit_char_ids(client)
        chars = char_gen(client)(ids)
        enemy_kills = []
        total_kills = []
        async for char in chars:
            enemy_kills.append(total_enemy_kills_from_char(char))
            total_kills.append(total_kills_stat(char))
        tks = list(map(lambda kills: teamkills(
            kills[0])(kills[1]), zip(enemy_kills, total_kills)))
        print(tks)


asyncio.get_event_loop().run_until_complete(main())
