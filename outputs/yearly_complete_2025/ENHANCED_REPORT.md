# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:45:27
**Output Directory:** `yearly_complete_2025`

## Executive Summary

This report presents nowcasting results for **11 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | *No valid models* | - | N/A | N/A | N/A |
| Cpi | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 12M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 1M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 3M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 6M | *No valid models* | - | N/A | N/A | N/A |
| Fx | *No valid models* | - | N/A | N/A | N/A |
| Govt Bond Yield 10 Yr | *No valid models* | - | N/A | N/A | N/A |
| Jisdor Exchange Rate | *No valid models* | - | N/A | N/A | N/A |
| Real Gdp Growth | *No valid models* | - | N/A | N/A | N/A |
| Informal Employment | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|

## 1. Bi7Drr

*No valid results found for Bi7Drr*

## 2. Cpi

*No valid results found for Cpi*

## 3. Deposit Rate 12M

*No valid results found for Deposit Rate 12M*

## 4. Deposit Rate 1M

*No valid results found for Deposit Rate 1M*

## 5. Deposit Rate 3M

*No valid results found for Deposit Rate 3M*

## 6. Deposit Rate 6M

*No valid results found for Deposit Rate 6M*

## 7. Fx

*No valid results found for Fx*

## 8. Govt Bond Yield 10 Yr

*No valid results found for Govt Bond Yield 10 Yr*

## 9. Jisdor Exchange Rate

*No valid results found for Jisdor Exchange Rate*

## 10. Real Gdp Growth

*No valid results found for Real Gdp Growth*

## 11. Informal Employment

*No valid results found for Informal Employment*

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
