"""Daily K-line demo."""

import pyqauto as aq
from pyqauto.exceptions import QuoteRouterError


def main() -> None:
    try:
        bars = aq.daily("000001", count=120)
    except QuoteRouterError as exc:
        print(f"Source request failed: [{exc.code}] {exc}")
        return
    for bar in bars:
        print(bar.to_dict())


if __name__ == "__main__":
    main()
