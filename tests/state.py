# Copyright 2018 John Reese
# Licensed under the MIT license

from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from aioslack.state import Cache
from .base import async_test, awaitable


class StateTest(TestCase):
    def test_cache_basics(self):
        cache = Cache(dict)
        item = {"id": "c123", "name": "foo"}

        self.assertFalse("c123" in cache)
        cache["c123"] = item
        self.assertTrue("c123" in cache)
        self.assertTrue("foo" in cache)
        self.assertEqual(cache["c123"], item)
        self.assertEqual(cache["foo"], item)

        with self.assertRaises(ValueError):
            cache["bar"] = "baz"

        self.assertFalse("bar" in cache)
