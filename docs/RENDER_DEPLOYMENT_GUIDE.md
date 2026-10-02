# Render Deployment — Step-by-Step

## 1. Test locally
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```
Open `http://127.0.0.1:5000`. Confirm the header says **API connected** and every dashboard tab loads.

## 2. Test the API locally
Open these URLs in the browser:
- `/api/health`
- `/api/model`
- `/api/metrics/comparison`
- `/api/analysis`
- `/api/correlations`
- `/api/forecast`
- `/api/forecast/all`
- `/api/forecast/live`

The health endpoint should return `status: ok`.

## 3. Create the GitHub repository
Create a new repository and upload the contents of this project folder, including `backend/`, `frontend/`, `data/`, `docs/`, `run.py`, `requirements.txt` and `Procfile`. Do not upload `.venv`.

## 4. Create the Render Web Service
In Render: New → Web Service → connect the GitHub repository.

Use:
- **Runtime:** Python
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn run:app`
- **Branch:** your deployment branch (usually `main`)

## 5. Environment variables
No database or external API key is required for the current research prototype. Optional variables supported by the app include:
- `STALE_AFTER_DAYS=30`
- `WHO_PM25_24H=15`
- `APP_TITLE=Jali Station — PM2.5 Forecast Dashboard`

## 6. Deploy
Click Create Web Service. Wait for the build to finish. Render will start Gunicorn and expose the public URL.

## 7. Verify the deployed API
If the Render URL is `https://your-app.onrender.com`, test:
- `https://your-app.onrender.com/api/health`
- `https://your-app.onrender.com/api/model`
- `https://your-app.onrender.com/api/forecast`

Then open the root URL and confirm the dashboard says **API connected**.

## 8. Important defense wording
Say: **“The dashboard is deployed as a Flask research prototype. Its APIs serve the final notebook artifacts. It is not connected to a live REMA sensor feed, so the 2026 forecast window is a capability demonstration rather than a validated operational forecast.”**

## 9. Common Render problems
### Build fails
Check `requirements.txt` and the Render build log.

### App starts but page is blank
Check `/api/health`. If it fails, a data artifact may be missing from `data/`.

### Images are missing
Confirm `frontend/static/current_figures/` was committed to GitHub.

### API says degraded
Check that all JSON/CSV files in `data/` are present and that the paths match the repository structure.

### Gunicorn cannot import app
The start command must be `gunicorn run:app`, and `run.py` must expose the Flask application object named `app`.

## 10. Updating after new modelling
Replace the artifacts in `data/`, replace the current notebook figures in `frontend/static/current_figures/`, update the metadata and test-period results, then redeploy. Do not present a new forecast as current until the underlying air-quality data and model have been retrained and independently validated.
