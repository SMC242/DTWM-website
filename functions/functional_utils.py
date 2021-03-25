from json import dumps
from functools import partial
from typing import Union, Coroutine, Callable, Tuple, List, Iterable, AsyncGenerator, Any, Iterator
from inspect import iscoroutinefunction as is_coro_func, iscoroutine as is_coro
from time import time


def call_func(func: Union[Coroutine, Callable]):
    """Call a function, async function, or coroutine."""
    async def call_func_inner(args=tuple(), kwargs=None):
        if not kwargs:
            kwargs = {}
        if is_coro(func):
            return await func
        elif is_coro_func(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)
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
    async def pipe_async_inner(*args, **kwargs):
        result = await call_func(funcs[0])(args, kwargs)
        for func in funcs[1:]:
            result = await call_func(func)([result])
        return result
    return pipe_async_inner


def with_timing(f: Callable):
    """Wrapper that prints the execution time of a function."""
    async def with_timing_inner(*args, **kwargs):
        start = time()
        result = await call_func(f)(args, kwargs)
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


def get_n(n: int) -> list:
    """Get up to n elements of an iterable."""
    def get_n_inner(iterable: Iterable):
        results = []
        for i, e in enumerate(iterable):
            if i == n:
                break
            results.append(e)
        return results
    return get_n_inner


def read_file(path: str):
    with open(path) as f:
        return [line.strip() for line in f.readlines()]
