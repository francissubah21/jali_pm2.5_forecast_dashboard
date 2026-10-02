# Jali Station PM2.5 Defense Dashboard — Final Notebook Update

Flask-based research dashboard for the dissertation:

**Forecasting Air Quality Using Time-Series Analysis: A Study of PM2.5 Concentration Trends and Predictive Modeling at Jali Station, Kigali**

## What was updated

The previous dashboard tabs are preserved:

1. Overview
2. PM2.5 Trends
3. Meteorology
4. 7-Day Forecast
5. Model & Methodology
6. Research Figures

The content has been updated to the uploaded final notebook and final dissertation. The old SARIMA-centered Model 1/2/3 results are no longer used as the primary dashboard results.

## Current analytical results

- 8,274 hourly REMA observations
- 727 processed daily PM2.5 observations
- 1.5×IQR outlier capping before imputation
- 75 observations capped (1.12%)
- Raw maximum: 3,335.06 µg/m³
- Processed maximum: 61.83 µg/m³
- Common chronological test period: 72 days
- Candidate models: Seasonal Naive, ARIMA, SARIMA, Random Forest, XGBoost, Prophet
- Selected model: **Random Forest**
- Test RMSE: **5.93 µg/m³**
- Test MAE: **4.42 µg/m³**
- Test MAPE: **22.08%**
- Native forecast: 1–7 March 2024
- Supplementary REMA–Meteo overlap: 206 days
- 2026 current-window forecast: **capability demonstration only** because the REMA training data end on 29 February 2024

## APIs

- `/api/health`
- `/api/model`
- `/api/analysis`
- `/api/metrics`
- `/api/metrics/comparison`
- `/api/correlations`
- `/api/forecast`
- `/api/forecast/all`
- `/api/forecast/live`
- `/api/forecast/download`
- `/api/forecast/live/download`

The frontend reads dashboard data through these Flask REST endpoints.

## Local run

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python run.py
```

Open `http://127.0.0.1:5000`.

## Render

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn run:app
```

See `docs/RENDER_DEPLOYMENT_GUIDE.md` for the full deployment checklist.

## Defense materials

- `docs/DEFENSE_FIGURE_GUIDE.md` — explanation of every current notebook figure and suggested defense interpretation.
- `docs/RENDER_DEPLOYMENT_GUIDE.md` — step-by-step Render deployment.
- `docs/FIGURE_SOURCE_NOTES.md` — source and scientific-status notes.
