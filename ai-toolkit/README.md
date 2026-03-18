# AI Toolkit — Full-Stack AI Framework

This directory contains every layer of the AI stack, from raw data ingestion through to production deployment.

## Modules

| Module | Purpose |
|---|---|
| [`data-pipeline/`](./data-pipeline/) | Ingest, clean, transform, and engineer features |
| [`ml/`](./ml/) | Classical ML models (scikit-learn), gradient boosting, AutoML |
| [`nlp/`](./nlp/) | Tokenisation, embeddings, LLM wrappers, RAG pipelines |
| [`computer-vision/`](./computer-vision/) | Classification, detection, segmentation |
| [`agents/`](./agents/) | Autonomous agent loops, tool-use, multi-agent orchestration |
| [`deployment/`](./deployment/) | FastAPI model server, Docker, Kubernetes manifests |
| [`evaluation/`](./evaluation/) | Metrics, experiment tracking, benchmarking |

## Quick Start

```bash
pip install -r requirements.txt

# Run the data pipeline
python data-pipeline/pipeline.py

# Train a sample ML model
python ml/train.py

# Start the model server
python deployment/server.py
```
