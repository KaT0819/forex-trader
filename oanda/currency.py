import oanda


class CurrencyMeta(type):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        cls._currencies = oanda.client.instruments
        return cls


class Currency(metaclass=CurrencyMeta):
    def __init__(self, code: str):
        pass
