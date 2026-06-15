from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_required_examples_exist_and_have_main() -> None:
    for name in [
        "realtime_quotes_demo.py",
        "full_realtime_quotes_demo.py",
        "index_realtime_demo.py",
        "minute_kline_15m_demo.py",
        "daily_kline_demo.py",
        "kline_unified_demo.py",
        "audit_demo.py",
        "diagnose_demo.py",
    ]:
        path = ROOT / "examples" / name
        assert path.exists()
        tree = ast.parse(path.read_text(encoding="utf-8"))
        functions = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        assert "main" in functions
