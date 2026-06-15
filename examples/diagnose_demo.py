"""Offline diagnose demo."""

import json

from aquote_router import QuoteRouter
from aquote_router.exceptions import QuoteRouterError


def main() -> None:
    try:
        router = QuoteRouter.from_config(
            pytdx_servers_path="config/pytdx_servers.example.json",
            source_policy_path="config/source_policy.example.yaml",
        )
    except QuoteRouterError as exc:
        print(f"Local configuration failed: [{exc.code}] {exc}")
        return
    print(json.dumps(router.diagnose(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
