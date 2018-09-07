from decimal import Decimal, ROUND_HALF_UP


class Money:
    def __init__(self, currency: str, amount: float):
        self.currency: str = currency
        self.amount = Decimal(amount)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Money)
            and self.currency == other.currency
            and self.amount == other.amount
        )

    def __ne__(self, other: "Money") -> bool:
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

    def __str__(self) -> str:
        return f"{self.amount:,} {self.currency}"

    def __repr__(self) -> str:
        return f"<Money: {self}>"
