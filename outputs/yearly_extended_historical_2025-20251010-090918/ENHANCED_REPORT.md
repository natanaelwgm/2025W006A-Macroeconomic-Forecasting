# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 09:11:29
**Output Directory:** `yearly_extended_historical_2025-20251010-090918`

## Executive Summary

This report presents nowcasting results for **15 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Cpi | *No valid models* | - | N/A | N/A | N/A |
| Crude Oil Price | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 12M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 1M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 3M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 6M | *No valid models* | - | N/A | N/A | N/A |
| Exports | *No valid models* | - | N/A | N/A | N/A |
| Government Expenditure | *No valid models* | - | N/A | N/A | N/A |
| Import Price Index | *No valid models* | - | N/A | N/A | N/A |
| Jibor | *No valid models* | - | N/A | N/A | N/A |
| Jisdor Exchange Rate | *No valid models* | - | N/A | N/A | N/A |
| Money Supply | *No valid models* | - | N/A | N/A | N/A |
| Motor Sales | *No valid models* | - | N/A | N/A | N/A |
| Real Gdp Growth | *No valid models* | - | N/A | N/A | N/A |
| Stock Index | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|

## 1. Cpi

*No valid results found for Cpi*

## 2. Crude Oil Price

*No valid results found for Crude Oil Price*

## 3. Deposit Rate 12M

*No valid results found for Deposit Rate 12M*

## 4. Deposit Rate 1M

*No valid results found for Deposit Rate 1M*

## 5. Deposit Rate 3M

*No valid results found for Deposit Rate 3M*

## 6. Deposit Rate 6M

*No valid results found for Deposit Rate 6M*

## 7. Exports

*No valid results found for Exports*

## 8. Government Expenditure

*No valid results found for Government Expenditure*

## 9. Import Price Index

*No valid results found for Import Price Index*

## 10. Jibor

*No valid results found for Jibor*

## 11. Jisdor Exchange Rate

*No valid results found for Jisdor Exchange Rate*

## 12. Money Supply

*No valid results found for Money Supply*

## 13. Motor Sales

*No valid results found for Motor Sales*

## 14. Real Gdp Growth

*No valid results found for Real Gdp Growth*

## 15. Stock Index

*No valid results found for Stock Index*

## Key Insights

1. **AR1 models** performed best on 0/15 targets, suggesting strong autoregressive patterns
3. **Forecast horizon degradation** is significant, with H=6 typically 50-100% worse than H=1

## Methodology

### Model Types Tested
- **AR1**: First-order autoregressive model
- **ARp**: Higher-order autoregressive model
- **Tree**: Single decision tree
- **RandomForest**: Bootstrap aggregated decision trees
- **GradientBoosting**: Sequential boosting with gradient descent
- **ExtraTrees**: Extremely randomized trees
- **StochasticGB**: Stochastic gradient boosting with subsampling

### Feature Engineering
- Target variable lags (1, 3, 12 months)
- Exogenous variable combinations
- Technical indicators (when applicable)
- Multiple normalization strategies
