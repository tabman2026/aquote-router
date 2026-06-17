from __future__ import annotations

import pyqauto
from pyqauto.models import KlineBar, QuoteRecord


class FakeRouter:
    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def realtime_quotes(self, symbols: list[str], *, include_raw: bool = False):
        self.calls.append(("realtime_quotes", list(symbols)))
        return [QuoteRecord(symbol=symbol, price=1.0) for symbol in symbols]

    def full_realtime_quotes(self, symbols: list[str], *, include_raw: bool = False):
        self.calls.append(("full_realtime_quotes", list(symbols)))
        return [QuoteRecord(symbol=symbol, price=2.0) for symbol in symbols]

    def index_realtime(self, symbols: list[str], *, include_raw: bool = False):
        self.calls.append(("index_realtime", list(symbols)))
        return [QuoteRecord(symbol=symbol, price=3.0) for symbol in symbols]

    def minute_kline(
        self,
        symbol: str,
        *,
        period: str = "1m",
        count: int = 240,
        include_raw: bool = False,
    ):
        self.calls.append(("minute_kline", (symbol, period, count)))
        return [KlineBar(symbol=symbol, close=4.0, period=period)]

    def daily_kline(
        self,
        symbol: str,
        *,
        count: int = 120,
        include_raw: bool = False,
    ):
        self.calls.append(("daily_kline", (symbol, count)))
        return [KlineBar(symbol=symbol, close=5.0, period="1d")]

    def kline(
        self,
        symbol: str,
        *,
        period: str = "1m",
        count: int = 120,
        include_raw: bool = False,
    ):
        self.calls.append(("kline", (symbol, period, count)))
        return [KlineBar(symbol=symbol, close=6.0, period=period)]

    def diagnose(self):
        self.calls.append(("diagnose", None))
        return {"apis": ["realtime_quotes"]}


def test_public_import_exposes_simple_api() -> None:
    assert pyqauto.quote is pyqauto.quote
    assert pyqauto.kline is pyqauto.kline


def test_simple_quote_api_uses_default_router(monkeypatch) -> None:
    fake = FakeRouter()
    monkeypatch.setattr(pyqauto, "_default_router", fake)

    record = pyqauto.quote("000001")
    records = pyqauto.quotes(["000001", "600000"])

    assert record.symbol == "000001"
    assert [item.symbol for item in records] == ["000001", "600000"]
    assert fake.calls == [
        ("realtime_quotes", ["000001"]),
        ("realtime_quotes", ["000001", "600000"]),
    ]


def test_simple_kline_api_uses_default_router(monkeypatch) -> None:
    fake = FakeRouter()
    monkeypatch.setattr(pyqauto, "_default_router", fake)

    bars = pyqauto.kline("000001", period="15m", count=10)

    assert bars[0].period == "15m"
    assert fake.calls == [("kline", ("000001", "15m", 10))]


def test_simple_diagnose_api_uses_default_router(monkeypatch) -> None:
    fake = FakeRouter()
    monkeypatch.setattr(pyqauto, "_default_router", fake)

    payload = pyqauto.diagnose()

    assert payload == {"apis": ["realtime_quotes"]}
    assert fake.calls == [("diagnose", None)]
