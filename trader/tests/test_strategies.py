from datetime import datetime
import typing as t

import pytest

from oanda.tests import factories
from ..strategies import Strategy, MomentumStrategy


class TestStrategy:
    def test_health(self):
        pass


class TestMomentumStrategy:
    @pytest.mark.parametrize(
        "prices, momentum",
        (
            ([factories.PriceFactory()], 0.0),
            ([factories.PriceFactory(), factories.PriceFactory()], 0.0),
            (
                [
                    factories.PriceFactory(asks=1, time=datetime(2018, 1, 1, 0, 0)),
                    factories.PriceFactory(asks=1.5, time=datetime(2018, 1, 1, 0, 1)),
                    factories.PriceFactory(asks=0.75, time=datetime(2018, 1, 1, 0, 2)),
                ],
                0.0,
            ),
            (
                [
                    factories.PriceFactory(asks=1, time=datetime(2018, 1, 1, 0, 0, 0)),
                    factories.PriceFactory(asks=2, time=datetime(2018, 1, 1, 0, 0, 1)),
                    factories.PriceFactory(asks=2, time=datetime(2018, 1, 1, 0, 0, 2)),
                ],
                0.5,
            ),
            (
                [
                    factories.PriceFactory(asks=2, time=datetime(2018, 1, 1, 0, 0, 0)),
                    factories.PriceFactory(asks=4, time=datetime(2018, 1, 1, 0, 0, 1)),
                    factories.PriceFactory(asks=4, time=datetime(2018, 1, 1, 0, 0, 2)),
                    factories.PriceFactory(asks=2, time=datetime(2018, 1, 1, 0, 0, 3)),
                    factories.PriceFactory(asks=0, time=datetime(2018, 1, 1, 0, 0, 4)),
                ],
                -0.5,
            ),
        ),
    )
    def test_get_momentum(self, prices: t.List[factories.models.Price], momentum: str):
        strategy = MomentumStrategy(
            instrument=factories.instrument_factory(), history=prices
        )
        assert momentum == strategy.get_momentum()
