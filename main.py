#!/usr/bin/env python

import asyncio

import oanda
from trader.trader import Trader


async def main():
    account = await oanda.api.OandaApi().account(oanda.config.OANDA_ACCOUNT_ID)
    trader = Trader(account=account, instruments=["USD_PLN", "EUR_USD"])
    await trader.run_forever()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
