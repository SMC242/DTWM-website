import asyncio
import auraxium
from typing import AsyncGenerator, Tuple, Coroutine, List, Union, Callable, Any, Iterable
from auraxium import ps2
from auraxium.census import Query
from json import dumps
from inspect import iscoroutinefunction as is_coro_func, iscoroutine as is_coro
from functools import reduce
from enum import Enum


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


# constants
API_KEY = read_file("PS2_API_KEY.txt")[0]
DTWM_ID = 37566723466738093


class Faction(Enum):
    VS = 1
    NC = 2
    TR = 3


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
    async def map_async_inner(data: Iterable[Any]) -> AsyncGenerator[None, Any]:
        for x in data:
            yield await f(x)
    return map_async_inner


async def flatten(gen: AsyncGenerator) -> List[Any]:
    return [e async for e in gen]


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


def chars_to_ids(chars: List[dict]) -> List[int]:
    return [int(c["character_id"]) for c in chars]


get_outfit_ids = pipe_async(get_chars(DTWM_ID), chars_to_ids)


def total_kills_query(char_id: int):
    query = query_factory("event")(type="KILL")(
        f"attacker_character_id={char_id}")
    return query


def do_kill_event_query(client):
    async def do_total_kills_query_inner(char_id: int):
        return (await client.request(total_kills_query(char_id)))["event_list"]
    return do_total_kills_query_inner


def character_query(id: int) -> Query:
    return query_factory("character")(character_id=id)()


def get_char(client: auraxium.Client):
    def char_from_response(response: dict) -> dict:
        return get_keys(["character_list", 0])(response)

    async def get_char_inner(id: int):
        result = await client.request(character_query(id))
        return char_from_response(result)
    return get_char_inner


def kill_to_faction(client: auraxium.Client):
    async def kill_to_faction_inner(kill_event: dict) -> Faction:
        char = await get_char(client)(kill_event["character_id"])
        print(char["name"]["first"])
        return Faction(int(char["faction_id"]))
    return kill_to_faction_inner


def teamkills(client: auraxium.Client):

    async def teamkills_inner(char_id: int):
        kill_events = await do_total_kills_query(client)(char_id)
        killed_factions = map_async(kill_to_faction)(client)(kill_events)
        def is_tk(faction): return faction == =


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        ids = await get_outfit_ids(client)
        kills = await do_total_kills_query(client)(ids[0])
        print(await kill_to_faction(client)(kills[0]))

        # chars = await get_chars(DTWM_ID)(client)
        # res = await experimental(client)(chars[0])
        # pretty_print(res)
        # with open("dump.json", "w") as f:
        #    f.write(dumps(res))
        # https://census.daybreakgames.com/s:PS2Damagerequest/get/ps2:v2/single_character_by_id?character_id=5428926375525123617
        # That endpoint has probably everything I need
        # outfit_kills = map_async(do_total_kills_query(client))(chars)


asyncio.get_event_loop().run_until_complete(main())
