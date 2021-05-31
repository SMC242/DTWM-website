from json import dumps
from functools import partial
from typing import Awaitable, Dict, Hashable, Optional, TypeVar, Union, Coroutine, Callable, Tuple, List, Iterable, AsyncGenerator, Any, Iterator, cast, overload
from inspect import iscoroutine as is_coro
from time import time
from asyncio import gather

T = TypeVar('T')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')

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


@overload
def pipe(funcs: Tuple[FuncT[T]]) -> FuncT[T]:
    # Type hint only signature (1 arg)
    ...


@overload
def pipe(funcs: Tuple[FuncT[T], Callable[[T], T2]]) -> FuncT[T2]:
    # Type hint only signature (2 args)
    ...


@overload
def pipe(funcs: Tuple[FuncT[T], Callable[[T], T2], Callable[[T2], T3]]) -> FuncT[T3]:
    # Type hint only signature (3 args)
    ...


@overload
def pipe(funcs: Tuple[FuncT[T], Callable[[T], T2], Callable[[T2], T3], Callable[[T3], T4]]) -> FuncT[T4]:
    # Type hint only signature (4 args)
    ...


@overload
def pipe(funcs: Tuple[FuncT[T], Callable[[T], T2], Callable[[T2], T3], Callable[[T3], T4], Callable[[T4], T5]]) -> FuncT[T5]:
    # Type hint only signature (5 args)
    ...


def pipe(funcs: Tuple[FuncT[T], ...]) -> FuncT[T]:
    """
    Call each function on the results of the last.
    The arguments will be passed to the first function only.
    """
    if not funcs:
        raise ValueError('Functions tuple is empty')

    def pipe_inner(*args: Any, **kwargs: Any) -> T:
        result: Any = funcs[0](*args, **kwargs)
        for func in funcs[1:]:
            result = func(result)
        return result

    return pipe_inner


@overload
def pipe_async(funcs: Tuple[CoroFuncOptT[T]]) -> CoroFuncT[T]:
    # Type hint only signature (1 arg)
    ...


@overload
def pipe_async(funcs: Tuple[CoroFuncOptT[T], Callable[[T], Awaitable[T2]]]) -> CoroFuncT[T2]:
    # Type hint only signature (2 args)
    ...


@overload
def pipe_async(funcs: Tuple[CoroFuncOptT[T], Callable[[T], Awaitable[T2]], Callable[[T2], Awaitable[T3]]]) -> CoroFuncT[T3]:
    # Type hint only signature (3 args)
    ...


@overload
def pipe_async(funcs: Tuple[CoroFuncOptT[T], Callable[[T], Awaitable[T2]], Callable[[T2], Awaitable[T3]], Callable[[T3], Awaitable[T4]]]) -> CoroFuncT[T4]:
    # Type hint only signature (4 args)
    ...


@overload
def pipe_async(funcs: Tuple[CoroFuncOptT[T], Callable[[T], Awaitable[T2]], Callable[[T2], Awaitable[T3]], Callable[[T3], Awaitable[T4]], Callable[[T4], Awaitable[T5]]]) -> CoroFuncT[T5]:
    # Type hint only signature (5 args)
    ...


def pipe_async(funcs: Tuple[CoroFuncOptT[T], ...]) -> CoroFuncT[T]:
    """
    Call each function on the results of the last.
    The arguments will be passed to the first function only.
    Supports sync and async functions.
    """
    if not funcs:
        raise ValueError('Functions tuple is empty')

    async def pipe_async_inner(*args: Any, **kwargs: Any) -> T:
        result: Any = await call_func(funcs[0])(args, kwargs)
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


def to_coros(func: Callable[..., Coroutine[None, None, T]]):
    """
    Applies the function to the list of arguments and returns all the coroutines.
    This is meant to be piped into execute_many.
    """
    def to_coros_inner(data: Iterable) -> List[Coroutine[None, None, T]]:
        return [func(e) for e in data]
    return to_coros_inner


async def execute_many(coros: List[Coroutine[None, None, Any]]):
    return await gather(*coros)


def execute_many_async(func: Callable[..., Coroutine[None, None, T]]):
    def execute_many_async_inner(data: Iterable) -> Coroutine[None, None, List[T]]:
        coros = to_coros(func)(data)
        return execute_many(coros)
    return execute_many_async_inner


def update_dict(d1: dict):
    """Merge the two dictionaries and return the new dictionary."""
    def update_dict_inner(d2: dict):
        return d1.update(d2) or d1
    return update_dict_inner


def chunk(chunk_size: int = 20):
    """Split a list into pieces sized `chunk_size` or less."""
    def chunk_inner(xs: list) -> List[list]:
        return [xs[i: i + chunk_size] for i in range(0, len(xs), chunk_size)]
    return chunk_inner
