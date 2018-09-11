import asyncio
from datetime import datetime, timedelta
import typing as t

from oanda import models
from oanda.api import OandaApi
from oanda.prices import Prices

from .strategies import Strategy


class Trader:
    def __init__(self, account: models.Account, instruments: t.List[str]):
        self.account = account
        self.instruments = instruments
        self.strategy = Strategy()

    def __repr__(self):
        return f"<Trader(account={self.account})>"

    async def run_forever(self):
        candles = await OandaApi().candles(
            instrument="EUR_USD",
            timeframe=(datetime.now() - timedelta(hours=1), datetime.now()),
        )
        self.strategy.learn(candles)
        asyncio.ensure_future(self.account.report_balance())
        for instrument in self.instruments:
            await Prices().subscribe(instrument=instrument, listener=self.listen)
        while True:
            await asyncio.sleep(1)

    def listen(self, price: models.Price):
        pass
