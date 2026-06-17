# Quickstart

## Install

```bash
python -X utf8 -m pip install pyqauto
```

For local development:

```bash
python -X utf8 -m pip install -e ".[dev,test]"
```

## Python

```python
import pyqauto as aq

print(aq.quote("000001").to_dict())
print([bar.to_dict() for bar in aq.kline("000001", period="15m", count=120)])
```

The default source policy and pytdx server config are bundled with the package.
Call `aq.configure(...)` only when you need project-specific overrides or audit
outputs.

## CLI

```bash
pyqauto realtime 000001 600000 --json
pyqauto kline 000001 --period 1d --count 120 --json
pyqauto diagnose --json
```

Live upstream availability can change. Use audit logs and `diagnose --json` when
debugging source failures.
