import typing as t

from dataclasses import dataclass
from datetime import datetime


@dataclass()
class Entry:
    title: str
    link: str
    summary: str
    author: str
    published: datetime
    updated: datetime


@dataclass()
class Feed:
    language: str
    title: str
    link: str
    subtitle: str
    entries: t.List[Entry]
