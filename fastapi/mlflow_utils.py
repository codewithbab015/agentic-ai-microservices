import os

import mlflow

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


def log_prediction_to_mlflow(
    model_name: str, input_text: str, output_text: str, metrics: dict | None = None
) -> str:
    with mlflow.start_run() as run:
        mlflow.log_param("model", model_name)
        mlflow.log_param("input_length", len(input_text))
        mlflow.log_metric("output_length", len(output_text))
        if metrics:
            for k, v in metrics.items():
                mlflow.log_metric(k, v)
        mlflow.log_text(input_text, "input.txt")
        mlflow.log_text(output_text, "output.txt")
        return run.info.run_id
