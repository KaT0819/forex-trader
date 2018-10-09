#!/usr/bin/env python

import argparse
import asyncio
import sys

import plotly

from aiohttp import web
from django.core.management import execute_from_command_line

import oanda
from oanda import models
from oanda.api import OandaApi
from trader.listeners import BalanceListener
from trader.trader import Trader
import server
from config import config


class App:
    def __init__(self):
        from django.conf import settings

        settings.configure(
            INSTALLED_APPS=["trader"],
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": "forex.sqlite3",
                }
            },
        )
        plotly.tools.set_credentials_file(
            username=config["plotly"]["username"], api_key=config["plotly"]["api_key"]
        )

    async def listen_on_transactions(self, account: models.Account):
        listeners = [BalanceListener(account)]
        async for transaction in OandaApi().stream_transactions(account_id=account.id):
            for listener in listeners:
                await listener.feed_transaction(transaction)

    async def run_traders(self):
        account = await oanda.api.OandaApi().account(
            account_id=oanda.config.OANDA_ACCOUNT_ID
        )
        asyncio.ensure_future(self.listen_on_transactions(account))

        instruments = ["USD_PLN", "EUR_USD"]
        for trader in [
            Trader(account=account, instrument=instrument) for instrument in instruments
        ]:
            asyncio.ensure_future(trader.run_forever())

    def run_server(self):
        asyncio.ensure_future(self.run_traders())

        app = web.Application()
        app.add_routes(server.views.routes)
        web.run_app(app, port="8000")

    def run_django_command(self):
        execute_from_command_line(sys.argv)


parser = argparse.ArgumentParser()
parser.add_argument("command", type=str)

parsed = parser.parse_args(sys.argv[1:])

app = App()

if parsed.command == "runserver":
    app.run_server()
else:
    app.run_django_command()
