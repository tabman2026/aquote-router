from __future__ import annotations

import pytest
from test_router_fallback import FakeAdapter, make_router

from aquote_router.adapters.pytdx_adapter import PYTDX_KLINE_PERIOD_CATEGORIES
from aquote_router.exceptions import UnsupportedPeriodError
from aquote_router.policy import SUPPORTED_MINUTE_KLINE_PERIODS


def test_pytdx_period_mapping_covers_supported_minute_periods() -> None:
    assert PYTDX_KLINE_PERIOD_CATEGORIES["1m"] == 7
    assert PYTDX_KLINE_PERIOD_CATEGORIES["5m"] == 0
    assert PYTDX_KLINE_PERIOD_CATEGORIES["15m"] == 1
    assert PYTDX_KLINE_PERIOD_CATEGORIES["30m"] == 2
    assert PYTDX_KLINE_PERIOD_CATEGORIES["60m"] == 3

    for period in SUPPORTED_MINUTE_KLINE_PERIODS:
        assert period in PYTDX_KLINE_PERIOD_CATEGORIES


@pytest.mark.parametrize("period", ["1m", "5m", "15m", "30m", "60m"])
def test_minute_kline_accepts_supported_periods(period: str) -> None:
    adapter = FakeAdapter("pytdx", "primary")
    router = make_router([adapter])

    bars = router.minute_kline("000001", period=period, count=240)

    assert bars[0].period == period
    assert adapter.calls == [f"minute_kline:{period}:240"]


def test_minute_kline_rejects_unsupported_period() -> None:
    router = make_router([FakeAdapter("pytdx", "primary")])

    with pytest.raises(UnsupportedPeriodError):
        router.minute_kline("000001", period="2m")
