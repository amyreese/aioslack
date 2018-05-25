# Copyright 2018 John Reese
# Licensed under the MIT license

from unittest import TestCase
from unittest.mock import MagicMock, patch, PropertyMock

from aioslack.core import Slack, SlackError
from aioslack.types import Auto
from .base import async_test, awaitable


class CoreTest(TestCase):

    @patch("aioslack.core.aiohttp")
    @async_test
    async def test_api(self, aiohttp):
        value = {"ok": True, "type": "hello"}

        response = MagicMock(name="response")
        response.status = 200
        response.json.return_value = awaitable(value)

        session = MagicMock(name="session")
        session.post.return_value = awaitable(response)
        session.close.return_value = awaitable(None)

        aiohttp.ClientSession.return_value = session

        async with Slack(token="xoxb-foo") as slack:
            value = await slack.api("something")
            self.assertTrue(value.ok)
            self.assertEqual(value.type, "hello")

        aiohttp.ClientSession.assert_called_with(
            headers={"Authorization": "Bearer xoxb-foo"}
        )
        session.post.assert_called_with("https://slack.com/api/something", json={})
        session.close.assert_called_once()

    @patch("aioslack.core.aiohttp")
    @async_test
    async def test_api_error(self, aiohttp):
        value = {"ok": False, "error": "not found"}

        response = MagicMock(name="response")
        response.status = 200
        response.json.return_value = awaitable(value)

        session = MagicMock(name="session")
        session.post.return_value = awaitable(response)
        session.close.return_value = awaitable(None)

        aiohttp.ClientSession.return_value = session

        with self.assertRaises(SlackError):
            async with Slack(token="xoxb-foo") as slack:
                await slack.api("something")

        aiohttp.ClientSession.assert_called_with(
            headers={"Authorization": "Bearer xoxb-foo"}
        )
        session.post.assert_called_with("https://slack.com/api/something", json={})
        session.close.assert_called_once()

    @patch("aioslack.core.aiohttp")
    @async_test
    async def test_rtm(self, aiohttp):
        rtm_response = {
            "ok": True,
            "url": "https://frob",
            "self": {},
            "team": {},
            "channels": [],
            "users": [],
            "groups": [],
        }
        events = [{"type": "hello"}]

        response = MagicMock(name="response")
        response.status = 200
        response.json.return_value = awaitable(rtm_response)

        async def websocket():
            for idx, event in enumerate(events):
                mock = MagicMock(name=f"event-{idx}")
                mock.json.return_value = event
                yield mock

        session = MagicMock(name="session")
        session.post.return_value = awaitable(response)
        session.close.return_value = awaitable(None)
        session.ws_connect.return_value = awaitable(websocket())

        aiohttp.ClientSession.return_value = session

        async with Slack(token="xoxb-foo") as slack:
            k = 0
            async for event in slack.rtm():
                self.assertEqual(event.type, "hello")

            aiohttp.ClientSession.assert_called_with(
                headers={"Authorization": "Bearer xoxb-foo"}
            )
            session.post.assert_called_with("https://slack.com/api/rtm.start", json={})
            session.ws_connect.assert_called_with(rtm_response["url"])

        session.close.assert_called_once()
