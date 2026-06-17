"""Realtime quote demo."""

import pyqauto as aq
from pyqauto.exceptions import QuoteRouterError


def main() -> None:
    try:
        records = aq.quotes(["000001", "600000"])
    except QuoteRouterError as exc:
        print(f"Source request failed: [{exc.code}] {exc}")
        return
    for record in records:
        print(record.to_dict())


if __name__ == "__main__":
    main()
