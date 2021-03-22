import asyncio
import auraxium
from typing import AsyncGenerator, Coroutine, List, Union, Callable, Any
from auraxium import ps2
from auraxium.census import Query
from json import dumps
from inspect import iscoroutinefunction as is_coro


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


# constants
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


def total_kills_query(char: ps2.Character):
    query = Query("event",
                  type="KILL").limit(1000)
    query.create_join(f"attacker_character_id={char['character_id']}")
    return query


def do_total_kills_query(client):
    async def do_total_kills_query_inner(char: ps2.Character):
        return await client.request(total_kills_query(char))
    return do_total_kills_query_inner


def experimental(client):
    async def experimental_inner(char):
        q = Query("characters_leaderboard", name="Kills", period="Forever")
        q.has(f"character_id={char['character_id']}")
        return await client.request(q)
    return experimental_inner


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        chars = await get_chars(DTWM_ID)(client)
        pretty_print(await experimental(client)(chars[0]))
        # https://census.daybreakgames.com/s:PS2Damagerequest/get/ps2:v2/single_character_by_id?character_id=5428926375525123617
        # That endpoint has probably everything I need
        #outfit_kills = map_async(do_total_kills_query(client))(chars)


asyncio.get_event_loop().run_until_complete(main())
