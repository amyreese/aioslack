# Copyright 2018 John Reese
# Licensed under the MIT license

"""
Basic type definitions for the Slack API.

Based on the Object Types documentation at https://api.slack.com/types
"""

from typing import Any, Dict, List, Mapping, Type, TypeVar
from attr import asdict, dataclass, fields_dict, make_class

T = TypeVar("T", bound="Auto")

Generic = Mapping[str, Any]  # subvalues that we don't (yet?) care about
URL = str
HTML = str


class Auto:

    def __init__(self, **kwargs) -> None:
        # silence mypy by have a default constructor
        pass

    def __getitem__(self, key: str) -> Any:
        return asdict(self)[key]

    @classmethod
    def build(cls: Type[T], data: Generic) -> T:
        """Build objects from dictionaries, recursively."""
        fields = fields_dict(cls)
        kwargs: Dict[str, Any] = {}
        for key, value in data.items():
            if key in fields and isinstance(value, Mapping):
                t = fields[key].type
                if issubclass(t, Auto):
                    value = t.build(value)
                else:
                    value = Auto.generate(value, name=key.title())
            kwargs[key] = value
        return cls(**kwargs)

    @classmethod
    def generate(
        cls, data: Generic, name: str = "Unknown", *, recursive: bool = True
    ) -> T:
        """Build dataclasses and objects from dictionaries, recursively."""
        kls = make_class(name, list(data.keys()), bases=(Auto,))
        data = {
            k: (
                Auto.generate(v, k.title())
                if recursive and isinstance(v, Mapping)
                else v
            )
            for k, v in data.items()
        }
        return kls(**data)


@dataclass
class Value(Auto):
    value: str
    creator: str
    last_set: int


@dataclass
class Channel(Auto):
    id: str
    name: str
    is_channel: bool
    created: int
    creator: str
    is_archived: bool
    is_general: bool
    name_normalized: str
    is_shared: bool
    is_org_shared: bool
    is_member: bool
    is_private: bool
    is_mpim: bool
    last_read: str
    latest: Generic
    unread_count: int
    unread_count_display: int
    members: List[str]
    topic: Value
    purpose: Value
    previous_names: List[str]


@dataclass
class Conversation(Auto):
    id: str
    name: str
    is_channel: bool
    is_group: bool
    is_im: bool
    created: int
    creator: str
    is_archived: bool
    is_general: bool
    unlinked: int
    name_normalized: str
    is_read_only: bool
    is_shared: bool
    is_ext_shared: bool
    is_org_shared: bool
    pending_shared: List[Any]
    is_pending_ext_shared: bool
    is_member: bool
    is_private: bool
    is_mpim: bool
    last_read: str
    topic: Value
    purpose: Value
    previous_names: List[str]
    num_members: int
    locale: str


@dataclass
class Event(Auto):
    token: str
    team_id: str
    api_app_id: str
    event: Generic
    type: str
    authed_users: List[str]
    event_id: str
    event_time: int


@dataclass
class File(Auto):
    id: str
    created: int
    timestamp: int
    name: str
    title: str
    mimetype: str
    filetype: str
    pretty_type: str
    user: str
    mode: str
    editable: bool
    is_external: bool
    external_type: str
    username: str
    size: int
    url_private: URL
    url_private_download: URL
    thumb_64: URL
    thumb_80: URL
    thumb_360: URL
    thumb_360_gif: URL
    thumb_360_w: int
    thumb_360_h: int
    thumb_480: URL
    thumb_480_w: int
    thumb_480_h: int
    thumb_160: URL
    permalink: URL
    permalink_public: URL
    edit_link: URL
    preview: HTML
    preview_highlight: HTML
    lines: int
    lines_more: int
    is_public: bool
    public_url_shared: bool
    display_as_bot: bool
    channels: List[str]
    groups: List[str]
    ims: List[str]
    initial_comment: Generic
    num_stars: int
    is_starred: bool
    pinned_to: List[str]
    reactions: List[Generic]
    comments_count: int


@dataclass
class Group(Auto):
    id: str
    name: str
    is_group: bool
    created: int
    creator: str
    is_archived: bool
    is_mpim: bool
    members: List[str]
    topic: Value
    purpose: Value
    last_read: str
    latest: Generic
    unread_count: int
    unread_count_display: int


@dataclass
class IM(Auto):
    id: str
    is_im: bool
    user: str
    created: int
    is_user_deleted: bool


@dataclass
class MPIM(Auto):
    id: str
    name: str
    is_mpim: bool
    is_group: bool
    created: int
    creator: str
    members: List[str]
    last_read: str
    latest: Generic
    unread_count: int
    unread_count_display: int


@dataclass
class Profile(Auto):
    avatar_hash: str
    status_text: str
    status_emoji: str
    real_name: str
    display_name: str
    real_name_normalized: str
    display_name_normalized: str
    email: str
    image_24: URL
    image_32: URL
    image_48: URL
    image_72: URL
    image_192: URL
    image_512: URL
    team: str


@dataclass
class User(Auto):
    id: str
    team_id: str
    name: str
    deleted: bool
    color: str
    real_name: str
    tz: str
    tz_label: str
    tz_offset: int
    profile: Profile
    is_admin: bool
    is_owner: bool
    is_primary_owner: bool
    is_restricted: bool
    is_ultra_restricted: bool
    is_bot: bool
    is_stranger: bool
    updated: int
    is_app_user: bool
    has_2fa: bool
    locale: str


@dataclass
class UserGroup(Auto):
    id: str
    team_id: str
    is_usergroup: bool
    name: str
    description: str
    handle: str
    is_external: bool
    date_create: int
    date_update: int
    date_delete: int
    auto_type: str
    created_by: str
    updated_by: str
    deleted_by: str
    prefs: Generic
    users: List[str]
    user_count: str
