import enum
import typing as t
import dataclasses
from collections import deque
from datetime import datetime, timedelta
from decimal import Decimal

import pandas

import plotly.plotly as plotly
from plotly import graph_objs
from plotly.plotly import iplot

from oanda import models
from oanda.api import OandaApi


class StrategyDecision(enum.Enum):
    DO_NOTHING = 0
    BUY = 1
    SELL = 2


@dataclasses.dataclass()
class Strategy:
    instrument: str
    period: timedelta = timedelta(minutes=1)

    position: t.Optional[models.Position] = None
    history: t.List[models.Price] = dataclasses.field(default_factory=list)

    async def learn(self) -> None:
        raise NotImplementedError

    def feed(self, price: models.Price) -> StrategyDecision:
        raise NotImplementedError

    async def buy(self):
        OandaApi().create_order()

    @property
    def profit(self) -> float:
        if not self.history or not self.position:
            return 0
        current_price = self.history[-1]
        return (
            current_price.bids - self.position.long.average_price
        ) / current_price.bids


class MomentumStrategy(Strategy):
    async def learn(self) -> None:
        pass

    def get_profits(self) -> t.Iterator[t.Tuple[float, datetime]]:
        last_price = self.history[0]
        for price in self.history[1:]:
            yield (price.asks - last_price.asks) / last_price.asks, price.time
            last_price = price

    def get_momentum(self) -> float:
        profits = self.get_profits()

        try:
            last_asks, last_time = next(profits)
        except StopIteration:
            return 0
        momentum = 0
        for asks, time in profits:
            momentum += float(last_asks + asks) / 2 * (time - last_time).total_seconds()
            last_asks, last_time = asks, time
        return momentum

    def feed(self, price: models.Price) -> StrategyDecision:
        while self.history and self.history[0].time < datetime.now() - self.period:
            self.history.pop(0)

        if self.history:
            initial_profit = (
                price.closeout_bid - price.closeout_ask
            ) / price.closeout_bid
            gain = (self.history[-1].closeout_ask - price.closeout_ask) / self.history[
                -1
            ].closeout_ask
            print(
                price.asks,
                "initial profit",
                initial_profit,
                "gain",
                gain,
                gain > -initial_profit,
            )
        self.history.append(price)

        if not self.ready:
            return StrategyDecision.DO_NOTHING

        momentum = self.get_momentum()
        # print(f"momentum: ", momentum, price)
        if momentum >= 0.1:
            return StrategyDecision.BUY
        elif momentum < -0.1:
            return StrategyDecision.SELL
        return StrategyDecision.DO_NOTHING

    @property
    def ready(self) -> bool:
        return (
            self.history
            and (datetime.now() - self.history[0].time) > 0.9 * self.period
            and (datetime.now() - self.history[-1].time) < 0.1 * self.period
        )
