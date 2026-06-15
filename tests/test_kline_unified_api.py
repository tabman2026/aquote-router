from __future__ import annotations

import pytest
from test_router_fallback import FakeAdapter, make_router

from aquote_router.exceptions import UnsupportedPeriodError


def test_kline_routes_minute_periods_to_minute_kline() -> None:
    adapter = FakeAdapter("pytdx", "primary")
    router = make_router([adapter])

    bars = router.kline("000001", period="15m", count=120)

    assert bars[0].period == "15m"
    assert adapter.calls == ["minute_kline:15m:120"]


@pytest.mark.parametrize("period", ["1d", "daily", "day"])
def test_kline_routes_daily_aliases_to_daily_kline(period: str) -> None:
    adapter = FakeAdapter("pytdx", "primary")
    router = make_router([adapter])

    bars = router.kline("000001", period=period, count=120)

    assert bars[0].period == "1d"
    assert adapter.calls == ["daily_kline:120"]


def test_kline_rejects_unsupported_period() -> None:
    router = make_router([FakeAdapter("pytdx", "primary")])

    with pytest.raises(UnsupportedPeriodError):
        router.kline("000001", period="2m")
