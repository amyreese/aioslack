# Copyright 2018 John Reese
# Licensed under the MIT license

import asyncio
from typing import Any, AsyncIterator, Dict, Optional

import aiohttp


class SlackError(Exception):
    """
    Generic error type for all Slack-related errors.
    """


class Slack:
    """
    Slack API entry point.
    """

    def __init__(self, token: str) -> None:
        self.token: str = token
        self._session: Optional[aiohttp.ClientSession] = None

    def __del__(self) -> None:
        asyncio.ensure_future(self.close())

    async def __aenter__(self) -> "Slack":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    @property
    def session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.token}"}
            )
        return self._session

    async def close(self) -> None:
        # TODO: track RTM sessions as tasks and cancel them here
        await self.session.close()
        self._session = None

    async def api(self, method: str, data: Dict[str, str] = None) -> Any:
        data = data or {}
        async with self.session.post(
            f"https://slack.com/api/{method}", json=data
        ) as response:
            if response.status != 200:
                raise SlackError(f"{method} returned status {response.status}")

            return await response.json()

    async def rtm(self) -> AsyncIterator[Any]:
        """Connect to the realtime messaging API and start yielding messages."""
        response = await self.api("rtm.connect")

        async with self.session.ws_connect(response["url"]) as ws:
            async for msg in ws:
                message = msg.json()
                if message["type"] == "goodbye":
                    break

                yield message
