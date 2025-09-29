# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-09-25 00:04:06
**Output Directory:** `yield_10y_sun_backtest-20250924-214716`

## Executive Summary

This report presents nowcasting results for **1 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| 10-Year Bond Yield | ExtraTrees-1023-v15-220412 | ExtraTrees | 0.3230 | 0.2546 | 0.2903 |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 0.3403 | 0.3403 | 1 |
| ARp | 0.5423 | 0.5423 | 1 |
| BVAR | 0.5367 | 0.5367 | 1 |
| DFM | 0.5151 | 0.5151 | 1 |
| DFM2 | 0.3295 | 0.3295 | 1 |
| ElasticNet | 0.3394 | 0.3394 | 1 |
| ElasticNetGrid | 0.3613 | 0.3613 | 1 |
| ExtraTrees | 0.3230 | 0.3230 | 1 |
| GARCH | 6.4340 | 6.4340 | 1 |
| GradientBoosting | 0.4276 | 0.4276 | 1 |
| LSTM | 0.4342 | 0.4342 | 1 |
| Lasso | 0.3344 | 0.3344 | 1 |
| Linear | 0.5423 | 0.5423 | 1 |
| RandomForest | 0.3374 | 0.3374 | 1 |
| Ridge | 0.4808 | 0.4808 | 1 |
| StandardizedLinear | 0.5423 | 0.5423 | 1 |
| StandardizedRidge | 0.5010 | 0.5010 | 1 |
| StochasticGB | 0.3472 | 0.3472 | 1 |
| Tree | 0.6607 | 0.6607 | 1 |
| XGBoost | 0.4910 | 0.4910 | 1 |

## 1. 10-Year Bond Yield

### Top 5 Models (Diverse Selection)

**1. ExtraTrees Model 🏆**
- ID: `ExtraTrees-1023-v15-220412`
- RMSE (H=1): 0.3230
- MAE (H=1): 0.2546
- R² (H=1): 0.2903
- MAPE: 3.7%
- RMSE (H=3): 0.4844
- RMSE (H=6): 0.6713
- Degradation: H3=+50.0%, H6=+107.9%
- Features: 20 variables
- Normalization: None
- Feature Pack: None

**2. DFM2 Model**
- ID: `DFM2-579-v03-215338`
- RMSE (H=1): 0.3295
- MAE (H=1): 0.2440
- R² (H=1): 0.2613
- MAPE: 3.5%
- RMSE (H=3): 0.3722
- RMSE (H=6): 0.5213
- Degradation: H3=+13.0%, H6=+58.2%
- Features: 20 variables
- Normalization: None
- Feature Pack: None

**3. Lasso Model**
- ID: `Lasso-1589-v05-222214`
- RMSE (H=1): 0.3344
- MAE (H=1): 0.2537
- R² (H=1): 0.2391
- MAPE: 3.6%
- RMSE (H=3): 0.4612
- RMSE (H=6): 0.6952
- Degradation: H3=+37.9%, H6=+107.9%
- Features: 20 variables
- Normalization: None
- Feature Pack: None

**4. RandomForest Model**
- ID: `RandomForest-1877-v05-222632`
- RMSE (H=1): 0.3374
- MAE (H=1): 0.2597
- R² (H=1): 0.2254
- MAPE: 3.8%
- RMSE (H=3): 0.5118
- RMSE (H=6): 0.7048
- Degradation: H3=+51.7%, H6=+108.9%
- Features: 20 variables
- Normalization: None
- Feature Pack: None

**5. ElasticNet Model**
- ID: `ElasticNet-725-v05-215522`
- RMSE (H=1): 0.3394
- MAE (H=1): 0.2571
- R² (H=1): 0.2162
- MAPE: 3.7%
- RMSE (H=3): 0.4744
- RMSE (H=6): 0.7041
- Degradation: H3=+39.8%, H6=+107.4%
- Features: 20 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-009-v09-214720 | 0.3403 | +5.4% |
| ARp | ARp-156-v12-214850 | 0.5423 | +67.9% |
| BVAR | BVAR-292-v04-215015 | 0.5367 | +66.2% |
| DFM | DFM-448-v16-215151 | 0.5151 | +59.5% |
| DFM2 | DFM2-579-v03-215338 | 0.3295 | +2.0% |
| ElasticNet | ElasticNet-725-v05-215522 | 0.3394 | +5.1% |
| ElasticNetGrid | ElasticNetGrid-941-v77-220207 | 0.3613 | +11.9% |
| ExtraTrees | ExtraTrees-1023-v15-220412 | 0.3230 | 0.0% |
| GARCH | GARCH-1169-v17-220642 | 6.4340 | +1892.0% |
| GradientBoosting | GradientBoosting-1315-v19-220854 | 0.4276 | +32.4% |
| LSTM | LSTM-1464-v24-221730 | 0.4342 | +34.4% |
| Lasso | Lasso-1589-v05-222214 | 0.3344 | +3.5% |
| Linear | Linear-1804-v76-222521 | 0.5423 | +67.9% |
| RandomForest | RandomForest-1877-v05-222632 | 0.3374 | +4.5% |
| Ridge | Ridge-2034-v18-222848 | 0.4808 | +48.9% |
| StandardizedLinear | StandardizedLinear-2164-v04-223047 | 0.5423 | +67.9% |
| StandardizedRidge | StandardizedRidge-2314-v10-223312 | 0.5010 | +55.1% |
| StochasticGB | StochasticGB-2524-v76-223617 | 0.3472 | +7.5% |
| Tree | Tree-2595-v03-223719 | 0.6607 | +104.6% |
| XGBoost | XGBoost-2747-v11-230528 | 0.4910 | +52.0% |

### Forecast Visualizations

#### 1. ExtraTrees Model Forecast
![ExtraTrees Forecast](yield_10y_sun_backtest-20250924-214716/visualizations/yield_10y_extratrees_rank1.png)

#### 2. DFM2 Model Forecast
![DFM2 Forecast](yield_10y_sun_backtest-20250924-214716/visualizations/yield_10y_dfm2_rank2.png)

#### 3. Lasso Model Forecast
![Lasso Forecast](yield_10y_sun_backtest-20250924-214716/visualizations/yield_10y_lasso_rank3.png)

#### All Models Comparison
![10-Year Bond Yield Comparison](yield_10y_sun_backtest-20250924-214716/visualizations/yield_10y_comparison.png)

---

## Key Insights

1. **AR1 models** performed best on 0/1 targets, suggesting strong autoregressive patterns
2. **Ensemble methods** appeared in top 3 for 1/1 targets
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
