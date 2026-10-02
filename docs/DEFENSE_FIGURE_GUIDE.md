# Defense Figure Guide — Jali PM2.5 Dashboard

## 1. Missingness map
Shows where hourly PM2.5 observations were missing. The purpose is to demonstrate why preprocessing was necessary before modelling.

## 2. Before vs after imputation
The upper panel is the raw series with gaps; the lower panel is the continuous series after short-gap interpolation, hour-of-day means and boundary interpolation.

## 3. Missing counts
Shows the missing-observation burden before treatment and the cleaned modelling state.

## 4. Outlier boxplots
Shows the effect of the extreme sensor observations on the distribution. The 1.5×IQR rule was applied before imputation.

## 5. Outlier time series
Highlights flagged extreme observations. The raw maximum was 3,335.06 µg/m³; the modelling series was capped at 61.83 µg/m³.

## 6. Outlier distribution
Shows how capping reduces extreme skew while retaining the central observations.

## 7. Daily PM2.5 trend
Shows the final 727-day daily series. Use it to explain long-term variation and the changing pollution levels across the study period.

## 8. Monthly mean PM2.5
Aggregates the daily series by month. It helps explain seasonal/longer-term changes that are harder to see in the daily plot.

## 9. Weekday pattern
Compares average PM2.5 by weekday. The values are close together, so weekly structure should not be explained as a simple weekday/weekend effect.

## 10. Seven-day decomposition
Separates the observed series into trend, seven-day seasonal component and residual. This supports the use of weekly seasonality in the modelling process.

## 11. ACF/PACF
Shows temporal dependence after first differencing. Explain that ACF measures correlation with lagged observations and PACF isolates the direct contribution of a lag after intermediate lags are accounted for.

## 12. Model comparison
Shows RMSE, MAE and MAPE for Seasonal Naive, ARIMA, SARIMA, Random Forest, XGBoost and Prophet on the same 72-day chronological test set. Random Forest has the lowest values across all three metrics.

## 13. Native Random Forest forecast
Shows the selected model forecast for 1–7 March 2024, immediately after the final REMA observation. Forecasts range from 15.30 to 16.51 µg/m³. The shaded interval is an empirical residual-based uncertainty band from the notebook.

## 14. All-model test forecasts
Compares actual PM2.5 with every candidate model across the common test window. It visually complements the numerical metric table.

## 15. Zoomed comparison
Provides a shorter window to make differences among leading models easier to see.

## 16. Forecast error over time
Error is actual minus predicted. Positive values mean under-prediction; negative values mean over-prediction. Large spikes identify periods that were difficult to forecast.

## 17. Native vs current-window forecast
The native panel is historically verifiable because actual observations exist. The 2026 panel is only a capability demonstration because the underlying REMA data stop in 2024.

## 18. Forecast summary bars
Compares the seven-day diagnostic RMSE, the authoritative 72-day test RMSE and current-window mean forecasts. The 72-day RMSE is the model-selection basis.

## 19. Meteorological heatmap
Shows Pearson correlations over the 206-day REMA–Meteo overlap. Radiation has the largest absolute marginal association (r = −0.2511). Correlation does not prove causation.

## 20. SARIMAX coefficients
Shows coefficient estimates and 95% confidence intervals for the supplementary weather-informed model. Humidity, wind speed, lagged temperature and lagged humidity were significant at 5% in the final specification. These are associations, not causal effects, and the short overlap limits generalisation.

## Short defense formula
For almost every figure, answer in this order: **what it shows → why it was produced → what the main result is → how it affected the modelling decision → what limitation remains.**
