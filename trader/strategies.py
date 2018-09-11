import enum
import typing as t
import dataclasses

import pandas

from oanda import models


class StrategyDecision(enum.Enum):
    DO_NOTHING = 0
    BUY = 1
    SELL = 2


class Strategy:
    def learn(self, candles: t.Iterable[models.Candle]):
        dataframe = pandas.DataFrame(
            (dataclasses.asdict(c) for c in candles)
        ).set_index("time")
        print(dataframe)
        print(dataframe.info())

    def feed(self, price: models.Price) -> StrategyDecision:
        pass
