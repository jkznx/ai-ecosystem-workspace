"""Minimal local self-check for the ASM09 application instrumentation."""

import os

os.environ["OBSERVABILITY_ENABLED"] = "false"

from prometheus_client import generate_latest  # noqa: E402

from backend.main import app  # noqa: E402
from backend.observability.metrics import observe_inference_job  # noqa: E402


def main() -> None:
    openapi_paths = app.openapi()["paths"]
    assert "/health/observability" in openapi_paths
    assert "/metrics" not in openapi_paths

    observe_inference_job(
        status="success",
        model_name="self-check",
        duration_seconds=0.01,
        entity_count=1,
    )
    metrics = generate_latest().decode("utf-8")
    assert 'model_name="self-check",status="success"' in metrics
    assert 'ai_ecosystem_inference_entities_total{model_name="self-check"} 1.0' in metrics

    print("observability self-check passed")


if __name__ == "__main__":
    main()
