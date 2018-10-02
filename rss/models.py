from __future__ import annotations

import dataclasses
from datetime import datetime
import typing as t


def skip_attrs_for_dataclass(data: dict, cls):
    assert dataclasses.is_dataclass(cls), f"{repr(cls)} is not a dataclass"
    field_names = {field.name for field in dataclasses.fields(cls)}
    return {k: v for k, v in data.items() if k in field_names}


@dataclasses.dataclass()
class Entry:
    id: str
    title: str
    link: str
    summary: str
    author: str
    published: datetime
    updated: datetime

    @classmethod
    def from_data(cls, data: dict) -> Entry:
        data["published"] = datetime.strptime(
            data["published"], "%a, %d %b %Y %H:%M:%S %Z"
        )
        data["updated"] = datetime.strptime(data["updated"], "%Y-%m-%dT%H:%M:%SZ")
        return Entry(**skip_attrs_for_dataclass(data, Entry))


@dataclasses.dataclass()
class Feed:
    language: str
    title: str
    link: str
    subtitle: str
    entries: t.List[Entry]

    @classmethod
    def from_data(cls, data: dict) -> Feed:
        data["entries"] = [Entry.from_data(entry) for entry in data["entries"]]
        return Feed(
            **skip_attrs_for_dataclass(data, Feed),
            **skip_attrs_for_dataclass(data["feed"], Feed),
        )
