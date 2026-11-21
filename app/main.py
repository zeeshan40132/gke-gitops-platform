
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="GitOps Platform Demo",
    description="A demo application deployed through a GitOps platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to the GitOps Platform Demo",
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
