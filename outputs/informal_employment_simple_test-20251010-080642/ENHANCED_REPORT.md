# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:07:03
**Output Directory:** `informal_employment_simple_test-20251010-080642`

## Executive Summary

This report presents nowcasting results for **1 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Informal Employment | Naive-002-v01-080648 | Naive | 2486.8733 | 2073.5012 | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 4533.4359 | 4533.4359 | 1 |
| Naive | 2486.8733 | 2486.8733 | 1 |
| SeasonalNaive | 2486.8733 | 2486.8733 | 1 |

## 1. Informal Employment

### Top 3 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-002-v01-080648`
- RMSE (H=1): 2486.8733
- MAE (H=1): 2073.5012
- Features: 1 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-003-v01-080648`
- RMSE (H=1): 2486.8733
- MAE (H=1): 2073.5012
- Features: 1 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-080647`
- RMSE (H=1): 4533.4359
- MAE (H=1): 3715.7596
- Features: 1 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-080647 | 4533.4359 | +82.3% |
| Naive | Naive-002-v01-080648 | 2486.8733 | 0.0% |
| SeasonalNaive | SeasonalNaive-003-v01-080648 | 2486.8733 | 0.0% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](informal_employment_simple_test-20251010-080642/visualizations/informal_employment_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](informal_employment_simple_test-20251010-080642/visualizations/informal_employment_seasonalnaive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](informal_employment_simple_test-20251010-080642/visualizations/informal_employment_ar1_rank3.png)

#### All Models Comparison
![Informal Employment Comparison](informal_employment_simple_test-20251010-080642/visualizations/informal_employment_comparison.png)

---

## Key Insights

1. **AR1 models** performed best on 0/1 targets, suggesting strong autoregressive patterns
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
