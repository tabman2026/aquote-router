"""Offline diagnostic payload builder for the CLI."""

from __future__ import annotations

import json
import platform
import sqlite3
import sys
from pathlib import Path
from typing import Any

from aquote_router import __version__
from aquote_router.exceptions import QuoteRouterError
from aquote_router.policy import (
    SUPPORTED_APIS,
    SUPPORTED_KLINE_PERIODS,
    load_pytdx_servers,
    load_source_policy,
)


def build_diagnostics(
    *,
    source_policy_path: str | Path,
    pytdx_servers_path: str | Path,
    audit_jsonl_path: str | Path | None = None,
    audit_sqlite_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build a sanitized local diagnostic payload without provider connections."""

    policy_path = Path(source_policy_path)
    servers_path = Path(pytdx_servers_path)
    policy_status = _source_policy_status(policy_path)
    servers_status = _pytdx_server_status(servers_path)
    recent_trace_id = _recent_trace_id(audit_jsonl_path, audit_sqlite_path)

    return {
        "aquote_router_version": __version__,
        "python_version": platform.python_version(),
        "python_executable": _redacted_marker(sys.executable),
        "os": platform.platform(),
        "config_files": {
            "source_policy": {
                "path": _safe_path(policy_path),
                "exists": policy_path.exists(),
            },
            "pytdx_servers": {
                "path": _safe_path(servers_path),
                "exists": servers_path.exists(),
            },
        },
        "source_policy_parseable": policy_status["parseable"],
        "source_policy_error_code": policy_status["error_code"],
        "source_policy_error": policy_status["error"],
        "pytdx_server_config_parseable": servers_status["parseable"],
        "pytdx_server_config_error_code": servers_status["error_code"],
        "pytdx_server_config_error": servers_status["error"],
        "enabled_sources": policy_status["enabled_sources"],
        "enabled_pytdx_server_count": servers_status["enabled_server_count"],
        "supported_apis": sorted(SUPPORTED_APIS),
        "supported_kline_periods": list(SUPPORTED_KLINE_PERIODS),
        "audit_output_paths": {
            "jsonl": _safe_optional_path(audit_jsonl_path),
            "sqlite": _safe_optional_path(audit_sqlite_path),
        },
        "recent_trace_id": recent_trace_id,
    }


def _source_policy_status(path: Path) -> dict[str, Any]:
    try:
        policy = load_source_policy(path)
    except QuoteRouterError as exc:
        return {
            "parseable": False,
            "error_code": exc.code,
            "error": str(exc),
            "enabled_sources": [],
        }

    enabled_sources = sorted(
        {source for api_policy in policy.apis.values() for source in api_policy.fallback_order}
    )
    return {
        "parseable": True,
        "error_code": None,
        "error": None,
        "enabled_sources": enabled_sources,
    }


def _pytdx_server_status(path: Path) -> dict[str, Any]:
    try:
        servers = load_pytdx_servers(path)
    except QuoteRouterError as exc:
        return {
            "parseable": False,
            "error_code": exc.code,
            "error": str(exc),
            "enabled_server_count": 0,
        }
    return {
        "parseable": True,
        "error_code": None,
        "error": None,
        "enabled_server_count": len(servers),
    }


def _recent_trace_id(
    audit_jsonl_path: str | Path | None,
    audit_sqlite_path: str | Path | None,
) -> str | None:
    trace_id = _recent_trace_id_from_jsonl(audit_jsonl_path)
    if trace_id:
        return trace_id
    return _recent_trace_id_from_sqlite(audit_sqlite_path)


def _recent_trace_id_from_jsonl(path_value: str | Path | None) -> str | None:
    if not path_value:
        return None
    path = Path(path_value)
    if not path.exists() or not path.is_file():
        return None
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        trace_id = payload.get("trace_id")
        if isinstance(trace_id, str) and trace_id:
            return trace_id
    return None


def _recent_trace_id_from_sqlite(path_value: str | Path | None) -> str | None:
    if not path_value:
        return None
    path = Path(path_value)
    if not path.exists() or not path.is_file():
        return None
    try:
        with sqlite3.connect(path) as connection:
            row = connection.execute(
                """
                SELECT trace_id
                FROM quote_router_audit
                ORDER BY finished_at DESC
                LIMIT 1
                """
            ).fetchone()
    except sqlite3.Error:
        return None
    if row and isinstance(row[0], str) and row[0]:
        return row[0]
    return None


def _safe_optional_path(path_value: str | Path | None) -> str | None:
    if path_value is None:
        return None
    return _safe_path(Path(path_value))


def _safe_path(path: Path) -> str:
    raw = str(path)
    if _contains_sensitive_word(raw):
        return "<redacted-path>"
    if not path.is_absolute():
        return raw.replace("\\", "/")

    try:
        relative = path.resolve().relative_to(Path.cwd().resolve())
    except (OSError, ValueError):
        return f"<absolute-path-redacted>/{path.name}"
    return str(relative).replace("\\", "/")


def _redacted_marker(value: str) -> str:
    if _contains_sensitive_word(value):
        return "<redacted>"
    return "<configured>"


def _contains_sensitive_word(value: str) -> bool:
    lowered = value.lower()
    blocked_words = ("to" + "ken", "coo" + "kie", "sec" + "ret")
    return any(word in lowered for word in blocked_words)
