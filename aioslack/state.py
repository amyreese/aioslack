# Copyright 2018 John Reese
# Licensed under the MIT license

"""
State management of the Slack connectionself.
"""

from typing import Dict, Iterator, Iterable, Mapping, Type, TypeVar, Optional

from .types import Auto

VT = TypeVar("VT", bound=Auto)


class Cache:
    """
    Cache objects of the given type, with optional readthrough via URL.
    """

    def __init__(self, _type: Type[VT], url: str = None) -> None:
        self.cache: Dict[str, VT] = {}
        self.type = _type
        self.url = url

    def __iter__(self) -> Iterator[str]:
        return self.cache.__iter__()

    def __len__(self) -> int:
        return self.cache.__len__()

    def __contains__(self, key: str) -> bool:
        return self.cache.__contains__(key)

    def __getitem__(self, key: str) -> VT:
        if key in self.cache:
            return self.cache[key]

        raise KeyError(f"{self.type.__name__} {key} not in cache")
        # TODO: make API request to fill cache?

    def __setitem__(self, key: str, value: VT) -> None:
        if not isinstance(value, self.type):
            raise ValueError(f"{key} is not {self.type.__name__}")
        self.cache[key] = value

    def __delitem__(self, key: str) -> None:
        return self.cache.__delitem__(key)

    def get(self, key: str, default: Optional[VT] = None) -> Optional[VT]:
        return self.cache.get(key, default)

    def fill(self, values: Iterable[VT], *, key: str = "id") -> None:
        for value in values:
            if not isinstance(value, self.type):
                raise ValueError(f"{value[key]} is not {self.type.__name__}")
            self.cache[value[key]] = value

    def update(self, values: Mapping[str, VT]) -> None:
        for key in values:
            value = values[key]
            if not isinstance(value, self.type):
                raise ValueError(f"{key} is not {self.type.__name__}")
            self.cache[key] = value
