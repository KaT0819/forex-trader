from __future__ import annotations

import datetime
import decimal
import dataclasses
import typing as t

from utils.money import Money


@dataclasses.dataclass()
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


@dataclasses.dataclass()
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


@dataclasses.dataclass()
class Account:
    id: str
    balance: Money
    positions: t.List[Position]

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


@dataclasses.dataclass()
class Price:
    instrument: str
    time: datetime.datetime
    # price: decimal.Decimal

    @classmethod
    def from_json(cls, data: dict) -> Price:
        return Price(
            instrument=data["instrument"],
            time=datetime.datetime.utcfromtimestamp(float(data["time"])),
            # price=decimal.Decimal(data['price']),
        )
