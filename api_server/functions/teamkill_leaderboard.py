import asyncio
from auraxium import Client
from auraxium.ps2 import Outfit
from typing import Tuple, List, Any, Iterable, Optional, Coroutine, Callable, Dict, Union
from auraxium.census import Query
from functools import reduce
from enum import Enum
from .functional_utils import read_file, pipe_async, map_curried, get_keys, with_debug, get_n, update_dict, execute_many_async, with_timing, chunk, pipe, map_async
import itertools

# constants
# Make sure you don't commit the API key -_-
# If getting service id errors, check that PS2_API_key matches /s:\w+/
API_KEY = read_file("PS2_API_KEY.txt")[0]
DTWM_ID = 37566723466738093


class Faction(Enum):
    """A human-friendly representation of a character's faction."""
    VS = 1
    NC = 2
    TR = 3
    NSO = 4


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


def with_show(fields: Optional[List[str]] = None):
    """Add a filter for the fields sent back from the query."""
    def with_show_inner(query: Query) -> Query:
        if not fields:
            return query
        show_string = ",".join(fields)
        query.show(show_string)
        return query
    return with_show_inner


async def outfit_id_by_tag(outfit_tag: str) -> Optional[int]:
    """Get an outfit's ID from their tag. Case insensitive"""

    lowercase_tag = outfit_tag.lower()
    async with Client() as client:  # default service ID used to avoid having to pass the main client
        result = await client.get(Outfit, alias_lower=lowercase_tag)
    if not result:
        return None
    return result.id


def query_outfit(outfit_id: int):
    """Build an API query for an outfit by ID."""
    return query_factory("outfit_member")(outfit_id=outfit_id)()


def with_character_query(query: Query):
    """Mix in a join on character."""
    query.create_join("character")
    query.limit(150)
    return query


get_characters_query = pipe(
    (query_outfit, with_character_query))


def get_outfit_chars(outfit_id: int):
    """Get all the characters of an outfit by its ID."""
    def char_from_member(member):
        return member["character_id_join_character"]

    async def get_outfit_chars_inner(client: Client) -> List[dict]:
        query = get_characters_query(outfit_id)
        result = await client.request(query)
        return map_curried(char_from_member)(result["outfit_member_list"])
    return get_outfit_chars_inner


def chars_to_ids(chars: List[dict]) -> List[int]:
    """Convert a list of characters to their IDs."""
    return [int(c["character_id"]) for c in chars]


def character_query(ids: List[int]) -> Query:
    """Build an API query for a character."""
    return query_factory("character")(character_id=",".join(map(str, ids)))()


def null_char(id: int):
    """Create a fake character for if no character was returned for an ID."""
    return {
        "name": "<null char>",
                "faction_id": str(Faction.NSO.value),
                "character_id": id,
    }


def find_char(chars: List[dict]):
    """Find a character by ID within a list of characters."""
    def find_char_inner(id: int) -> dict:
        for char in chars:
            if int(char["character_id"]) == id:
                return char
        return null_char(id)
    return find_char_inner


def validate_char_result(chars: List[dict]):
    """Insert null characters where no character was returned for an ID."""
    def validate_char_result_inner(ids: List[int]) -> List[dict]:
        return [find_char(chars)(id) for id in ids]
    return validate_char_result_inner


def _query_chars(client: Client):
    """Get characters from the API."""
    def query_chars_inner(fields: Optional[List[str]] = None):
        async def query_chars_inner2(ids: List[int]):
            # TODO: batch into 100 players/query
            char_query = character_query(ids)
            query = with_show(fields)(char_query)
            result = await client.request(query)
            chars = result["character_list"]
            return validate_char_result(chars)(ids)
        return query_chars_inner2
    return query_chars_inner


def get_chars_batched(client: Client):
    """Batch request characters by id from the API"""
    def get_chars_inner(show_fields: List[str] = None):
        async def get_chars_inner2(ids: List[int]):
            fields = show_fields or []
            batched_ids = chunk(100)(ids) if len(ids) > 100 else [ids]
            results = await execute_many_async(_query_chars(client)(fields))(batched_ids)
            return itertools.chain.from_iterable(results)
        return get_chars_inner2
    return get_chars_inner


def char_to_name(char: dict) -> str:
    """Get the name of a character."""
    return get_keys(["name", "first"])(char)


def faction_from_char(char: dict) -> Faction:
    """Get the faction of a character"""
    return Faction(int(char["faction_id"]))


def is_nso(faction: Faction) -> bool:
    return faction == Faction.NSO


def find_first_non_nso(factions: List[Faction]) -> Faction:
    for f in factions:
        if not is_nso(f):
            return f
    raise ValueError(f"All {len(factions)} players were NSO")


def not_nso_outfit(factions: List[Faction]) -> Optional[Faction]:
    """
    Returns a non-NSO faction if the outfit has any.
    Returns None if no non-NSOs were found.
    """
    try:
        # Assume that if the first 5 characters are NSO, all of them are
        return find_first_non_nso(factions[:5])
    except ValueError:
        return None


def kill_event_query(limit: int = 500):
    """Build an API query for the kill events of a player."""
    def kill_event_inner(char_id: int):
        query = query_factory("characters_event")(
            type="KILL", character_id=char_id)()
        query.limit(limit)
        return query
    return kill_event_inner


def do_kill_event_query(client):
    """Get the kill events for a character"""
    async def do_total_kills_query_inner(char_id: int):
        result = await client.request(kill_event_query(250)(char_id))
        return result["characters_event_list"]
    return do_total_kills_query_inner


def kills_to_factions(client: Client):
    """Get the faction of the person killed in the event."""
    async def kills_to_factions_inner(kill_events: List[dict]) -> List[Faction]:
        ids: List[int] = list(
            map(lambda e: int(e["character_id"]), kill_events))
        chars = await get_chars_batched(client)(["faction_id", "character_id"])(ids)
        factions: Iterable[Faction] = map_curried(faction_from_char)(chars)
        return list(factions)
    return kills_to_factions_inner


def remove_suicides(events: List[dict]) -> List[dict]:
    def is_not_suicide(event: dict) -> bool:
        return event["character_id"] != event["attacker_character_id"]
    return list(filter(is_not_suicide, events))


def is_tk(char_faction: Faction):
    def is_tk_inner(killed_faction: Faction):
        return killed_faction == char_faction
    return is_tk_inner


def count_tks(char_faction: Faction) -> Callable[[List[Faction]], List[int]]:
    """Get a function to count the number of teamkills from a list of kill events."""
    def count_truthy(acc: int, value: Any):
        return acc + 1 if value else acc

    return pipe(
        [map_curried(is_tk(char_faction)),
         lambda tks: reduce(count_truthy, tks, 0)]
    )


def teamkills(client: Client):
    def teamkills_inner(char_faction: Faction):
        teamkills_inner_func: Callable[[int], Coroutine] = pipe_async((
            do_kill_event_query(client),
            remove_suicides,
            # all the time is spent here
            kills_to_factions(client),
            count_tks(char_faction),
        ))
        return teamkills_inner_func
    return teamkills_inner


TKRecord = Tuple[dict, int]  # a record of a character and their TKs
TKTable = List[TKRecord]


def build_tks_table(chars: List[dict]):
    """
    Transform characters and their TKs into a list of records.
    ASSUMPTION: chars[0] corresponds to tks[0]
    """

    def sort_by_tk(record: TKRecord):
        return record[1]

    def build_tks_table_inner(tks: List[int]) -> TKTable:
        if len(chars) != len(tks):
            raise ValueError("Uneven length between characters and tks")
        names = map_curried(char_to_name)(chars)
        records: Iterable[TKRecord] = zip(names, tks)
        return sorted(records, key=sort_by_tk)
    return build_tks_table_inner


def table_to_dicts(table: TKTable) -> List[dict]:
    """Transform the tuples to dictionaries."""
    return list(map(lambda row: {"name": row[0], "tks": row[1]}, table))


def convert_nso(outfit_faction: Faction):
    def convert_nso_inner(char: dict):
        faction = faction_from_char(char)
        return update_dict({"faction_id": outfit_faction}) if is_nso(faction) else char
    return convert_nso_inner


def check_nso(chars: List[dict]):
    """
    Check if an outfit is NSO.
    Returns the faction of the outfit, or None if it's NSO.
    """
    first_5_chars = get_n(5)(chars)
    first_5_factions = list(map_curried(faction_from_char)(first_5_chars))
    outfit_faction = not_nso_outfit(first_5_factions)
    return outfit_faction


def clean_chars(outfit_faction: Faction):
    """Convert NSO characters to their outfit's faction."""
    def clean_chars_inner(chars: List[dict]) -> List[dict]:
        return [c for c in map_curried(
            convert_nso(outfit_faction))(chars)]
    return clean_chars_inner


async def main(outfit_id: int = DTWM_ID) -> Coroutine[None, None, TKTable]:
    async with Client(service_id=API_KEY) as client:
        # Fetch the outfit
        # Generators are consumed upon usage, so I need a list
        chars = list(await get_outfit_chars(outfit_id)(client))  # 0.8 seconds
        ids = chars_to_ids(chars)  # negligible

        # Check that it's not an NSO outfit
        outfit_faction = check_nso(chars)  # negligible
        if not outfit_faction:
            raise ValueError("NSO outfit")

        # Conform NSOs with the faction of the outfit
        cleaned_chars = clean_chars(outfit_faction)(chars)  # negligible

        # build table
        get_tks_with_progress = with_debug(teamkills(client)(outfit_faction))
        # 35.9 seconds
        teamkills_per_member = await execute_many_async(get_tks_with_progress)(ids)
        table = build_tks_table(cleaned_chars)(
            teamkills_per_member)  # negligible
        final_form = table_to_dicts(table)
        print(table)
        return final_form


if __name__ == "__main__":
    # asyncio.get_event_loop().run_until_complete(with_timing(main)())
    async def test():
        id = await outfit_id_by_tag("bho")
        res = await main(id)
    asyncio.get_event_loop().run_until_complete(test())
