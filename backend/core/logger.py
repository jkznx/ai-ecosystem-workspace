from __future__ import annotations

import contextvars
import json
import logging
import logging.handlers
import sys
from pathlib import Path

from opentelemetry import trace

from backend.core.config import settings

_request_id_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


def set_request_id(request_id: str) -> None:
    _request_id_ctx.set(request_id)


def get_request_id() -> str:
    return _request_id_ctx.get()


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        span_context = trace.get_current_span().get_span_context()
        if span_context.is_valid:
            record.trace_id = format(span_context.trace_id, "032x")
            record.span_id = format(span_context.span_id, "016x")
        else:
            record.trace_id = "-"
            record.span_id = "-"
        return True


_TEXT_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | req=%(request_id)s | "
    "trace=%(trace_id)s span=%(span_id)s | "
    "%(module)s:%(funcName)s:%(lineno)d | %(message)s"
)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": self.formatTime(record, "%Y-%m-%dT%H:%M:%S%z"),
            "level": record.levelname,
            "logger": record.name,
            "request_id": getattr(record, "request_id", "-"),
            "trace_id": getattr(record, "trace_id", "-"),
            "span_id": getattr(record, "span_id", "-"),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        extra_fields = getattr(record, "extra_fields", None)
        if extra_fields:
            payload.update(extra_fields)
        return json.dumps(payload, ensure_ascii=False)


_LOG_DIR = Path("logs")


def get_logger(name: str = settings.APP_NAME) -> logging.Logger:
    logger = logging.getLogger(name)
    if getattr(logger, "_custom_logger_configured", False):
        return logger

    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)
    logger.propagate = False
    context_filter = ContextFilter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(_TEXT_FORMAT))
    console_handler.addFilter(context_filter)
    logger.addHandler(console_handler)

    _LOG_DIR.mkdir(exist_ok=True)
    file_handler = logging.handlers.RotatingFileHandler(
        _LOG_DIR / f"{settings.APP_NAME}.jsonl",
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(JSONFormatter())
    file_handler.addFilter(context_filter)
    logger.addHandler(file_handler)

    logger._custom_logger_configured = True
    return logger


logger = get_logger()
