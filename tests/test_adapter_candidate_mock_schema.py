from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "adapter_candidates"

EXPECTED_FIXTURES = [
    "efinance_realtime_raw_sample.json",
    "efinance_kline_raw_sample.json",
    "baostock_kline_raw_sample.json",
    "mootdx_quote_raw_sample.json",
    "mootdx_kline_raw_sample.json",
]


def test_adapter_candidate_raw_schema_files_exist_and_parse() -> None:
    for filename in EXPECTED_FIXTURES:
        path = FIXTURE_DIR / filename
        assert path.is_file(), filename
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["source_name"] in {"efinance", "baostock", "mootdx"}
        assert payload["source_api"]
        assert payload["return_type"]
        assert payload["unit_notes"]
        assert payload["request"]["live_request"] is False


def test_adapter_candidate_raw_schema_files_do_not_store_private_material() -> None:
    forbidden = ["token", "cookie", "secret", "webhook"]
    for filename in EXPECTED_FIXTURES:
        text = (FIXTURE_DIR / filename).read_text(encoding="utf-8").lower()
        for term in forbidden:
            assert term not in text, f"{filename} contains {term}"
