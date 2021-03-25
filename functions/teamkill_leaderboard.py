import asyncio
import auraxium
from typing import AsyncGenerator, Tuple, Coroutine, List, Union, Callable, Any, Iterable, Iterator
from auraxium import ps2
from auraxium.census import Query
from json import dumps
from inspect import iscoroutinefunction as is_coro_func, iscoroutine as is_coro
from functools import reduce, partial
from enum import Enum
from time import time


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


# constants
# Make sure you don't commit the API key -_-
# If getting service id errors, check that PS2_API_key matches /s:w+/
API_KEY = read_file("PS2_API_KEY.txt")[0]
DTWM_ID = 37566723466738093


class Faction(Enum):
    """A human-friendly representation of a character's faction."""
    VS = 1
    NC = 2
    TR = 3


def call_func(func: Union[Coroutine, Callable]):
    """Call a function, async function, or coroutine."""
    async def call_func_inner(args):
        if is_coro(func):
            return await func
        elif is_coro_func(func):
            return await func(*args)
        return func(*args)
    return call_func_inner


def pipe(*funcs: Tuple[Callable]):
    """
    Call each function on the results of the last.
    The arguments will be passed to the first function only.
    """
    def pipe_inner(*args, **kwargs):
        result = funcs[0](*args, **kwargs)
        for func in funcs[1:]:
            result = func(result)
        return result
    return pipe_inner


def pipe_async(*funcs: List[Union[Coroutine, Callable]]):
    """
    Call each function on the results of the last.
    The arguments will be passed to the first function only.
    Supports sync and async functions.
    """
    async def pipe_async_inner(*args):
        result = await call_func(funcs[0])(args)
        for func in funcs[1:]:
            result = await call_func(func)([result])
        return result
    return pipe_async_inner


def with_timing(f: Callable):
    """Wrapper that prints the execution time of a function."""
    async def with_timing_inner(*args, **kwargs):
        start = time()
        result = await call_func(f)(*args, **kwargs)
        print(f"Time taken: {time() - start}")
        return result
    return with_timing_inner


def with_debug(func: Callable):
    """
    Wrap a function with a print statement for its inputs,
    outputs and execution time.
    """
    async def with_debug_inner(*args, **kwargs):
        print(f"Arguments for function {func} were: {args}")
        result = await with_timing(func)(*args, **kwargs)
        print(f"Output: {result}")
        return result
    return with_debug_inner


def prettify(data):
    """Convert a dictionary to a human-friendly string."""
    return dumps(data, sort_keys=True, indent=4)


def pretty_print(data: dict) -> dict:
    """Print a human-friendly version of a dictionary."""
    print(prettify(data))
    return data


def get_keys(keys: Union[List[str], str]):
    """Get nested keys in a dictionary."""
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
    """Apply a function to each element of data.
    Supports async and sync functions."""
    async def map_async_inner(data: Iterable[Any]) -> AsyncGenerator[None, Any]:
        for x in data:
            yield await f(x)
    return map_async_inner


def map_curried(f: Callable) -> Callable[[Iterable], Iterator]:
    """Apply a function to each element of data."""
    return partial(map, f)


async def flatten(gen: AsyncGenerator) -> List[Any]:
    """Convert an async generator to a list of its results."""
    return [e async for e in gen]


def query_factory(collection: str):
    """
    Build a query.
    Do not manually construct Queries as you might forget to pass the api key.
    This function is also curried so better than the constructor UmU
    """
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
    """Build an API query for an outfit by ID."""
    return query_factory("outfit_member")(outfit_id=outfit_id)()


def with_character_query(query: Query):
    """Mix in a join on character."""
    query.create_join("character")
    return query


get_characters_query = pipe_async(
    query_outfit, with_character_query)


def get_chars(outfit_id: int):
    """Get all the characters of an outfit by its ID."""
    async def get_kills_per_char_inner(client: auraxium.Client):
        query = await get_characters_query(outfit_id)
        result = await client.request(query)
        return result["outfit_member_list"]
    return get_kills_per_char_inner


def chars_to_ids(chars: List[dict]) -> List[int]:
    """Convert a list of characters to their IDs."""
    return [int(c["character_id"]) for c in chars]


def kill_event_query(char_id: int):
    """Build an API query for the kill events of a player."""
    def kill_event_inner(limit: int = 500):
        query = query_factory("event")(type="KILL")(
            f"attacker_character_id={char_id}")
        query.limit(limit)
        return query
    return kill_event_inner


def do_kill_event_query(client):
    """Get the kill events for a character"""
    async def do_total_kills_query_inner(char_id: int):
        result = await client.request(kill_event_query(char_id)())
        return result["event_list"]
    return do_total_kills_query_inner


def character_query(id: int) -> Query:
    """Build an API query for a character."""
    return query_factory("character")(character_id=id)()


def get_char(client: auraxium.Client):
    """Request a character by id from the API"""
    def char_from_response(response: dict) -> dict:
        return get_keys(["character_list", 0])(response)

    async def get_char_inner(id: int):
        result = await client.request(character_query(id))
        return char_from_response(result)
    return get_char_inner


def faction_from_char(char: dict) -> Faction:
    """Get the faction of a character"""
    return Faction(int(char["faction_id"]))


def kill_to_faction(client: auraxium.Client):
    """Get the faction of the person killed in the event."""
    async def kill_to_faction_inner(kill_event: dict) -> Faction:
        char = await get_char(client)(kill_event["character_id"])
        return faction_from_char(char)
    return kill_to_faction_inner


def teamkills(client: auraxium.Client):
    def count_truthy(acc: int, value: Any):
        return acc + 1 if value else acc

    def teamkills_inner(char_faction: Faction):
        def is_tk(killed_faction: Faction):
            return killed_faction == char_faction

        async def teamkills_inner2(char_id: int):
            kill_events = await do_kill_event_query(client)(char_id)
            killed_factions = await pipe_async(
                map_async(kill_to_faction(client)),
                flatten
            )(kill_events)
            tks: Iterator[bool] = map_curried(is_tk)(killed_factions)
            return reduce(count_truthy, tks)
        return teamkills_inner2
    return teamkills_inner


def build_tks_table(chars: List[dict]):
    """
    Transform characters and their TKs into a list of records.
    ASSUMPTION: chars[0] corresponds to tks[0]
    """
    Record = Tuple[dict, int]  # a record of a character and their TKs

    def sort_by_tk(row1: Record, row2: Record):
        return row1[1] > row2[1]

    def build_tks_table_inner(tks: List[int]):
        if len(chars) != len(tks):
            raise ValueError("Uneven length between characters and tks")
        records: Iterable[Record] = zip(chars, tks)
        return sorted(records, key=sort_by_tk)
    return build_tks_table_inner


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        chars = await get_chars(DTWM_ID)(client)
        ids = chars_to_ids(chars)
        # Assume that everyone in the outfit is from the same faction
        # This will be broken by NSO, however there is no way to check for NSO
        # so this is unavoidable
        faction = await pipe_async(get_char(client), faction_from_char)(ids[0])
        teamkills_per_member = map_async(teamkills(client)(faction))(ids)
        table = build_tks_table(chars)(await flatten(teamkills_per_member))
        print(table)


asyncio.get_event_loop().run_until_complete(main())
