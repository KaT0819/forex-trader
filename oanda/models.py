from __future__ import annotations

import asyncio
import datetime
import decimal
import enum
import typing as t
from dataclasses import dataclass

from utils.money import Money


@enum.unique
class Granularity(enum.Enum):
    S5 = "S5"
    S10 = "S10"
    S15 = "S15"
    S30 = "S30"
    M1 = "M1"
    M2 = "M2"
    M4 = "M4"
    M5 = "M5"
    M10 = "M10"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H2 = "H2"
    H3 = "H3"
    H4 = "H4"
    H6 = "H6"
    H8 = "H8"
    H12 = "H12"
    D = "D"
    W = "W"
    M = "M"


@enum.unique
class OrderType(enum.Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    MARKET_IF_TOUCHED = "MARKET_IF_TOUCHED"
    TAKE_PROFIT = "TAKE_PROFIT"
    STOP_LOSS = "STOP_LOSS"
    TRAILING_STOP_LOSS = "TRAILING_STOP_LOSS"
    FIXED_PRICE = "FIXED_PRICE"


@dataclass()
class Candle:
    complete: bool
    open: decimal.Decimal
    close: decimal.Decimal
    low: decimal.Decimal
    high: decimal.Decimal
    volume: int
    time: datetime.datetime

    @classmethod
    def from_json(cls, data: dict) -> Candle:
        mid: dict = data.pop("mid")
        return Candle(
            open=decimal.Decimal(mid["o"]),
            close=decimal.Decimal(mid["c"]),
            high=decimal.Decimal(mid["h"]),
            low=decimal.Decimal(mid["l"]),
            time=datetime.datetime.fromtimestamp(float(data.pop("time"))),
            **data,
        )


@dataclass()
class Units:
    amount: int
    average_price: decimal.Decimal

    @classmethod
    def from_json(cls, data: dict) -> Units:
        average_price = data.get("averagePrice")
        return Units(
            amount=int(data["units"]),
            average_price=average_price and decimal.Decimal(average_price),
        )


@dataclass()
class Position:
    instrument: str
    long: Units
    short: Units

    @classmethod
    def from_json(cls, data: dict) -> Position:
        return Position(
            instrument=data["instrument"],
            long=Units.from_json(data["long"]),
            short=Units.from_json(data["short"]),
        )


@dataclass()
class Account:
    id: str
    balance: Money
    positions: t.List[Position]

    async def report_balance(self):
        print(self)
        while True:
            last_balance = self.balance
            await asyncio.sleep(1)
            if last_balance != self.balance:
                print(self)

    @classmethod
    def from_json(cls, data: dict) -> Account:
        return Account(
            id=data["account"]["id"],
            balance=Money(
                amount=data["account"]["balance"], currency=data["account"]["currency"]
            ),
            positions=[
                Position.from_json(position)
                for position in data["account"]["positions"]
            ],
        )


@dataclass()
class Price:
    instrument: str
    time: datetime.datetime
    asks: decimal.Decimal
    bids: decimal.Decimal

    @classmethod
    def from_json(cls, data: dict) -> Price:
        return Price(
            instrument=data["instrument"],
            time=datetime.datetime.fromtimestamp(float(data["time"])),
            asks=decimal.Decimal(data["asks"][0]["price"]),
            bids=decimal.Decimal(data["bids"][0]["price"]),
        )
