# Copyright 2018 John Reese
# Licensed under the MIT license

import asyncio
import logging
import re
from typing import cast, Any, AsyncIterator, Match

import aiohttp

from .state import Cache
from .types import Auto, Channel, Event, Group, User, Response, RTMStart

log = logging.getLogger(__name__)


class SlackError(Exception):
    """
    Generic error type for all Slack-related errors.
    """

    def __init__(self, message: str, *context: Any) -> None:
        super().__init__(message)
        self.context = context


class Slack:
    """
    Slack API entry point.
    """

    def __init__(self, token: str) -> None:
        self.token: str = token
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {self.token}"}
        )

        self.me: Auto = Auto()
        self.team: Auto = Auto()
        self.channels = Cache(Channel, "channels.info")
        self.users = Cache(User, "users.info")
        self.groups = Cache(Group, "groups.info")

        self.decode_re = re.compile(r"<(?:@(?P<userid>\w+)|!(?P<alias>\w+))>")
        self.encode_re = re.compile(r"@(?P<name>\w+)")

    def __del__(self) -> None:
        asyncio.ensure_future(self.close())

    async def __aenter__(self) -> "Slack":
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def close(self) -> None:
        # TODO: track RTM sessions as tasks and cancel them here
        await self.session.close()

    async def api(self, method: str, **kwargs: str) -> Auto:
        async with self.session.post(
            f"https://slack.com/api/{method}", data=kwargs
        ) as request:
            if request.status != 200:
                raise SlackError(f"{method} returned status {request.status}")

            value = await request.json()
            if "self" in value:
                value["self_"] = value.pop("self")
            response = Response.generate(value, recursive=False)
            if not response.ok:
                raise SlackError(
                    f'{method} error: "{response.error}"', kwargs, response
                )
            if response.warning:
                log.warning(f'{method} warning: "{response.warning}"')
            return response

    async def rtm(self) -> AsyncIterator[Event]:
        """Connect to the realtime event API and start yielding events."""
        response = cast(RTMStart, await self.api("rtm.start"))

        self.me = Auto.generate(response.self_, "Me", recursive=False)
        self.team = Auto.generate(response.team, "Team", recursive=False)
        self.channels.fill(Channel.build(item) for item in response.channels)
        self.users.fill(User.build(item) for item in response.users)
        self.groups.fill(Group.build(item) for item in response.groups)

        log.debug(
            f"received {len(self.users)} users, {len(self.channels)} channels "
            f"and {len(self.groups)} groups from rtm.start"
        )

        async with self.session.ws_connect(response["url"]) as ws:
            async for msg in ws:
                event: Event = Event.generate(msg.json(), recursive=False)

                if event.type == "goodbye":
                    break

                yield event

    def decode(self, text: str, prefix: str = "@") -> str:
        """Decode <@id> and <!alias> into @username."""

        def callback(match: Match) -> str:
            m = match.groupdict()
            if m["userid"]:
                user = self.users.get(m["userid"], None)
                if user is None:
                    username = m["userid"]
                else:
                    username = user.name
            elif m["alias"]:
                username = m["alias"]
            return f"{prefix}{username}"

        return self.decode_re.sub(callback, text)

    def encode(self, text: str) -> str:
        """Encode @username into <@id> or <!alias>."""

        def callback(match: Match) -> str:
            name = match.group("name").lower()
            if name in ["here", "everyone", "channel"]:
                return f"<!{name}>"
            else:
                for user in self.users.values():
                    if user.name == name:
                        return f"<@{user.id}>"
            return match.group(0)

        return self.encode_re.sub(callback, text)
