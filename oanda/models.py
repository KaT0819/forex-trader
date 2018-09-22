from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from decimal import Decimal
import enum
import typing as t

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
    open: Decimal
    close: Decimal
    low: Decimal
    high: Decimal
    volume: int
    time: datetime

    @classmethod
    def from_json(cls, data: dict) -> Candle:
        mid: dict = data.pop("mid")
        return Candle(
            open=Decimal(mid["o"]),
            close=Decimal(mid["c"]),
            high=Decimal(mid["h"]),
            low=Decimal(mid["l"]),
            time=datetime.fromtimestamp(float(data.pop("time"))),
            **data,
        )


@dataclass()
class Units:
    amount: int
    average_price: t.Optional[Decimal]

    @classmethod
    def from_json(cls, data: dict) -> Units:
        average_price = data.get("averagePrice")
        return Units(
            amount=int(data["units"]),
            average_price=Decimal(average_price) if average_price else None,
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
class PriceBucket:
    price: Decimal
    liquidity: int

    @classmethod
    def from_json(cls, data: dict) -> PriceBucket:
        return PriceBucket(
            price=Decimal(data["price"]), liquidity=int(data["liquidity"])
        )


@dataclass()
class Price:
    instrument: str
    time: datetime
    tradeable: bool
    asks: t.List[PriceBucket]
    bids: t.List[PriceBucket]
    closeout_bid: Decimal
    closeout_ask: Decimal

    @classmethod
    def from_json(cls, data: dict) -> Price:
        assert data["type"] == "PRICE"
        return Price(
            instrument=data["instrument"],
            tradeable=data["tradeable"],
            time=datetime.fromtimestamp(float(data["time"])),
            closeout_bid=Decimal(data["closeoutBid"]),
            closeout_ask=Decimal(data["closeoutAsk"]),
            asks=[PriceBucket.from_json(d) for d in data["asks"]],
            bids=[PriceBucket.from_json(d) for d in data["bids"]],
        )

    @property
    def spread(self) -> Decimal:
        return (self.asks - self.bids) / self.asks


@dataclass()
class TransactionHeartbeat:
    time: datetime
    last_transaction_id: int

    @classmethod
    def from_json(cls, data: dict) -> TransactionHeartbeat:
        return TransactionHeartbeat(
            time=datetime.fromtimestamp(float(data["time"])),
            last_transaction_id=int(data["lastTransactionID"]),
        )


@dataclass()
class Transaction:
    id: int
    time: datetime
    account_id: str

    @classmethod
    def from_json(cls, data: dict) -> Transaction:
        return Transaction(
            id=int(data["id"]),
            time=datetime.fromtimestamp(float(data["time"])),
            account_id=data["accountID"],
        )


@dataclass()
class TransferFundsTransaction(Transaction):
    account_balance: Decimal

    @classmethod
    def from_json(cls, data: dict) -> DailyFinancingTransaction:
        return DailyFinancingTransaction(
            account_balance=Decimal(data["accountBalance"]),
            **asdict(Transaction.from_json(data)),
        )


@dataclass()
class OrderFillTransaction(Transaction):
    account_balance: Decimal

    @classmethod
    def from_json(cls, data: dict) -> DailyFinancingTransaction:
        return DailyFinancingTransaction(
            account_balance=Decimal(data["accountBalance"]),
            **asdict(Transaction.from_json(data)),
        )


@dataclass()
class DailyFinancingTransaction(Transaction):
    account_balance: Decimal

    @classmethod
    def from_json(cls, data: dict) -> DailyFinancingTransaction:
        return DailyFinancingTransaction(
            account_balance=Decimal(data["accountBalance"]),
            **asdict(Transaction.from_json(data)),
        )
