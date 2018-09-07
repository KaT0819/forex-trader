import asyncio
import typing as t

from oanda import models
from oanda.prices import Prices


class Trader:
    def __init__(self, account: models.Account, instruments: t.List[str]):
        self.account = account
        self.instruments = instruments
        self.prices: t.Dict[str, t.List[models.Price]] = {
            i: [] for i in self.instruments
        }

    def __repr__(self):
        return f"<Trader(account={self.account})>"

    async def run_forever(self):
        for instrument in self.instruments:
            await Prices().subscribe(instrument=instrument, listener=self.listen)
        while True:
            print(self.prices)
            await asyncio.sleep(1)

    def listen(self, price: models.Price):
        if not self.prices[price.instrument] or price != self.prices[price.instrument][-1]:
            self.prices[price.instrument].append(price)
