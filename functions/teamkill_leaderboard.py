import asyncio
import auraxium
from typing import Coroutine, List, Union, Callable
from auraxium import ps2
from auraxium.errors import MissingServiceIDError
from inspect import iscoroutinefunction as is_coro

# constants


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


API_KEY = read_file("PS2_API_KEY.txt")[0]
DTWM_ID = 37566723466738093


def pipe_async(*funcs: List[Union[Coroutine, Callable]]):
    def call_func(func: Union[Coroutine, Callable]):
        async def call_func_inner(args):
            if is_coro(func):
                return await func(*args)
            return func(*args)
        return call_func_inner

    async def pipe_async_inner(*args):
        result = await call_func(funcs[0])(args)
        for func in funcs[1:]:
            result = await call_func(func)([result])
        return result
    return pipe_async_inner


def with_retry(func):
    async def with_retry_inner(*args):
        try:
            result = await func(*args)
        except MissingServiceIDError:
            print("Rate limited. Retrying...")
            for i in range(6):
                await asyncio.sleep(10)
                print(f"Waited {i + 1 * 10} seconds so far")
            result = await func(*args)
        return result
    return with_retry_inner


def get_dtwm(dtwm_id: int) -> Coroutine[None, None, ps2.Outfit]:
    async def get_dtwm_inner(client: auraxium.Client):
        result = await client.get_by_id(ps2.Outfit, dtwm_id)
        if not result:
            raise ValueError(
                "Failed to get DTWM outfit. Check that the DTWM id is correct")
        return result
    return get_dtwm_inner


async def get_members(outfit: ps2.Outfit):
    return await outfit.members().flatten()


async def to_character(member: ps2.OutfitMember):
    return await member.character()


def get_characters(members: List[ps2.OutfitMember]):
    return asyncio.gather(*[to_character(m) for m in members])


async def get_kills(char: ps2.Character):
    return await char.events(type="KILL")


def kills_per_char(chars: List[ps2.Character]):
    # check what return asyncio.gather does
    return asyncio.gather(*[get_kills(c) for c in chars])


get_all_chars = pipe_async(
    get_dtwm(DTWM_ID),
    with_retry(get_members),
    with_retry(get_characters)
)


async def main():
    async with auraxium.Client(service_id=API_KEY) as client:
        characters = await get_all_chars(client)

        kills_per_character = kills_per_char(characters)
        print(kills_per_character)


asyncio.get_event_loop().run_until_complete(main())
