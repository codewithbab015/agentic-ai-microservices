from fastapi import FastAPI
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from pydantic import BaseModel

from .langgraph_utils import run_multi_agent_graph
from .mlflow_utils import log_prediction_to_mlflow

app = FastAPI(title="LangGraph Multi-Agent API")

# Prometheus Metrics
PRED_COUNTER = Counter(
    "fastapi_predictions_total",
    "Total predictions processed",
    ["agent_name"],  # differentiate agents if multiple
)

REQUEST_LATENCY = Histogram(
    "inference_latency_seconds", "Time spent processing inference", ["agent_name"]
)


class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None


@app.post("/inference")
def inference(payload: QueryRequest):
    agent_name = "langgraph-worker"

    # Measure latency and increment counter
    with REQUEST_LATENCY.labels(agent_name=agent_name).time():
        result = run_multi_agent_graph(payload.query, payload.session_id)
        log_prediction_to_mlflow(agent_name, payload.query, result["response"])
        PRED_COUNTER.labels(agent_name=agent_name).inc()

    return result


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
