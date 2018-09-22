import warnings
from dataclasses import dataclass

import colorama

from oanda import models
from utils.money import Money


@dataclass()
class BalanceListener:
    account: models.Account

    def __post_init__(self):
        print(
            colorama.Style.BRIGHT
            + colorama.Fore.WHITE
            + repr(self)
            + colorama.Style.RESET_ALL
        )

    def balance_changed(self, new_balance: Money):
        if new_balance > self.account.balance:
            print(
                colorama.Style.BRIGHT
                + colorama.Fore.GREEN
                + f"+{new_balance - self.account.balance} => {new_balance}"
                + colorama.Style.RESET_ALL
            )
        elif new_balance < self.account.balance:
            print(
                colorama.Style.BRIGHT
                + colorama.Fore.GREEN
                + f"+{new_balance - self.account.balance} => {new_balance}"
                + colorama.Style.RESET_ALL
            )
        else:
            warnings.warn(f"(Undefined state) Balance did not change")

    async def feed_transaction(self, transaction: models.Transaction):
        if transaction.account_id == self.account.id and isinstance(
            transaction,
            (
                models.TransferFundsTransaction,
                models.DailyFinancingTransaction,
                models.OrderFillTransaction,
            ),
        ):
            self.account.balance = transaction.account_balance
