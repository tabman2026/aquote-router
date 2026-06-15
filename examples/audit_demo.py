"""Audit output demo."""

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
        records = router.realtime_quotes(["000001"])
    except QuoteRouterError as exc:
        print(f"Source request failed and audit was attempted: [{exc.code}] {exc}")
        return
    for record in records:
        print(record.to_dict())


if __name__ == "__main__":
    main()
