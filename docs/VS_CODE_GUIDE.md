# VS Code setup guide

## A. Install Python

Check:

```powershell
python --version
```

Recommended: Python 3.11 or 3.12 for broad compatibility with scientific Python packages.

## B. Open terminal in VS Code

Use:

**Terminal → New Terminal**

Then:

```powershell
cd path\to\jali_pm25_flask_dashboard
```

## C. Create environment

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

## D. Select the interpreter

Press:

```text
Ctrl + Shift + P
```

Search:

```text
Python: Select Interpreter
```

Select the interpreter inside:

```text
.venv
```

## E. Install packages

```powershell
pip install -r requirements.txt
```

## F. Run

```powershell
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

## G. Test API

Try:

```text
http://127.0.0.1:5000/api/health
```

Then:

```text
http://127.0.0.1:5000/api/metrics
```

Then:

```text
http://127.0.0.1:5000/api/forecast?mode=native
```

## H. What each backend file does

### `backend/app.py`

Creates Flask and registers the API blueprint.

### `backend/api/routes.py`

Defines REST endpoints.

### `backend/services/data_service.py`

Reads and transforms the model-generated CSV/JSON files.

### `backend/config.py`

Stores configurable values such as the staleness threshold.

### `run.py`

Starts the development server.

## I. What each frontend file does

### `index.html`

Defines the dashboard structure.

### `style.css`

Controls layout, cards, tables, warning banner and responsive design.

### `app.js`

Calls Flask with the Fetch API, receives JSON, updates the dashboard and creates the Plotly forecast chart.

## J. Data flow for one chart

When the dashboard opens:

```text
Browser
  ↓
GET /api/forecast?mode=native
  ↓
routes.py
  ↓
data_service.py
  ↓
forecast_native.csv
  ↓
JSON response
  ↓
app.js
  ↓
Plotly
  ↓
Interactive chart
```

## K. Changing from sample artifacts to notebook artifacts

After running the corrected notebook, copy:

```text
forecast_native.csv
forecast_demo.csv
model_metadata.json
model_comparison.json
```

to:

```text
jali_pm25_flask_dashboard/data/
```

Overwrite the starter files.

Restart Flask if necessary and refresh the browser.

## L. Thesis screenshot checklist

Before taking the screenshot:

- API says "API connected"
- model name is visible
- RMSE/MAE/MAPE are visible
- staleness banner is visible because the source data are old
- forecast chart loads
- prediction interval is visible
- daily summary loads
- model comparison loads
- CSV download works

## M. Common errors

### `ModuleNotFoundError: No module named 'flask'`

Run:

```powershell
pip install -r requirements.txt
```

### `Required artifact is missing`

Make sure all four CSV/JSON files are inside:

```text
data/
```

### Port already in use

Stop the other Flask process, or change the port in `run.py`.

### PowerShell activation error

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then:

```powershell
.venv\Scripts\Activate.ps1
```

### Dashboard loads but chart is empty

Open:

```text
http://127.0.0.1:5000/api/forecast?mode=native
```

If that endpoint returns an error, fix the data artifact first.

If it returns JSON, open the browser developer console with F12 and inspect the JavaScript error.

## N. GitHub commands

```powershell
git init
git add .
git commit -m "Build Flask PM2.5 forecasting dashboard"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not commit:

- `.venv/`
- `.env`
- passwords/API keys
- large raw Excel datasets unless you intentionally want them public
