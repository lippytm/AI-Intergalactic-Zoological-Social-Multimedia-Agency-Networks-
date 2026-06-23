"""
Model Evaluation & Experiment Tracking
=======================================
Metrics helpers, confusion matrix utilities, and MLflow experiment tracking.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def classification_metrics(y_true: Any, y_pred: Any, y_proba: Any = None) -> dict[str, float]:
    from sklearn.metrics import (
        accuracy_score,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )

    metrics: dict[str, float] = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision_macro": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall_macro": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_macro": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }
    if y_proba is not None:
        try:
            metrics["roc_auc_ovr"] = roc_auc_score(y_true, y_proba, multi_class="ovr")
        except ValueError:
            pass
    return metrics


def regression_metrics(y_true: Any, y_pred: Any) -> dict[str, float]:
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    return {
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "r2": r2_score(y_true, y_pred),
    }


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

def plot_confusion_matrix(
    y_true: Any,
    y_pred: Any,
    labels: list[str] | None = None,
    save_path: str | None = None,
) -> None:
    import matplotlib.pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
        logger.info("Confusion matrix saved to %s", save_path)
    else:
        plt.show()


# ---------------------------------------------------------------------------
# MLflow experiment tracking
# ---------------------------------------------------------------------------

def log_experiment(
    experiment_name: str,
    run_name: str,
    params: dict[str, Any],
    metrics: dict[str, float],
    artifacts: list[str] | None = None,
) -> str:
    """Log parameters, metrics, and artefacts to an MLflow experiment."""
    import mlflow  # type: ignore

    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name) as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        if artifacts:
            for path in artifacts:
                mlflow.log_artifact(path)
        logger.info("MLflow run %s logged to experiment %r", run.info.run_id, experiment_name)
        return run.info.run_id


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    y_true = rng.integers(0, 3, size=100)
    y_pred = rng.integers(0, 3, size=100)
    metrics = classification_metrics(y_true, y_pred)
    logger.info("Classification metrics: %s", metrics)

    reg_true = rng.normal(size=100)
    reg_pred = reg_true + rng.normal(scale=0.1, size=100)
    reg_metrics = regression_metrics(reg_true, reg_pred)
    logger.info("Regression metrics: %s", reg_metrics)
