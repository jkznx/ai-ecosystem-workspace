from __future__ import annotations

from typing import Any

from opentelemetry import propagate, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from backend.core.config import settings

_provider: TracerProvider | None = None


def configure_telemetry(
    service_name: str,
    *,
    app: Any | None = None,
    sqlalchemy_engine: Any | None = None,
) -> None:
    """Configure one OTLP tracer provider per API or worker process."""
    global _provider

    if not settings.OBSERVABILITY_ENABLED or _provider is not None:
        return

    resource = Resource.create(
        {
            "service.name": service_name,
            "service.namespace": "ai-ecosystem",
            "service.version": "0.1.0",
            "deployment.environment.name": settings.ENVIRONMENT,
        }
    )
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(
        endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT,
        insecure=settings.OTEL_EXPORTER_OTLP_INSECURE,
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    _provider = provider

    RequestsInstrumentor().instrument()
    RedisInstrumentor().instrument()
    URLLib3Instrumentor().instrument()

    if sqlalchemy_engine is not None:
        SQLAlchemyInstrumentor().instrument(engine=sqlalchemy_engine)

    if app is not None:
        FastAPIInstrumentor.instrument_app(
            app,
            excluded_urls=settings.OTEL_EXCLUDED_URLS,
        )


def inject_trace_context() -> dict[str, str]:
    carrier: dict[str, str] = {}
    if settings.OBSERVABILITY_ENABLED:
        propagate.inject(carrier)
    return carrier


def extract_trace_context(carrier: dict[str, str] | None) -> Any:
    return propagate.extract(carrier or {})


def shutdown_telemetry() -> None:
    global _provider
    if _provider is not None:
        _provider.shutdown()
        _provider = None
