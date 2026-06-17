"""Exception types and stable error codes for pyqauto."""

from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    """Stable public error codes used by CLI output and audit diagnostics."""

    CONFIG_NOT_FOUND = "CONFIG_NOT_FOUND"
    CONFIG_PARSE_FAILED = "CONFIG_PARSE_FAILED"
    SOURCE_POLICY_NOT_FOUND = "SOURCE_POLICY_NOT_FOUND"
    SOURCE_POLICY_INVALID = "SOURCE_POLICY_INVALID"
    PYTDX_CONNECT_FAILED = "PYTDX_CONNECT_FAILED"
    PYTDX_ALL_SERVERS_FAILED = "PYTDX_ALL_SERVERS_FAILED"
    EASYQUOTATION_SINA_FAILED = "EASYQUOTATION_SINA_FAILED"
    EASYQUOTATION_TENCENT_FAILED = "EASYQUOTATION_TENCENT_FAILED"
    FALLBACK_EXHAUSTED = "FALLBACK_EXHAUSTED"
    SOURCE_POLICY_BLOCKED = "SOURCE_POLICY_BLOCKED"
    UNSUPPORTED_SYMBOL = "UNSUPPORTED_SYMBOL"
    UNSUPPORTED_PERIOD = "UNSUPPORTED_PERIOD"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    NORMALIZE_FAILED = "NORMALIZE_FAILED"
    AUDIT_WRITE_FAILED = "AUDIT_WRITE_FAILED"
    CLI_ARGUMENT_ERROR = "CLI_ARGUMENT_ERROR"


ERROR_CODES = tuple(code.value for code in ErrorCode)


class QuoteRouterError(Exception):
    """Base exception for all router errors."""

    default_code = ErrorCode.FALLBACK_EXHAUSTED

    def __init__(self, message: str | None = None, *, code: ErrorCode | str | None = None) -> None:
        super().__init__(message or self.default_code.value)
        self.code = _normalize_code(code or self.default_code)


class ConfigurationError(QuoteRouterError):
    """Raised when local configuration is invalid or incomplete."""

    default_code = ErrorCode.CONFIG_PARSE_FAILED


class SourcePolicyError(ConfigurationError):
    """Raised when source policy is invalid."""

    default_code = ErrorCode.SOURCE_POLICY_INVALID


class AdapterError(QuoteRouterError):
    """Raised when an adapter cannot complete a source request."""

    default_code = ErrorCode.NORMALIZE_FAILED


class SourceUnavailableError(AdapterError):
    """Raised when a configured source is unavailable or returns no records."""

    default_code = ErrorCode.EMPTY_RESPONSE


class NoAvailableSourceError(QuoteRouterError):
    """Raised after every allowed source failed."""

    default_code = ErrorCode.FALLBACK_EXHAUSTED


class UnsupportedSymbolError(AdapterError):
    """Raised when a symbol is outside the documented support rules."""

    default_code = ErrorCode.UNSUPPORTED_SYMBOL


class UnsupportedPeriodError(AdapterError):
    """Raised when a kline period is outside the supported set."""

    default_code = ErrorCode.UNSUPPORTED_PERIOD


def _normalize_code(code: ErrorCode | str) -> str:
    if isinstance(code, ErrorCode):
        return code.value
    return str(code)
