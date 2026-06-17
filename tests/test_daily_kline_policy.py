from __future__ import annotations

from test_router_fallback import FakeAdapter, make_router

from pyqauto.adapters.pytdx_adapter import PYTDX_KLINE_PERIOD_CATEGORIES


def test_pytdx_period_mapping_contains_daily() -> None:
    assert PYTDX_KLINE_PERIOD_CATEGORIES["1d"] == 4


def test_daily_kline_uses_pytdx_daily_period() -> None:
    adapter = FakeAdapter("pytdx", "primary")
    router = make_router([adapter])

    bars = router.daily_kline("000001", count=120)

    assert bars[0].period == "1d"
    assert adapter.calls == ["daily_kline:120"]


def test_daily_kline_policy_is_pytdx_only() -> None:
    router = make_router([FakeAdapter("pytdx", "primary")])

    api_policy = router.policy.api("daily_kline")

    assert api_policy.allow_fallback is False
    assert api_policy.fallback_order == ["pytdx"]
