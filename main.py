#!/usr/bin/env python

import asyncio

import plotly

from aiohttp import web

import oanda
from oanda import models
from oanda.api import OandaApi
from trader.listeners import BalanceListener
from trader.trader import Trader
import server
from config import config


def setup():
    plotly.tools.set_credentials_file(
        username=config["plotly"]["username"], api_key=config["plotly"]["api_key"]
    )


async def listen_on_transactions(account: models.Account):
    listeners = [BalanceListener(account)]
    async for transaction in OandaApi().stream_transactions(account_id=account.id):
        for listener in listeners:
            await listener.feed_transaction(transaction)


async def main():
    account = await oanda.api.OandaApi().account(
        account_id=oanda.config.OANDA_ACCOUNT_ID
    )
    asyncio.ensure_future(listen_on_transactions(account))

    instruments = ["USD_PLN", "EUR_USD"]
    for trader in [
        Trader(account=account, instrument=instrument) for instrument in instruments
    ]:
        asyncio.ensure_future(trader.run_forever())


setup()
asyncio.ensure_future(main())

app = web.Application()
app.add_routes(server.views.routes)
web.run_app(app)
