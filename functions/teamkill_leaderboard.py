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
    query = query_factory("event")(type="KILL")(
        f"attacker_character_id={char['character_id']}")
    return query


def do_total_kills_query(client):
    async def do_total_kills_query_inner(char: ps2.Character):
        return await client.request(total_kills_query(char))
    return do_total_kills_query_inner


def get_single_char(client: auraxium.Client):
    async def get_single_char_inner(char):
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


def kpm_generator(client):
    def kpm_generator_inner(chars):
        return map_async(kpm_from_char(client))(chars)
    return kpm_generator_inner


async def chunked_kpms(client, chars, chunk_size: int = 5, pause_seconds: float = 10.0):
    def next_(gen): return gen.__anext__()
    chunk = []
    gen = kpm_generator(client)(chars)
    for i in range(len(chars)):
        # Force a delay to prevent rate limit
        if i != 0 and i % chunk_size == 0:
            yield chunk
            chunk = []
            await asyncio.sleep(pause_seconds)
        chunk.append(await next_(gen))


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
        async for chunk in chunked_kpms(client, ids):
            print([k for k in chunk])

        # chars = await get_chars(DTWM_ID)(client)
        # res = await experimental(client)(chars[0])
        # pretty_print(res)
        # with open("dump.json", "w") as f:
        #    f.write(dumps(res))
        # https://census.daybreakgames.com/s:PS2Damagerequest/get/ps2:v2/single_character_by_id?character_id=5428926375525123617
        # That endpoint has probably everything I need
        # outfit_kills = map_async(do_total_kills_query(client))(chars)


asyncio.get_event_loop().run_until_complete(main())
