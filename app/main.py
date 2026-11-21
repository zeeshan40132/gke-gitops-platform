
from fastapi import FastAPI, Request
from fastapi.responses import Response
from datetime import datetime, timezone
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
import time


app = FastAPI(
    title="GitOps Platform Demo",
    description="A demo application deployed through a GitOps platform",
    version="1.0.0"
)


# Prometheus metrics

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"]
)

ERROR_COUNT = Counter(
    "http_errors_total",
    "Total number of HTTP errors",
    ["method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request processing duration in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)
)


# HTTP monitoring middleware

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response

    finally:
        # Avoid counting Prometheus scraping itself.
        if request.url.path != "/metrics":

            duration = time.perf_counter() - start_time

            route = request.scope.get("route")
            endpoint = getattr(route, "path", "unmatched")

            method = request.method
            status = str(status_code)

            REQUEST_COUNT.labels(
                method, endpoint, status
            ).inc()

            if status_code >= 400:
                ERROR_COUNT.labels(
                    method, endpoint, status
                ).inc()

            REQUEST_LATENCY.labels(
                method, endpoint
            ).observe(duration)


# Application endpoints

@app.get("/")
def home():
    return {
        "message": "GitOps deployment update successful",
        "platform": "OpenTofu + Kubernetes + GitOps",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/version")
def version():
    return {
        "version": app.version,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Prometheus metrics endpoint

@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
