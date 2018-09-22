from decimal import Decimal


class Money:
    def __init__(self, currency: str, amount: float) -> None:
        self.currency: str = currency
        self.amount = Decimal(amount)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Money)
            and self.currency == other.currency
            and self.amount == other.amount
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __gt__(self, other: "Money") -> bool:
        assert isinstance(other, Money), f"Expected `{other}` to be of type Money"
        if self.currency != other.currency:
            raise TypeError("Cannot compare different currencies")
        return self.amount > other.amount

    def __ge__(self, other: "Money") -> bool:
        return self.__gt__(other) or self.__eq__(other)

    def __lt__(self, other: "Money") -> bool:
        return not self.__ge__(other)

    def __le__(self, other: "Money") -> bool:
        return not self.__gt__(other)

    def __sub__(self, other):
        if isinstance(other, Money) and self.currency == other.currency:
            return Money(currency=self.currency, amount=self.amount - other.amount)
        raise ValueError(f"Invalid value {repr(other)}")

    def __add__(self, other):
        return self - -other

    def __neg__(self):
        return Money(currency=self.currency, amount=-self.amount)

    def __str__(self) -> str:
        return f"{self.amount:,} {self.currency}"

    def __repr__(self) -> str:
        return f"<Money: {self}>"
