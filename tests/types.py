# Copyright 2018 John Reese
# Licensed under the MIT license

from typing import Mapping
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

        @dataclass
        class Fizz(Auto):
            buzz: dict

        data = {"buzz": {"foo": "bar"}}
        fizz = Fizz.build(data)
        self.assertIsInstance(fizz.buzz, Auto)
        self.assertEqual(fizz.buzz.foo, "bar")

    def test_auto_generate(self):
        data = {"foo": "bar", "fizz": "buzz"}
        obj = Auto.generate(data)

        self.assertIsInstance(obj, Auto)
        self.assertEqual(obj.__class__.__name__, "Auto")
        self.assertEqual(obj.foo, "bar")
        self.assertEqual(obj.fizz, "buzz")

        data = {"foo": "bar", "fizz": {"buzz": 1, "bug": "bee"}}
        obj = Auto.generate(data, "Something")

        self.assertIsInstance(obj, Auto)
        self.assertEqual(obj.__class__.__name__, "Something")
        self.assertEqual(obj.foo, "bar")
        self.assertIsInstance(obj.fizz, Auto)
        self.assertEqual(obj.fizz.__class__.__name__, "Fizz")
        self.assertEqual(obj.fizz.buzz, 1)
        self.assertEqual(obj.fizz.bug, "bee")

        obj = Auto.generate(data, "Something", recursive=False)

        self.assertIsInstance(obj, Auto)
        self.assertEqual(obj.__class__.__name__, "Something")
        self.assertEqual(obj.foo, "bar")
        self.assertNotIsInstance(obj.fizz, Auto)
        self.assertIsInstance(obj.fizz, Mapping)
        self.assertEqual(obj.fizz, data["fizz"])

    def test_value(self):
        data = {"value": "something", "creator": "me", "last_set": 12345}
        value = Value(value="something", creator="me", last_set=12345)

        self.assertEqual(Value(**data), value)
        self.assertEqual(Value.build(data), value)
