"""Offline diagnose demo."""

import json

import pyqauto as aq
from pyqauto.exceptions import QuoteRouterError


def main() -> None:
    try:
        payload = aq.diagnose()
    except QuoteRouterError as exc:
        print(f"Local configuration failed: [{exc.code}] {exc}")
        return
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
