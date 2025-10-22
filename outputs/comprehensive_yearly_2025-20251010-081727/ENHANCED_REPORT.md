# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:27:09
**Output Directory:** `comprehensive_yearly_2025-20251010-081727`

## Executive Summary

This report presents nowcasting results for **11 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Cpi | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 12M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 1M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 3M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 6M | *No valid models* | - | N/A | N/A | N/A |
| Fx | *No valid models* | - | N/A | N/A | N/A |
| Fed Funds | *No valid models* | - | N/A | N/A | N/A |
| Jisdor Exchange Rate | *No valid models* | - | N/A | N/A | N/A |
| Money Supply | *No valid models* | - | N/A | N/A | N/A |
| Real Gdp Growth | *No valid models* | - | N/A | N/A | N/A |
| Stock Index | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|

## 1. Cpi

*No valid results found for Cpi*

## 2. Deposit Rate 12M

*No valid results found for Deposit Rate 12M*

## 3. Deposit Rate 1M

*No valid results found for Deposit Rate 1M*

## 4. Deposit Rate 3M

*No valid results found for Deposit Rate 3M*

## 5. Deposit Rate 6M

*No valid results found for Deposit Rate 6M*

## 6. Fx

*No valid results found for Fx*

## 7. Fed Funds

*No valid results found for Fed Funds*

## 8. Jisdor Exchange Rate

*No valid results found for Jisdor Exchange Rate*

## 9. Money Supply

*No valid results found for Money Supply*

## 10. Real Gdp Growth

*No valid results found for Real Gdp Growth*

## 11. Stock Index

*No valid results found for Stock Index*

## Key Insights

1. **AR1 models** performed best on 0/11 targets, suggesting strong autoregressive patterns
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
