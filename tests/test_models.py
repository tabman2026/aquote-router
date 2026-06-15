from __future__ import annotations

from dataclasses import fields

from aquote_router.models import KlineBar, QuoteRecord


def test_quote_record_omits_raw_by_default() -> None:
    record = QuoteRecord(symbol="000001", price=1.23, raw={"large": "payload"})

    data = record.to_dict()

    assert data["symbol"] == "000001"
    assert "raw" not in data


def test_quote_record_can_include_raw() -> None:
    record = QuoteRecord(symbol="000001", raw={"field": "value"})

    data = record.to_dict(include_raw=True)

    assert data["raw"] == {"field": "value"}


def test_kline_bar_fields_are_complete() -> None:
    field_names = {field.name for field in fields(KlineBar)}

    for name in [
        "symbol",
        "datetime",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "period",
        "source",
        "source_level",
        "raw",
    ]:
        assert name in field_names


def test_kline_bar_omits_raw_by_default_and_keeps_period() -> None:
    bar = KlineBar(
        symbol="000001",
        close=10.1,
        period="15m",
        source="pytdx",
        source_level="primary",
        raw={"close": 10.1},
    )

    data = bar.to_dict()

    assert data["period"] == "15m"
    assert data["close"] == 10.1
    assert bar.price == 10.1
    assert "raw" not in data
