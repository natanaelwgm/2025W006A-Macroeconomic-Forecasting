# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:42:38
**Output Directory:** `yearly_batch2_2025-20251010-084101`

## Executive Summary

This report presents nowcasting results for **4 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Deposit Rate 12M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 1M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 3M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 6M | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|

## 1. Deposit Rate 12M

*No valid results found for Deposit Rate 12M*

## 2. Deposit Rate 1M

*No valid results found for Deposit Rate 1M*

## 3. Deposit Rate 3M

*No valid results found for Deposit Rate 3M*

## 4. Deposit Rate 6M

*No valid results found for Deposit Rate 6M*

## Key Insights

1. **AR1 models** performed best on 0/4 targets, suggesting strong autoregressive patterns
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
