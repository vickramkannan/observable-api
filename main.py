from fastapi import FastAPI, Request
from fastapi.responses import Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from collections import deque
import time
import uuid

EMAIL = "22f3000616@ds.study.iitm.ac.in"

app = FastAPI()

# Startup time
start_time = time.time()

# Prometheus counter
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP Requests"
)

# Store the last 1000 log entries
logs = deque(maxlen=1000)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Increment counter for every request
    http_requests_total.inc()

    request_id = str(uuid.uuid4())

    logs.append({
        "level": "INFO",
        "ts": time.time(),
        "path": request.url.path,
        "request_id": request_id
    })

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/")
def home():
    return {"message": "Observable API Running"}


@app.get("/work")
def work(n: int):
    # Simulate work
    total = 0
    for i in range(n):
        total += i

    return {
        "email": EMAIL,
        "done": n
    }


@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "uptime_s": time.time() - start_time
    }


@app.get("/logs/tail")
def logs_tail(limit: int = 10):
    return list(logs)[-limit:]
