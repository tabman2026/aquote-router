# Adapter Template

This is a pseudocode template for a future adapter. It is not a real upstream
integration.

## File Location

Put adapter code in `pyqauto/adapters/`.

Example:

```text
pyqauto/adapters/example_source_adapter.py
tests/test_example_source_adapter.py
```

## Naming

Use a class name ending in `Adapter`. Set `source_name` to the stable source id
that will appear in audit records and standard rows.

## Required Methods

Every new adapter must implement:

- `fetch_raw`
- `inspect_raw_schema`
- `normalize_to_standard`
- `validate_standard_output`

## Pseudocode

```python
from __future__ import annotations

from typing import Any

from pyqauto.adapters.base import BaseQuoteAdapter
from pyqauto.exceptions import AdapterError
from pyqauto.source_schema import build_standard_row, raw_records


class ExampleAdapter(BaseQuoteAdapter):
    source = "example_source"
    source_name = "example_source"

    field_mapping = {
        "symbol": "code",
        "name": "name",
        "price": "last",
        "open": "open",
        "high": "high",
        "low": "low",
        "pre_close": "pre_close",
        "volume_shares": "volume",
        "amount_yuan": "amount",
        "datetime": "trade_time",
    }

    unit_rules = [
        {
            "raw_field": "volume",
            "raw_unit": "lot",
            "standard_field": "volume_shares",
            "standard_unit": "share",
            "conversion": "multiply_by_100",
        },
        {
            "raw_field": "amount",
            "raw_unit": "yuan",
            "standard_field": "amount_yuan",
            "standard_unit": "yuan",
            "conversion": "keep",
        },
    ]

    def fetch_raw(self, symbols: list[str], **kwargs: Any) -> Any:
        try:
            # Call the upstream public API here.
            return upstream_client.get_quotes(symbols)
        except Exception as exc:
            raise AdapterError(f"{self.source_name} fetch failed: {exc}") from exc

    def inspect_raw_schema(self, raw: Any = None, **kwargs: Any) -> dict[str, Any]:
        return super().inspect_raw_schema(
            raw=raw,
            source_api="example.get_quotes",
            field_mapping=self.field_mapping,
            unit_rules=self.unit_rules,
            **kwargs,
        )

    def normalize_to_standard(self, raw: Any, **kwargs: Any) -> list[dict[str, Any]]:
        fetch_time = kwargs["fetch_time"]
        rows: list[dict[str, Any]] = []
        for item in raw_records(raw):
            rows.append(
                build_standard_row(
                    symbol_raw=item.get("code"),
                    name=item.get("name"),
                    last_price=item.get("last"),
                    pre_close=item.get("pre_close"),
                    open_price=item.get("open"),
                    high=item.get("high"),
                    low=item.get("low"),
                    volume_shares=lots_to_shares(item.get("volume")),
                    amount_yuan=item.get("amount"),
                    trade_time=item.get("trade_time"),
                    fetch_time=fetch_time,
                    source_name=self.source_name,
                    source_api="example.get_quotes",
                    raw_row=item,
                )
            )
        return rows

    def validate_standard_output(self, rows: list[dict[str, Any]], **kwargs: Any):
        return super().validate_standard_output(
            rows,
            field_mapping=self.field_mapping,
            **kwargs,
        )
```

## Return Values

`fetch_raw` returns the upstream object unchanged. `normalize_to_standard`
returns a list of dictionaries. Public APIs should return pyqauto models only
after validation succeeds.

## Error Handling

Convert upstream exceptions into `AdapterError` or a more specific project
exception. Empty payloads, missing mapped fields, and unit conversion failures
should be visible in validation diagnostics and audit attempts.

## Unit Conversion

Do conversion in `normalize_to_standard`, not in `fetch_raw`. Keep raw data
available for diagnostics when `include_raw=True`, but never rely on raw fields
after validation.

## Schema Drift Guard

Call `validate_standard_output` before the router consumes rows. Missing core
fields should produce `field_missing` or `schema_drift`; they should not be
silently replaced with zero.

## Audit Fields

Accepted records must preserve:

- `source`
- `source_level`
- `trace_id`
- `fallback_from`
- `is_fallback`

Rejected attempts should record source, duration, error type, and rejection
reason.

## Test Template

```python
def test_example_adapter_normalizes_units() -> None:
    adapter = ExampleAdapter()
    raw = [{"code": "000001", "name": "Sample", "last": "10.5", "volume": "12", "amount": "3456"}]

    rows = adapter.normalize_to_standard(raw, fetch_time="2026-01-01T00:00:00Z")
    result = adapter.validate_standard_output(rows)

    assert result.is_valid
    assert rows[0]["volume_shares"] == 1200
    assert rows[0]["amount_yuan"] == 3456
```

## Documentation Template

When adding a real adapter, update:

- `docs/DATA_SOURCES.md`
- `docs/UNIT_RULES_FOR_ADAPTERS.md`
- `docs/SOURCE_POLICY.md`
- `docs/RETURN_FIELDS.md`
- `docs/AUDIT_TRAIL.md`

