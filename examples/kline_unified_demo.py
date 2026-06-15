"""Unified K-line API demo."""

from aquote_router import QuoteRouter
from aquote_router.exceptions import QuoteRouterError


def main() -> None:
    router = QuoteRouter.from_config(
        pytdx_servers_path="config/pytdx_servers.example.json",
        source_policy_path="config/source_policy.example.yaml",
        audit_jsonl_path="logs/aquote_router_audit.jsonl",
        audit_sqlite_path="logs/aquote_router_audit.sqlite3",
    )
    try:
        minute_bars = router.kline("000001", period="15m", count=120)
        daily_bars = router.kline("000001", period="1d", count=120)
    except QuoteRouterError as exc:
        print(f"Source request failed: [{exc.code}] {exc}")
        return
    print({"minute_sample": [bar.to_dict() for bar in minute_bars[:1]]})
    print({"daily_sample": [bar.to_dict() for bar in daily_bars[:1]]})


if __name__ == "__main__":
    main()
