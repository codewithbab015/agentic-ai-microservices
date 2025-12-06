from fastapi.responses import Response
from langgraph_utils import run_multi_agent_graph
from mlflow_utils import log_prediction_to_mlflow
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI(title="LangGraph Multi-Agent API")

PRED_COUNTER = Counter("fastapi_predictions_total", "Total predictions processed")


class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None


@app.post("/inference")
def inference(payload: QueryRequest):
    PRED_COUNTER.inc()
    result = run_multi_agent_graph(payload.query, payload.session_id)
    log_prediction_to_mlflow("langgraph-worker", payload.query, result["response"])
    return result


@app.get("/healthz")
def health():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
