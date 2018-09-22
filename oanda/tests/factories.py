from datetime import datetime, timedelta
import random

import factory.fuzzy

import pytz

from .. import models


def instrument_factory():
    return random.choice(["EUR_USD", "USD_PLN"])


class PriceFactory(factory.Factory):
    class Meta:
        model = models.Price

    instrument = factory.LazyFunction(instrument_factory)
    time = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.now(pytz.utc) - timedelta(hours=5),
        end_dt=datetime.now(pytz.utc),
    )
    asks = factory.fuzzy.FuzzyDecimal(low=0.5, high=4.0)
    bids = factory.fuzzy.FuzzyDecimal(low=0.5, high=4.0)
