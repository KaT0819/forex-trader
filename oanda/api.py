import json
import datetime
import typing as t
import warnings
from decimal import Decimal

import aiohttp

from utils.singleton import Singleton
from . import config, models


class OandaException(Exception):
    pass


class OandaApi(metaclass=Singleton):
    headers = {
        "Authorization": f"Bearer {config.OANDA_TOKEN}",
        "Accept-Datetime-Format": config.OANDA_DATETIME_FORMAT,
        "Content-Type": "application/json",
    }

    @classmethod
    async def _call_endpoint(cls, method: str, path: str, **kwargs) -> dict:
        kwargs["params"] = {
            k: v for k, v in kwargs.get("params", {}).items() if v is not None
        }
        if "data" in kwargs:
            kwargs["data"] = json.dumps(kwargs["data"])
        async with aiohttp.ClientSession() as session:
            async with getattr(session, method.lower())(
                url=f"{config.OANDA_URL}{path}", headers=cls.headers, **kwargs
            ) as response:
                data = await response.json()
                cls._catch_errors(data)
                return data

    @classmethod
    async def _stream_endpoint(
        cls, method, path: str, **kwargs
    ) -> t.AsyncIterable[dict]:
        kwargs["params"] = {
            k: v for k, v in kwargs.get("params", {}).items() if v is not None
        }
        async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=0)  # type: ignore
        ) as session:
            async with getattr(session, method.lower())(
                url=f"{config.OANDA_STREAMING_URL}{path}", headers=cls.headers, **kwargs
            ) as response:
                async for chunk, _ in response.content.iter_chunks():  # type: bytes, int
                    for line in chunk.strip(b"\n").split(b"\n"):
                        data = json.loads(line.decode())
                        cls._catch_errors(data)
                        yield data

    @classmethod
    def _catch_errors(cls, data: dict):
        if "errorMessage" in data:
            raise OandaException(data["errorMessage"])

    async def account(self, *, account_id: str):
        data = await self._call_endpoint(method="get", path=f"/accounts/{account_id}")
        return models.Account.from_json(data)

    async def instruments(self, *, account_id: str) -> t.Iterable[str]:
        data = await self._call_endpoint(
            method="get", path=f"/accounts/{account_id}/instruments/"
        )
        return (i["name"] for i in data["instruments"])

    async def pricing(
        self,
        *,
        account_id: str,
        instruments: t.Iterable[str],
        since: datetime.datetime = None,
    ) -> t.Iterable[models.Price]:
        data = await self._call_endpoint(
            method="get",
            path=f"/accounts/{account_id}/pricing/",
            params={
                "instruments": ",".join(instruments),
                "since": since and int(since.timestamp()),
            },
        )
        return (models.Price.from_json(p) for p in data["prices"])

    async def stream_pricing(
        self, *, account_id: str, instruments: t.Iterable[str]
    ) -> t.AsyncIterable[models.Price]:
        async for data in self._stream_endpoint(
            method="get",
            path=f"/accounts/{account_id}/pricing/stream/",
            params={"instruments": ",".join(instruments)},
        ):
            if data["type"] == "HEARTBEAT":
                pass
            elif data["type"] == "PRICE":
                yield models.Price.from_json(data)
            else:
                warnings.warn(f"(Unhandled payload in stream_pricing) {data}")

    async def candles(
        self,
        *,
        instrument: str,
        timeframe: t.Tuple[datetime.datetime, datetime.datetime],
        granularity: models.Granularity = models.Granularity.S5,
    ) -> t.Iterable[models.Candle]:
        data = await self._call_endpoint(
            method="get",
            path=f"/instruments/{instrument}/candles/",
            params={
                "from": str(timeframe[0].timestamp()),
                "to": str(timeframe[1].timestamp()),
                "granularity": granularity.value,
            },
        )
        return (models.Candle.from_json(c) for c in data["candles"])

    async def create_order(
        self,
        *,
        account_id: str,
        instrument: str,
        units: int,
        order_type: models.OrderType = models.OrderType.MARKET,
    ):
        data = await self._call_endpoint(
            method="post",
            path=f"/accounts/{account_id}/orders/",
            data={
                "order": {
                    "instrument": instrument,
                    "units": units,
                    "type": order_type.value,
                }
            },
        )
        print()
        print(data)
        print()
        return data

    async def close_position(
        self,
        *,
        account_id: str,
        instrument: str,
        short_units: Decimal,
        long_units: Decimal,
    ):
        data = await self._call_endpoint(
            method="put",
            path=f"/accounts/{account_id}/positions/{instrument}/close/",
            data={"shortUnits": str(short_units), "longUnits": str(long_units)},
        )
        print()
        print(data)
        print()
        return data

    async def stream_transactions(
        self, *, account_id: str
    ) -> t.AsyncIterable[models.Transaction]:
        last_transaction_id: t.Optional[int] = None
        async for data in self._stream_endpoint(
            method="get", path=f"/accounts/{account_id}/transactions/stream/"
        ):
            if data["type"] == "HEARTBEAT":
                heartbeat = models.TransactionHeartbeat.from_json(data)
                if (
                    last_transaction_id
                    and last_transaction_id != heartbeat.last_transaction_id
                ):
                    warnings.warn(
                        f"(Streaming issue) Transactions "
                        f"{last_transaction_id}-{heartbeat.last_transaction_id} have not been captured"
                    )
                continue
            last_transaction_id = int(data["id"])

            if data["type"] == "DAILY_FINANCING":
                yield models.DailyFinancingTransaction.from_json(data)
            elif data["type"] == "TRANSFER_FUNDS":
                yield models.TransferFundsTransaction.from_json(data)
            elif data["type"] == "ORDER_FILL":
                yield models.OrderFillTransaction.from_json(data)
            else:
                warnings.warn(f"(Unhandled payload in stream_transactions) {data}")
