# Quickstart

## Install

```bash
python -X utf8 -m pip install aquote-router
```

For local development:

```bash
python -X utf8 -m pip install -e ".[dev,test]"
```

## Python

```python
from aquote_router import QuoteRouter

router = QuoteRouter.from_config(
    pytdx_servers_path="config/pytdx_servers.example.json",
    source_policy_path="config/source_policy.example.yaml",
)

print([record.to_dict() for record in router.realtime_quotes(["000001"])])
print([bar.to_dict() for bar in router.kline("000001", period="15m", count=120)])
```

## CLI

```bash
aquote-router realtime 000001 600000 --json
aquote-router kline 000001 --period 1d --count 120 --json
aquote-router diagnose --json
```

Live upstream availability can change. Use audit logs and `diagnose --json` when
debugging source failures.
