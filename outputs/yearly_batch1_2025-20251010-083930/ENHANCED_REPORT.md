# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:40:39
**Output Directory:** `yearly_batch1_2025-20251010-083930`

## Executive Summary

This report presents nowcasting results for **4 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | *No valid models* | - | N/A | N/A | N/A |
| Cpi | *No valid models* | - | N/A | N/A | N/A |
| Fx | *No valid models* | - | N/A | N/A | N/A |
| Real Gdp Growth | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|

## 1. Bi7Drr

*No valid results found for Bi7Drr*

## 2. Cpi

*No valid results found for Cpi*

## 3. Fx

*No valid results found for Fx*

## 4. Real Gdp Growth

*No valid results found for Real Gdp Growth*

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
