# ================================================================
# NOTEBOOK UPDATE — 7-DAY FORECAST FROM THE END OF TRAINING DATA
# ================================================================
# RUN THIS CELL AFTER CELL 33 (the native Model 3 forecast figure)
# and BEFORE Part 10 — Streamlit Dashboard.
#
# Purpose:
#   1. Refit all five candidate models on their respective FULL
#      modelling tracks.
#   2. Generate a seven-day forecast immediately after the end of
#      each model's training series.
#   3. Put all model forecasts in one CSV so they can be inspected
#      side-by-side.
#
# Important:
#   - This is a validation/check cell, not a replacement for the
#     model-selection analysis already reported in the thesis.
#   - Model 4 (SARIMAX) requires future meteorological predictors.
#     Because future weather values are not available in this
#     notebook, its forecast below is explicitly labelled as a
#     SCENARIO using the last observed exogenous values repeated
#     over the seven-day horizon. Do NOT call that a live forecast.
# ================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ---------------------------------------------------------------
# Helper: produce one seven-day forecast with 95% intervals
# ---------------------------------------------------------------
def _seven_day_forecast(fit, start_after, model_name, note=""):
    pred = fit.get_forecast(steps=7)
    mean = np.maximum(np.asarray(pred.predicted_mean, dtype=float), 0)
    ci = pred.conf_int(alpha=0.05)
    lower = np.maximum(np.asarray(ci.iloc[:, 0], dtype=float), 0)
    upper = np.maximum(np.asarray(ci.iloc[:, 1], dtype=float), 0)

    dates = pd.date_range(
        start=pd.Timestamp(start_after) + pd.Timedelta(days=1),
        periods=7,
        freq="D"
    )

    return pd.DataFrame({
        "Model": model_name,
        "Forecast_Date": dates,
        "Forecast_PM25": mean,
        "Lower_95CI": lower,
        "Upper_95CI": upper,
        "Forecast_Note": note,
    })


all_future_forecasts = []

# ---------------------------------------------------------------
# MODEL 1 — Missing-value treatment only
# ---------------------------------------------------------------
# Use the order selected during the original Model 1 grid search,
# but refit it on the COMPLETE Track 0 series before forecasting.
model1_full = SARIMAX(
    daily_pm25_clean,
    order=best_1["order"],
    seasonal_order=best_1["seasonal_order"],
    enforce_stationarity=False,
    enforce_invertibility=False,
).fit(disp=False)

fc1_future = _seven_day_forecast(
    model1_full,
    daily_pm25_clean.index.max(),
    "Model 1 — Missing-only SARIMA",
    "Full Track 0 refit; sensor fault retained by design."
)
all_future_forecasts.append(fc1_future)


# ---------------------------------------------------------------
# MODEL 2 — Log SARIMA
# ---------------------------------------------------------------
# Refit on the COMPLETE log-transformed Track 1 series and then
# back-transform the forecast to the original PM2.5 scale.
log_full = np.log1p(daily_pm25_full)
model2_full = SARIMAX(
    log_full,
    order=best_2["order"],
    seasonal_order=best_2["seasonal_order"],
    enforce_stationarity=False,
    enforce_invertibility=False,
).fit(disp=False)

pred2 = model2_full.get_forecast(steps=7)
mean2 = np.maximum(np.expm1(np.asarray(pred2.predicted_mean, dtype=float)), 0)
ci2 = pred2.conf_int(alpha=0.05)
lower2 = np.maximum(np.expm1(np.asarray(ci2.iloc[:, 0], dtype=float)), 0)
upper2 = np.maximum(np.expm1(np.asarray(ci2.iloc[:, 1], dtype=float)), 0)
dates2 = pd.date_range(
    start=daily_pm25_full.index.max() + pd.Timedelta(days=1),
    periods=7,
    freq="D"
)

fc2_future = pd.DataFrame({
    "Model": "Model 2 — Log SARIMA",
    "Forecast_Date": dates2,
    "Forecast_PM25": mean2,
    "Lower_95CI": lower2,
    "Upper_95CI": upper2,
    "Forecast_Note": "Full Track 1 refit; forecast back-transformed with expm1().",
})
all_future_forecasts.append(fc2_future)


# ---------------------------------------------------------------
# MODEL 3 — Selected outlier-treated SARIMA
# ---------------------------------------------------------------
# This is the model used by the dashboard. It is refitted on the
# COMPLETE cleaned Track 1 series before generating the future
# seven-day forecast.
model3_full = SARIMAX(
    daily_pm25_full,
    order=best_3["order"],
    seasonal_order=best_3["seasonal_order"],
    enforce_stationarity=False,
    enforce_invertibility=False,
).fit(disp=False)

fc3_future = _seven_day_forecast(
    model3_full,
    daily_pm25_full.index.max(),
    "Model 3 — Outlier-treated SARIMA",
    "Full Track 1 refit; selected deployment prototype."
)
all_future_forecasts.append(fc3_future)


# ---------------------------------------------------------------
# MODEL 4 — SARIMAX with meteorological variables
# ---------------------------------------------------------------
# A genuine future SARIMAX forecast needs future values for every
# exogenous variable. The notebook does not contain those future
# weather values. Therefore we provide a clearly labelled scenario:
# the LAST observed exogenous row is repeated for seven days.
# This is useful for checking the model, but it is NOT a live
# meteorological forecast.
# ---------------------------------------------------------------
model4_full = SARIMAX(
    target_4,
    exog=exog_4,
    order=best_order_4,
    seasonal_order=(0, 0, 1, 7),
    enforce_stationarity=False,
    enforce_invertibility=False,
).fit(disp=False)

future_exog4 = pd.DataFrame(
    np.repeat(exog_4.iloc[[-1]].values, 7, axis=0),
    columns=exog_4.columns,
    index=pd.date_range(
        start=target_4.index.max() + pd.Timedelta(days=1),
        periods=7,
        freq="D",
    ),
)

pred4 = model4_full.get_forecast(steps=7, exog=future_exog4)
mean4 = np.maximum(np.asarray(pred4.predicted_mean, dtype=float), 0)
ci4 = pred4.conf_int(alpha=0.05)
lower4 = np.maximum(np.asarray(ci4.iloc[:, 0], dtype=float), 0)
upper4 = np.maximum(np.asarray(ci4.iloc[:, 1], dtype=float), 0)

fc4_future = pd.DataFrame({
    "Model": "Model 4 — SARIMAX",
    "Forecast_Date": future_exog4.index,
    "Forecast_PM25": mean4,
    "Lower_95CI": lower4,
    "Upper_95CI": upper4,
    "Forecast_Note": (
        "SCENARIO ONLY: last observed meteorological predictors repeated "
        "for seven days; not a live forecast."
    ),
})
all_future_forecasts.append(fc4_future)


# ---------------------------------------------------------------
# MODEL 5 — Prophet benchmark
# ---------------------------------------------------------------
from prophet import Prophet

prophet_full = daily_pm25_full.rename("PM2.5").reset_index()
prophet_full.columns = ["ds", "y"]

model5_full = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
)
model5_full.fit(prophet_full)

future5 = model5_full.make_future_dataframe(periods=7, freq="D")
pred5 = model5_full.predict(future5).tail(7)

fc5_future = pd.DataFrame({
    "Model": "Model 5 — Prophet",
    "Forecast_Date": pd.to_datetime(pred5["ds"]).values,
    "Forecast_PM25": np.maximum(pred5["yhat"].values, 0),
    "Lower_95CI": np.maximum(pred5["yhat_lower"].values, 0),
    "Upper_95CI": np.maximum(pred5["yhat_upper"].values, 0),
    "Forecast_Note": "Full Track 1 refit; benchmark model with short-history caveat.",
})
all_future_forecasts.append(fc5_future)


# ---------------------------------------------------------------
# COMBINE + DISPLAY
# ---------------------------------------------------------------
all_models_forecast = pd.concat(all_future_forecasts, ignore_index=True)
all_models_forecast["Forecast_PM25"] = all_models_forecast["Forecast_PM25"].round(3)
all_models_forecast["Lower_95CI"] = all_models_forecast["Lower_95CI"].round(3)
all_models_forecast["Upper_95CI"] = all_models_forecast["Upper_95CI"].round(3)

print("\nALL-MODEL 7-DAY FORECASTS FROM THE END OF TRAINING DATA")
print("=" * 72)
print(all_models_forecast.to_string(index=False))

print("\nSeven-day forecast means by model:")
print(
    all_models_forecast.groupby("Model")["Forecast_PM25"]
    .mean()
    .round(2)
    .sort_index()
)

# Save for later inspection.
all_models_forecast.to_csv("all_models_7day_forecasts.csv", index=False)
print("\nSaved: all_models_7day_forecasts.csv")


# ---------------------------------------------------------------
# COMPARISON PLOT — all five models
# ---------------------------------------------------------------
plt.figure(figsize=(12, 6))
for model_name, group in all_models_forecast.groupby("Model"):
    plt.plot(
        group["Forecast_Date"],
        group["Forecast_PM25"],
        marker="o",
        linewidth=2,
        label=model_name,
    )

plt.axhline(15, linestyle="--", linewidth=1, label="15 µg/m³ reference")
plt.axhline(35, linestyle=":", linewidth=1, label="35 µg/m³ reference")
plt.axhline(55, linestyle=":", linewidth=1, label="55 µg/m³ reference")
plt.title("Seven-Day PM2.5 Forecast Comparison — All Candidate Models")
plt.xlabel("Forecast date")
plt.ylabel("PM2.5 (µg/m³)")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("fig_all_models_7day_forecast.png", dpi=150)
plt.show()

print("Saved: fig_all_models_7day_forecast.png")
print("\nINTERPRETATION NOTE:")
print("Model 3 remains the dashboard deployment model. This cell only exposes")
print("the forecasts from all candidate models so you can inspect their behaviour")
print("after refitting on the complete available training record.")
print("Model 4 is a constant-weather scenario because future weather inputs were")
print("not available in the study dataset.")
