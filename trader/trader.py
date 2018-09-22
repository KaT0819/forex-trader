from datetime import timedelta

from oanda import models
from oanda.prices import Prices

from .strategies import MomentumStrategy, StrategyDecision


class Trader:
    def __init__(self, account: models.Account, instrument: str) -> None:
        self.account = account
        self.instrument = instrument
        self.strategy = MomentumStrategy(
            instrument=self.instrument, period=timedelta(seconds=30)
        )

    def __repr__(self):
        return f"<Trader(instrument={self.instrument})>"

    async def run_forever(self) -> None:
        await self.strategy.learn()
        await Prices().subscribe(instrument=self.instrument, listener=self.listen)

    def listen(self, price: models.Price):
        decision = self.strategy.feed(price)
        if decision == StrategyDecision.SELL:
            pass

        elif decision == StrategyDecision.BUY:
            pass

        elif decision == StrategyDecision.DO_NOTHING:
            pass
