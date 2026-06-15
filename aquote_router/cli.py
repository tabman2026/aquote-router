"""Command line interface for aquote-router."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import click

from aquote_router import __version__
from aquote_router.diagnostics import build_diagnostics
from aquote_router.exceptions import QuoteRouterError
from aquote_router.router import QuoteRouter

DEFAULT_PYTDX_SERVERS = "config/pytdx_servers.example.json"
DEFAULT_SOURCE_POLICY = "config/source_policy.example.yaml"


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__)
@click.option("--config", "source_policy_path", default=DEFAULT_SOURCE_POLICY, show_default=True)
@click.option("--pytdx-servers", default=DEFAULT_PYTDX_SERVERS, show_default=True)
@click.option("--audit-jsonl", default=None)
@click.option("--audit-sqlite", default=None)
@click.option("--json", "json_output", is_flag=True)
@click.pass_context
def main(
    ctx: click.Context,
    source_policy_path: str,
    pytdx_servers: str,
    audit_jsonl: str | None,
    audit_sqlite: str | None,
    json_output: bool,
) -> None:
    """A-share quote source router."""

    ctx.obj = {
        "source_policy_path": source_policy_path,
        "pytdx_servers_path": pytdx_servers,
        "audit_jsonl_path": audit_jsonl,
        "audit_sqlite_path": audit_sqlite,
        "json_output": json_output,
    }


@main.command()
@click.option("--json", "diagnose_json_output", is_flag=True)
@click.pass_obj
def diagnose(options: dict[str, Any], diagnose_json_output: bool) -> None:
    """Show local configuration summary without provider connections."""

    payload = build_diagnostics(
        source_policy_path=options["source_policy_path"],
        pytdx_servers_path=options["pytdx_servers_path"],
        audit_jsonl_path=options["audit_jsonl_path"],
        audit_sqlite_path=options["audit_sqlite_path"],
    )
    _print_payload(
        payload,
        json_output=bool(options["json_output"] or diagnose_json_output),
    )


@main.command()
@click.argument("symbols", nargs=-1, required=True)
@click.option("--json", "command_json_output", is_flag=True)
@click.pass_obj
def realtime(
    options: dict[str, Any],
    symbols: tuple[str, ...],
    command_json_output: bool,
) -> None:
    """Fetch realtime quotes."""

    router = _router_from_options(options)
    try:
        records = router.realtime_quotes(list(symbols))
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc
    _print_records(records, json_output=bool(options["json_output"] or command_json_output))


@main.command("full")
@click.argument("symbols", nargs=-1, required=True)
@click.option("--json", "command_json_output", is_flag=True)
@click.pass_obj
def full(
    options: dict[str, Any],
    symbols: tuple[str, ...],
    command_json_output: bool,
) -> None:
    """Fetch full realtime quotes."""

    router = _router_from_options(options)
    try:
        records = router.full_realtime_quotes(list(symbols))
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc
    _print_records(records, json_output=bool(options["json_output"] or command_json_output))


@main.command("index")
@click.argument("symbols", nargs=-1, required=True)
@click.option("--json", "command_json_output", is_flag=True)
@click.pass_obj
def index_realtime(
    options: dict[str, Any],
    symbols: tuple[str, ...],
    command_json_output: bool,
) -> None:
    """Fetch index realtime quotes."""

    router = _router_from_options(options)
    try:
        records = router.index_realtime(list(symbols))
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc
    _print_records(records, json_output=bool(options["json_output"] or command_json_output))


@main.command()
@click.argument("symbol")
@click.option("--period", default="1m", show_default=True)
@click.option("--count", default=240, show_default=True, type=int)
@click.option("--json", "command_json_output", is_flag=True)
@click.pass_obj
def minute(
    options: dict[str, Any],
    symbol: str,
    period: str,
    count: int,
    command_json_output: bool,
) -> None:
    """Fetch pytdx-only minute kline records."""

    router = _router_from_options(options)
    try:
        records = router.minute_kline(symbol, period=period, count=count)
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc
    _print_records(records, json_output=bool(options["json_output"] or command_json_output))


@main.command()
@click.argument("symbol")
@click.option("--count", default=120, show_default=True, type=int)
@click.option("--json", "command_json_output", is_flag=True)
@click.pass_obj
def daily(
    options: dict[str, Any],
    symbol: str,
    count: int,
    command_json_output: bool,
) -> None:
    """Fetch pytdx-only daily kline records."""

    router = _router_from_options(options)
    try:
        records = router.daily_kline(symbol, count=count)
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc
    _print_records(records, json_output=bool(options["json_output"] or command_json_output))


@main.command()
@click.argument("symbol")
@click.option("--period", default="1m", show_default=True)
@click.option("--count", default=120, show_default=True, type=int)
@click.option("--json", "command_json_output", is_flag=True)
@click.pass_obj
def kline(
    options: dict[str, Any],
    symbol: str,
    period: str,
    count: int,
    command_json_output: bool,
) -> None:
    """Fetch pytdx-only kline records through the unified API."""

    router = _router_from_options(options)
    try:
        records = router.kline(symbol, period=period, count=count)
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc
    _print_records(records, json_output=bool(options["json_output"] or command_json_output))


def _router_from_options(options: dict[str, Any]) -> QuoteRouter:
    try:
        return QuoteRouter.from_config(
            pytdx_servers_path=Path(options["pytdx_servers_path"]),
            source_policy_path=Path(options["source_policy_path"]),
            audit_jsonl_path=options["audit_jsonl_path"],
            audit_sqlite_path=options["audit_sqlite_path"],
        )
    except QuoteRouterError as exc:
        raise click.ClickException(_format_error(exc)) from exc


def _format_error(exc: QuoteRouterError) -> str:
    return f"[{exc.code}] {exc}"


def _print_payload(payload: Any, *, json_output: bool) -> None:
    if json_output:
        click.echo(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    if isinstance(payload, dict):
        for key, value in payload.items():
            click.echo(f"{key}: {value}")
    else:
        click.echo(str(payload))


def _print_records(records: list[Any], *, json_output: bool) -> None:
    rows = [record.to_dict() for record in records]
    if json_output:
        click.echo(json.dumps(rows, ensure_ascii=False, indent=2))
        return
    columns = [
        "symbol",
        "name",
        "price",
        "close",
        "period",
        "datetime",
        "source",
        "source_level",
        "trace_id",
    ]
    columns = [
        column
        for column in columns
        if any(row.get(column) not in (None, "") for row in rows)
        or column in {"symbol", "source", "source_level", "trace_id"}
    ]
    widths = {
        column: max(
            [len(column)]
            + [len(str(row.get(column, "") or "")) for row in rows]
        )
        for column in columns
    }
    header = "  ".join(column.ljust(widths[column]) for column in columns)
    click.echo(header)
    click.echo("  ".join("-" * widths[column] for column in columns))
    for row in rows:
        click.echo(
            "  ".join(str(row.get(column, "") or "").ljust(widths[column]) for column in columns)
        )


main.add_command(full, "full-realtime")


if __name__ == "__main__":
    main()
