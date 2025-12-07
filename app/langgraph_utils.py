import os

import requests

PLANNER_URL = os.getenv("PLANNER_URL", "http://agents-planner:8083")


def run_multi_agent_graph(query: str, session_id: str | None = None):
    payload = {"query": query, "session_id": session_id}
    resp = requests.post(f"{PLANNER_URL}/run-workflow", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()
