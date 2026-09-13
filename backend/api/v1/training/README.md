# Training API

Endpoints for AI model training workflows.

## Endpoints

- `POST /v1/training/start` - Start a new training job
- `GET /v1/training/{training_id}/status` - Get training status and metrics
- `GET /v1/training/{training_id}/logs` - Stream training logs
- `POST /v1/training/{training_id}/stop` - Stop an active training job
- `GET /v1/training/{training_id}/model` - Download trained model

## How to use

```bash
# Start training
curl -X POST http://localhost:8000/v1/training/start \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": "my-dataset",
    "model_type": "token-classifier",
    "epochs": 3,
    "learning_rate": 0.001
  }'

# Check status
curl http://localhost:8000/v1/training/abc123/status
```

## Model types

- **token-classifier** - Token classification (NER, POS tagging, etc.)
- **text-classifier** - Text/document classification
- More types can be added by extending training service
