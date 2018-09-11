#!/usr/bin/env python

import asyncio

import oanda
from trader.trader import Trader


async def main():
    # await oanda.api.OandaApi().create_order(
    #     account_id=oanda.config.OANDA_ACCOUNT_ID, instrument="EUR_USD", units=1
    # )
    account = await oanda.api.OandaApi().account(
        account_id=oanda.config.OANDA_ACCOUNT_ID
    )
    print(account)
    # trader = Trader(account=account, instruments=["USD_PLN", "EUR_USD"])
    # await trader.run_forever()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
