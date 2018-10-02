import asyncio
import typing as t
from dataclasses import dataclass
from pprint import pprint

import aiohttp
import feedparser

from . import models


@dataclass()
class RssFeed:
    url: str
    _feed: t.Optional[models.Feed] = None

    @property
    async def feed(self):
        if not self._feed:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    data = await response.content.read()
                    pprint(feedparser.parse(data))
                    self._feed = models.Feed.from_data(feedparser.parse(data))
        return self._feed

    async def listen(self) -> t.AsyncIterable[models.Entry]:
        while True:
            await asyncio.sleep(60)
            entries = self._feed.entries.copy()
            new_feed = await self.feed
            if entries != new_feed.entries:
                for entry in new_feed.entries:
                    if entry not in entries:
                        yield entry
