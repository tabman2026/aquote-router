"""Audit output demo."""

import pyqauto as aq
from pyqauto.exceptions import QuoteRouterError


def main() -> None:
    aq.configure(
        audit_jsonl_path="logs/pyqauto_audit.jsonl",
        audit_sqlite_path="logs/pyqauto_audit.sqlite3",
    )
    try:
        records = aq.quotes(["000001"])
    except QuoteRouterError as exc:
        print(f"Source request failed and audit was attempted: [{exc.code}] {exc}")
        return
    for record in records:
        print(record.to_dict())


if __name__ == "__main__":
    main()
