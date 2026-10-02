# API reference

## GET /api/health

Returns service status.

Example:

```json
{
  "status": "ok",
  "service": "Jali PM2.5 Flask API",
  "model_available": true
}
```

## GET /api/forecast?mode=native

Returns the scientifically valid forecast artifact.

## GET /api/forecast?mode=demo

Returns the demonstration artifact.

The response contains:

- mode
- demo_only
- last_training_date
- forecast records
- daily summary
- staleness information

## GET /api/forecast/summary?mode=native

Returns only daily forecast summaries.

## GET /api/forecast/download?mode=native

Downloads the selected forecast as CSV.

## GET /api/metrics

Returns:

- model
- order
- seasonal order
- RMSE
- MAE
- MAPE
- Ljung–Box status
- training date
- staleness status

## GET /api/metrics/comparison

Returns all five thesis model results.

## GET /api/model

Returns model identity and study metadata.
