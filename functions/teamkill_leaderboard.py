import asyncio
import auraxium
from typing import List
from auraxium import ps2


def pipe(*funcs):
    def inner(*args):
        result = funcs[0](*args)
        for func in funcs[1:]:
            result = func(result)
        return result
    return inner


def get_dtwm(client: auraxium.Client):
    DTWM_ID = 37566723466738093

    async def get_dtwm_inner():
        result = await client.get_by_id(ps2.Outfit, DTWM_ID)
        if not result:
            raise ValueError(
                "Failed to get DTWM outfit. Check that the DTWM id is correct")
        return result
    return get_dtwm_inner


async def get_members(
    outfit: ps2.Outfit): return await outfit.members().flatten()


async def to_character(
    member: ps2.OutfitMember): return await member.character()


def get_characters(members: List[ps2.OutfitMember]):
    return asyncio.gather(*[to_character(m) for m in members])


async def get_kills(char: ps2.Character):
    return await char.events(type="KILL")


def kills_per_char(chars: List[ps2.Character]):
    return asyncio.gather(*[get_kills(c) for c in chars])


async def main():
    async with auraxium.Client() as client:
        dtwm = await get_dtwm(client)()
        members = await get_members(dtwm)
        characters = await get_characters(members)
        kills_per_member = await kills_per_char(characters)
        print(kills_per_member)


asyncio.get_event_loop().run_until_complete(main())
