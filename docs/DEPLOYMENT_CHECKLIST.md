# Defense and Deployment Checklist

## Before the thesis defense

- [ ] Run `python run.py` locally.
- [ ] Confirm the API badge says **API connected**.
- [ ] Open Overview and confirm the native forecast appears.
- [ ] Open PM2.5 Trends and confirm all figures load.
- [ ] Open Meteorology and confirm the correlation chart loads.
- [ ] Open 7-Day Forecast and test Native/Demo buttons.
- [ ] Test CSV download.
- [ ] Open Model & Methodology and review limitations.
- [ ] Do not describe Demo mode as a live 2026 forecast.

## Recommended defense demonstration order

1. Overview — explain the research workflow.
2. PM2.5 Trends — answer Objective 1.
3. Meteorology — answer Objective 3 and explain the 206-day overlap.
4. 7-Day Forecast — answer Objectives 2 and 4.
5. Model & Methodology — explain model selection and limitations.

## Render

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
gunicorn run:app
```
