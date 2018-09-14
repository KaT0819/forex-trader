import enum
import typing as t
import dataclasses
from datetime import datetime, timedelta

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

    async def learn(self) -> None:
        raise NotImplementedError

    def feed(self, price: models.Price) -> StrategyDecision:
        raise NotImplementedError


class MomentumStrategy(Strategy):
    async def learn(self) -> None:
        candles = await OandaApi().candles(
            instrument=self.instrument,
            timeframe=(datetime.now() - timedelta(hours=1), datetime.now()),
        )
        data_frame = pandas.DataFrame(
            (dataclasses.asdict(c) for c in candles)
        ).set_index("time")
        data_frame.index = pandas.DatetimeIndex(data_frame.index)

        # plotly.plot([graph_objs.Candlestick(
        #     x=data_frame.index,
        #     open=data_frame.open,
        #     close=data_frame.close,
        #     high=data_frame.high,
        #     low=data_frame.low,
        # )], filename=f'{self.instrument}')

    def feed(self, price: models.Price) -> StrategyDecision:
        return StrategyDecision.DO_NOTHING
