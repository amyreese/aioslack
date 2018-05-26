# Copyright 2018 John Reese
# Licensed under the MIT license

"""
Basic type definitions for the Slack API.

Based on the Object Types documentation at https://api.slack.com/types
"""

import logging

from typing import Any, Dict, List, Mapping, Type, TypeVar
from attr import asdict, dataclass, fields_dict, ib, make_class

T = TypeVar("T", bound="Auto")

Generic = Mapping[str, Any]  # subvalues that we don't (yet?) care about
URL = str
HTML = str

log = logging.getLogger(__name__)


class Auto:

    def __init__(self, **kwargs) -> None:
        # silence mypy by have a default constructor
        pass

    def __contains__(self, key: str) -> bool:
        return key in asdict(self)

    def __getitem__(self, key: str) -> Any:
        return asdict(self)[key]

    @classmethod
    def build(cls: Type[T], data: Generic) -> T:
        """Build objects from dictionaries, recursively."""
        fields = fields_dict(cls)
        kwargs: Dict[str, Any] = {}
        for key, value in data.items():
            if key in fields:
                if isinstance(value, Mapping):
                    t = fields[key].type
                    if issubclass(t, Auto):
                        value = t.build(value)
                    else:
                        value = Auto.generate(value, name=key.title())
                kwargs[key] = value
            else:
                log.warning(f"got unknown attribute {key} for {cls.__name__}")
        return cls(**kwargs)

    @classmethod
    def generate(
        cls: Type[T], data: Generic, name: str = None, *, recursive: bool = True
    ) -> T:
        """Build dataclasses and objects from dictionaries, recursively."""
        if name is None:
            name = cls.__name__
        kls = make_class(name, {k: ib(default=None) for k in data}, bases=(cls,))
        data = {
            k: (
                cls.generate(v, k.title())
                if recursive and isinstance(v, Mapping)
                else v
            )
            for k, v in data.items()
        }
        return kls(**data)


@dataclass
class Value(Auto):
    value: str = ""
    creator: str = ""
    last_set: int = 0


@dataclass
class Channel(Auto):
    id: str
    name: str
    is_channel: bool = True
    created: int = 0
    creator: str = ""
    is_archived: bool = False
    is_general: bool = False
    name_normalized: str = ""
    is_shared: bool = False
    is_org_shared: bool = False
    is_member: bool = False
    is_private: bool = False
    is_mpim: bool = False
    last_read: str = ""
    latest: Generic = {}
    unread_count: int = 0
    unread_count_display: int = 0
    members: List[str] = []
    topic: Value = Value()
    purpose: Value = Value()
    previous_names: List[str] = []


@dataclass
class Conversation(Auto):
    id: str
    name: str
    is_channel: bool = False
    is_group: bool = False
    is_im: bool = False
    created: int = 0
    creator: str = ""
    is_archived: bool = False
    is_general: bool = False
    unlinked: int = 0
    name_normalized: str = ""
    is_read_only: bool = False
    is_shared: bool = False
    is_ext_shared: bool = False
    is_org_shared: bool = False
    pending_shared: List[Any] = []
    is_pending_ext_shared: bool = False
    is_member: bool = False
    is_private: bool = False
    is_mpim: bool = False
    last_read: str = ""
    topic: Value = Value()
    purpose: Value = Value()
    previous_names: List[str] = []
    num_members: int = 0
    locale: str = "en-US"


@dataclass
class Event(Auto):
    type: str = ""


@dataclass
class EventWrapper(Auto):
    token: str = ""
    team_id: str = ""
    api_app_id: str = ""
    event: Event = Event()
    type: str = ""
    authed_users: List[str] = []
    event_id: str = ""
    event_time: int = 0


@dataclass
class File(Auto):
    id: str
    created: int = 0
    timestamp: int = 0
    name: str = ""
    title: str = ""
    mimetype: str = ""
    filetype: str = ""
    pretty_type: str = ""
    user: str = ""
    mode: str = ""
    editable: bool = False
    is_external: bool = False
    external_type: str = ""
    username: str = ""
    size: int = 0
    url_private: URL = ""
    url_private_download: URL = ""
    thumb_64: URL = ""
    thumb_80: URL = ""
    thumb_360: URL = ""
    thumb_360_gif: URL = ""
    thumb_360_w: int = 0
    thumb_360_h: int = 0
    thumb_480: URL = ""
    thumb_480_w: int = 0
    thumb_480_h: int = 0
    thumb_160: URL = ""
    permalink: URL = ""
    permalink_public: URL = ""
    edit_link: URL = ""
    preview: HTML = ""
    preview_highlight: HTML = ""
    lines: int = 0
    lines_more: int = 0
    is_public: bool = False
    public_url_shared: bool = False
    display_as_bot: bool = False
    channels: List[str] = []
    groups: List[str] = []
    ims: List[str] = []
    initial_comment: Generic = {}
    num_stars: int = 0
    is_starred: bool = False
    pinned_to: List[str] = []
    reactions: List[Generic] = []
    comments_count: int = 0


@dataclass
class Group(Auto):
    id: str
    name: str
    is_group: bool = True
    created: int = 0
    creator: str = ""
    is_archived: bool = False
    is_mpim: bool = False
    members: List[str] = []
    topic: Value = Value()
    purpose: Value = Value()
    last_read: str = ""
    latest: Generic = {}
    unread_count: int = 0
    unread_count_display: int = 0


@dataclass
class IM(Auto):
    id: str
    is_im: bool = True
    user: str = ""
    created: int = 0
    is_user_deleted: bool = False


@dataclass
class MPIM(Auto):
    id: str
    name: str
    is_mpim: bool = False
    is_group: bool = False
    created: int = 0
    creator: str = ""
    members: List[str] = []
    last_read: str = ""
    latest: Generic = {}
    unread_count: int = 0
    unread_count_display: int = 0


@dataclass
class Profile(Auto):
    avatar_hash: str = ""
    status_text: str = ""
    status_emoji: str = ""
    real_name: str = ""
    display_name: str = ""
    real_name_normalized: str = ""
    display_name_normalized: str = ""
    email: str = ""
    image_24: URL = ""
    image_32: URL = ""
    image_48: URL = ""
    image_72: URL = ""
    image_192: URL = ""
    image_512: URL = ""
    team: str = ""


@dataclass
class Response(Auto):
    ok: bool
    error: str = ""
    warning: str = ""


@dataclass
class RTMStart(Auto):
    self_: Generic
    team: Generic
    channels: List
    users: List
    groups: List


@dataclass
class User(Auto):
    id: str
    team_id: str
    name: str
    deleted: bool = False
    color: str = ""
    real_name: str = ""
    tz: str = ""
    tz_label: str = ""
    tz_offset: int = 0
    profile: Profile = Profile()
    is_admin: bool = False
    is_owner: bool = False
    is_primary_owner: bool = False
    is_restricted: bool = False
    is_ultra_restricted: bool = False
    is_bot: bool = False
    is_stranger: bool = False
    updated: int = 0
    is_app_user: bool = False
    has_2fa: bool = False
    locale: str = "en-US"


@dataclass
class UserGroup(Auto):
    id: str
    team_id: str = ""
    is_usergroup: bool = True
    name: str = ""
    description: str = ""
    handle: str = ""
    is_external: bool = False
    date_create: int = 0
    date_update: int = 0
    date_delete: int = 0
    auto_type: str = ""
    created_by: str = ""
    updated_by: str = ""
    deleted_by: str = ""
    prefs: Generic = {}
    users: List[str] = []
    user_count: str = ""
