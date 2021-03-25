import asyncio
from auraxium import Client
from typing import Tuple, List, Any, Iterable, Iterator, Optional
from auraxium.census import Query
from functools import reduce
from enum import Enum
from functional_utils import read_file, pipe_async, map_curried, map_async, get_keys, flatten, with_debug, get_n

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
    def char_from_member(member):
        return member["character_id_join_character"]

    async def get_kills_per_char_inner(client: Client):
        query = await get_characters_query(outfit_id)
        result = await client.request(query)
        return map_curried(char_from_member)(result["outfit_member_list"])
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


def get_char(client: Client):
    """Request a character by id from the API"""
    def char_from_response(response: dict) -> dict:
        return get_keys(["character_list", 0])(response)

    def null_char(id: int):
        """Create a fake character for if no character was returned for an ID."""
        return {
            "character_list": {
                "name": "<null char>",
                "faction_id": Faction.NSO,
                "character_id": id,
            },
            "returned": "0"
        }

    async def get_char_inner(id: int):
        result = await client.request(character_query(id))
        validated = result if int(result["returned"]) > 0 else null_char(id)
        return char_from_response(validated)
    return get_char_inner


def faction_from_char(char: dict) -> Faction:
    """Get the faction of a character"""
    return Faction(int(char["faction_id"]))


def kill_to_faction(client: Client):
    """Get the faction of the person killed in the event."""
    async def kill_to_faction_inner(kill_event: dict) -> Faction:
        char = await get_char(client)(kill_event["character_id"])
        return faction_from_char(char)
    return kill_to_faction_inner


def teamkills(client: Client):
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

    def sort_by_tk(record: Record):
        return record[1]

    def build_tks_table_inner(tks: List[int]):
        if len(chars) != len(tks):
            raise ValueError("Uneven length between characters and tks")
        records: Iterable[Record] = zip(chars, tks)
        return sorted(records, key=sort_by_tk)
    return build_tks_table_inner


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
        return find_first_non_nso(factions[5:])
    except ValueError:
        return None


def convert_nso(outfit_faction: Faction):
    def convert_nso_inner(char: dict):
        faction = faction_from_char(char)
        return char.update({"faction_id": outfit_faction}) if is_nso(faction) else char
    return convert_nso_inner


async def main():
    async with Client(service_id=API_KEY) as client:
        # Fetch the outfit
        chars = await get_chars(DTWM_ID)(client)
        ids = chars_to_ids(chars)

        # Check that it's not an NSO outfit
        first_5_chars = get_n(5)(chars)
        first_5_factions = await flatten(map_async(faction_from_char)(first_5_chars))
        outfit_faction = not_nso_outfit(first_5_factions)
        if not outfit_faction:
            # TODO: handle NSO outfit
            pass

        # Conform NSOs with the faction of the outfit
        cleaned_chars = map_curried(convert_nso(outfit_faction))(chars)

        debugged = with_debug(teamkills(client)(outfit_faction))
        teamkills_per_member = map_async(debugged)(ids)
        tks_flat = await flatten(teamkills_per_member)
        table = build_tks_table(cleaned_chars)(tks_flat)
        print(table)


asyncio.get_event_loop().run_until_complete(main())
