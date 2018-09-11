import asyncio
import datetime

import typing as t

from oanda.api import OandaApi
from utils.singleton import Singleton
from . import config, models

PriceListener = t.Callable[[models.Price], t.Any]

loop = asyncio.get_event_loop()


class Prices(metaclass=Singleton):
    _listeners: t.Dict[str, t.List[PriceListener]] = {}

    async def subscribe(self, instrument: str, listener: PriceListener):
        if instrument not in self._listeners:
            start_loop = not bool(self._listeners)
            prices = await OandaApi().pricing(
                config.OANDA_ACCOUNT_ID,
                instruments=[instrument],
                since=datetime.datetime.now(),
            )
            print(prices)
            for price in prices:
                listener(price)
            self._listeners[instrument] = [listener]
            if start_loop:
                asyncio.ensure_future(self.run_forever())
        else:
            self._listeners[instrument].append(listener)

    async def run_forever(self):
        instruments = self._listeners.keys()
        async for price in OandaApi().stream_pricing(
            config.OANDA_ACCOUNT_ID, instruments
        ):
            for listener in self._listeners[price.instrument]:
                listener(price)
            if instruments != self._listeners.keys():
                if self._listeners.keys():
                    asyncio.ensure_future(self.run_forever())
                break
