# Copyright 2018 John Reese
# Licensed under the MIT license

import asyncio

from functools import wraps
from typing import Any, Callable

SENTINEL = object()


def async_test(fn: Callable[..., Any]) -> Callable[..., Any]:

    @wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(fn(*args, **kwargs))

    return wrapper


class awaitable:

    def __init__(self, obj: Any = SENTINEL) -> None:
        if obj is SENTINEL:
            obj = self

        self.obj = obj

    async def __aenter__(self) -> Any:
        return self.obj

    async def __aexit__(self, *args) -> None:
        pass

    def __call__(self, *args, **kwargs) -> Any:
        return self.obj

    def __await__(self) -> Any:

        async def wrapped():
            return self.obj

        return wrapped().__await__()
