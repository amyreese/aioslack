# Copyright 2018 John Reese
# Licensed under the MIT license

from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from aioslack.state import Cache
from .base import async_test, awaitable


class StateTest(TestCase):

    def test_cache_basics(self):
        cache = Cache(int)

        self.assertFalse("foo" in cache)
        cache["foo"] = 1
        self.assertTrue("foo" in cache)
        self.assertEqual(cache["foo"], 1)

        with self.assertRaises(ValueError):
            cache["bar"] = "baz"

        self.assertFalse("bar" in cache)
