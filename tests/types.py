# Copyright 2018 John Reese
# Licensed under the MIT license

from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from attr import dataclass
from aioslack.types import Auto, Value
from .base import async_test, awaitable


class TypesTest(TestCase):

    def test_auto_build(self):

        @dataclass
        class Foo(Auto):
            fizz: int
            buzz: str

        @dataclass
        class Bar(Auto):
            foo: Foo
            bar: str

        data = {"foo": {"fizz": 1, "buzz": "howdy"}, "bar": "baz"}

        bar = Bar.build(data)
        self.assertEqual(bar, Bar(foo=Foo(fizz=1, buzz="howdy"), bar="baz"))
        self.assertEqual(bar.foo, Foo(fizz=1, buzz="howdy"))
        self.assertEqual(bar.bar, "baz")
        self.assertEqual(bar.foo.fizz, 1)
        self.assertEqual(bar.foo.buzz, "howdy")

    def test_value(self):
        data = {"value": "something", "creator": "me", "last_set": 12345}
        value = Value(value="something", creator="me", last_set=12345)

        self.assertEqual(Value(**data), value)
        self.assertEqual(Value.build(data), value)
