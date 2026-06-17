"""Unified K-line API demo."""

import pyqauto as aq
from pyqauto.exceptions import QuoteRouterError


def main() -> None:
    try:
        minute_bars = aq.kline("000001", period="15m", count=120)
        daily_bars = aq.kline("000001", period="1d", count=120)
    except QuoteRouterError as exc:
        print(f"Source request failed: [{exc.code}] {exc}")
        return
    print({"minute_sample": [bar.to_dict() for bar in minute_bars[:1]]})
    print({"daily_sample": [bar.to_dict() for bar in daily_bars[:1]]})


if __name__ == "__main__":
    main()
