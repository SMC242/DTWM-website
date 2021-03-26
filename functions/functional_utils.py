from json import dumps
from functools import partial
from typing import Awaitable, Dict, Hashable, Optional, TypeVar, Union, Coroutine, Callable, Tuple, List, Iterable, AsyncGenerator, Any, Iterator, cast, overload
from inspect import iscoroutine as is_coro
from time import time

T = TypeVar('T')
T2 = TypeVar('T2')

FuncT = Callable[..., T]  # Generic functin
CoroT = Coroutine[Any, Any, T]  # Generic coroutine
CoroFuncT = Callable[..., CoroT[T]]  # Generic coroutine function
# Generic coroutine or regular function
CoroFuncOptT = Union[FuncT[T], CoroFuncT[T]]

# Recursive string dictionary
DictStrRecT = Dict[str, Union[T, 'DictStrRecT[T]']]


def call_func(func: CoroFuncOptT[T]) -> CoroFuncT[T]:
    """Call a function or coroutine function."""
    async def call_func_inner(
            args: Tuple[Any, ...] = (),
            kwargs: Optional[Dict[str, Any]] = None) -> T:
        if kwargs is None:
            kwargs = {}
        ret: Union[CoroT[T], T] = func(*args, **kwargs)
        if is_coro(ret):
            return await cast(CoroT[T], ret)
        else:
            return cast(T, ret)
    return call_func_inner


def pipe(*funcs: FuncT) -> FuncT:
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


def pipe_async(*funcs: CoroFuncOptT) -> CoroFuncT:
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


def with_timing(f: CoroFuncOptT[T]) -> Callable[..., Awaitable[T]]:
    """Wrapper that prints the execution time of a function."""
    async def with_timing_inner(*args: Any, **kwargs: Any) -> T:
        start = time()
        result = await call_func(f)(args, kwargs)
        print(f"Time taken: {time() - start}")
        return result
    return with_timing_inner


def with_debug(func: CoroFuncOptT[T]) -> Callable[..., Awaitable[T]]:
    """
    Wrap a function with a print statement for its inputs,
    outputs and execution time.
    """
    async def with_debug_inner(*args: Any, **kwargs: Any) -> T:
        print(f"Arguments for function {func} were: {args}")
        result = await with_timing(func)(*args, **kwargs)
        print(f"Output: {result}")
        return result
    return with_debug_inner


def prettify(data: Dict[Hashable, Any]) -> str:
    """Convert a dictionary to a human-friendly string."""
    return dumps(data, sort_keys=True, indent=4)


def pretty_print(data: Dict[T, T2]) -> Dict[T, T2]:
    """Print a human-friendly version of a dictionary."""
    print(prettify(data))
    return data


def get_keys(keys: Union[Iterable[str], str]) -> Callable[[DictStrRecT[T]], T]:
    """Get nested keys in a dictionary."""
    def get_keys_inner(data: DictStrRecT[T]) -> T:
        head: str
        tail: List[str]
        if isinstance(keys, str):
            head, tail = keys, []
        else:
            head, *tail = keys
        value: Union[T, DictStrRecT[T]] = data[head]
        # NOTE: I was unable to get Pylance to cooperate here, it keeps
        # inserting "object" as a type for DictStrRect[T] and it don't make
        # no sense.
        # This might be down to non-ideal support for recursive dictionaries?)
        return get_keys(tail)(value) if tail else value  # type: ignore
    # NOTE: Similar issue here; T is being doubly-assigned by the inner
    # function is *somehow* is a problem? Using T2 doesn't help either as it
    # underconstraints the type.
    return get_keys_inner  # type: ignore


def map_async(f: CoroFuncOptT[T]) -> Callable[[Iterable[T]], AsyncGenerator[T, None]]:
    """Apply a function to each element of data.
    Supports async and sync functions."""
    async def map_async_inner(data: Iterable[T]) -> AsyncGenerator[T, None]:
        for x in data:
            val: Union[Awaitable[T], T] = f(x)
            if is_coro(val):
                yield await cast(Awaitable[T], val)
            else:
                yield cast(T, val)
    return map_async_inner


def map_curried(f: FuncT[T]) -> Callable[[Iterable[Any]], Iterator[T]]:
    """Apply a function to each element of data."""
    return cast(Callable[[Iterable[Any]], Iterator[T]], partial(map, f))


async def flatten(gen: AsyncGenerator[Any, T]) -> List[T]:
    """Convert an async generator to a list of its results."""
    return [e async for e in gen]


def get_n(n: int) -> Callable[[Iterable[T]], List[T]]:
    """Get up to n elements of an iterable."""
    def get_n_inner(iterable: Iterable[T]) -> List[T]:
        results: List[T] = []
        for i, e in enumerate(iterable):
            if i >= n:
                break
            results.append(e)
        return results
    return get_n_inner


def read_file(path: str) -> List[str]:
    with open(path) as f:
        return [line.strip() for line in f.readlines()]
