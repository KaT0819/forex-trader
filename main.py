#!/usr/bin/env python

import plotly

import asyncio

import oanda
from oanda import models
from trader.trader import Trader


def setup():
    plotly.tools.set_credentials_file(
        username="karol-gruszczyk", api_key="7t1SnfeRfsKEUxD1zMrJ"
    )


async def main():
    account = await oanda.api.OandaApi().account(
        account_id=oanda.config.OANDA_ACCOUNT_ID
    )
    asyncio.ensure_future(account.run_forever())
    instruments = ["USD_PLN", "EUR_USD"]
    for trader in [
        Trader(account=account, instrument=instrument) for instrument in instruments
    ]:
        asyncio.ensure_future(trader.run_forever())
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    setup()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        pass
