# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-09-22 00:28:39
**Output Directory:** `2109_model_test-20250922-002632`

## Executive Summary

This report presents nowcasting results for **4 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| CPI Year-over-Year | DFM2-044-v12-002633 | DFM2 | 0.6013 | 0.5062 | N/A |
| GDP Year-over-Year | AR1-004-v04-002724 | AR1 | 2.2174 | 0.9495 | N/A |
| Policy Rate (7DRR) | AR1-007-v07-002816 | AR1 | 0.3129 | 0.2625 | N/A |
| USD/IDR Exchange Rate | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 1.0604 | 0.3129 | 3 |
| DFM | 2.0431 | 0.9478 | 3 |
| DFM2 | 1.1507 | 0.6013 | 3 |
| ElasticNet | 1.2726 | 0.6426 | 3 |
| ElasticNetGrid | 1.2566 | 0.5941 | 3 |
| Lasso | 1.2555 | 0.6484 | 3 |
| RandomForest | 2.0088 | 0.9330 | 3 |
| Ridge | 1.1861 | 0.5629 | 3 |
| StandardizedRidge | 1.1551 | 0.4993 | 3 |

## 1. CPI Year-over-Year

### Top 5 Models (Diverse Selection)

**1. DFM2 Model 🏆**
- ID: `DFM2-044-v12-002633`
- RMSE (H=1): 0.6013
- MAE (H=1): 0.5062
- RMSE (H=3): 1.0647
- RMSE (H=6): 1.5228
- Degradation: H3=+77.1%, H6=+153.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-122-v10-002724`
- RMSE (H=1): 0.6401
- MAE (H=1): 0.5462
- RMSE (H=3): 1.2042
- RMSE (H=6): 1.8836
- Degradation: H3=+88.1%, H6=+194.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**3. ElasticNet Model**
- ID: `ElasticNet-049-v01-002633`
- RMSE (H=1): 0.6426
- MAE (H=1): 0.5446
- RMSE (H=3): 1.1344
- RMSE (H=6): 1.6314
- Degradation: H3=+76.5%, H6=+153.9%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-142-v14-002724`
- RMSE (H=1): 0.6437
- MAE (H=1): 0.5480
- RMSE (H=3): 1.2141
- RMSE (H=6): 1.9114
- Degradation: H3=+88.6%, H6=+196.9%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. Lasso Model**
- ID: `Lasso-081-v01-002719`
- RMSE (H=1): 0.6484
- MAE (H=1): 0.5536
- RMSE (H=3): 1.1275
- RMSE (H=6): 1.6227
- Degradation: H3=+73.9%, H6=+150.3%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-013-v13-002632 | 0.6510 | +8.3% |
| DFM | DFM-030-v14-002633 | 1.7394 | +189.3% |
| DFM2 | DFM2-044-v12-002633 | 0.6013 | 0.0% |
| ElasticNet | ElasticNet-049-v01-002633 | 0.6426 | +6.9% |
| ElasticNetGrid | ElasticNetGrid-080-v16-002718 | 0.8452 | +40.6% |
| Lasso | Lasso-081-v01-002719 | 0.6484 | +7.8% |
| RandomForest | RandomForest-103-v07-002722 | 1.4117 | +134.8% |
| Ridge | Ridge-122-v10-002724 | 0.6401 | +6.5% |
| StandardizedRidge | StandardizedRidge-142-v14-002724 | 0.6437 | +7.1% |

### Forecast Visualizations

#### 1. DFM2 Model Forecast
![DFM2 Forecast](2109_model_test-20250922-002632/visualizations/cpi_yoy_dfm2_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](2109_model_test-20250922-002632/visualizations/cpi_yoy_ridge_rank2.png)

#### 3. ElasticNet Model Forecast
![ElasticNet Forecast](2109_model_test-20250922-002632/visualizations/cpi_yoy_elasticnet_rank3.png)

#### All Models Comparison
![CPI Year-over-Year Comparison](2109_model_test-20250922-002632/visualizations/cpi_yoy_comparison.png)

---

## 2. GDP Year-over-Year

### Top 5 Models (Diverse Selection)

**1. AR1 Model 🏆**
- ID: `AR1-004-v04-002724`
- RMSE (H=1): 2.2174
- MAE (H=1): 0.9495
- RMSE (H=3): 3.0399
- RMSE (H=6): 4.2724
- Degradation: H3=+37.1%, H6=+92.7%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**2. DFM2 Model**
- ID: `DFM2-044-v12-002725`
- RMSE (H=1): 2.2327
- MAE (H=1): 0.9892
- RMSE (H=3): 3.0983
- RMSE (H=6): 4.6517
- Degradation: H3=+38.8%, H6=+108.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**3. Lasso Model**
- ID: `Lasso-092-v12-002811`
- RMSE (H=1): 2.3144
- MAE (H=1): 1.3265
- RMSE (H=3): 2.7908
- RMSE (H=6): 3.5068
- Degradation: H3=+20.6%, H6=+51.5%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**4. ElasticNet Model**
- ID: `ElasticNet-052-v04-002726`
- RMSE (H=1): 2.3169
- MAE (H=1): 1.3320
- RMSE (H=3): 2.7863
- RMSE (H=6): 3.5102
- Degradation: H3=+20.3%, H6=+51.5%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**5. StandardizedRidge Model**
- ID: `StandardizedRidge-132-v04-002815`
- RMSE (H=1): 2.3223
- MAE (H=1): 1.0691
- RMSE (H=3): 3.2700
- RMSE (H=6): 5.1546
- Degradation: H3=+40.8%, H6=+122.0%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-004-v04-002724 | 2.2174 | 0.0% |
| DFM | DFM-024-v08-002725 | 3.4423 | +55.2% |
| DFM2 | DFM2-044-v12-002725 | 2.2327 | +0.7% |
| ElasticNet | ElasticNet-052-v04-002726 | 2.3169 | +4.5% |
| ElasticNetGrid | ElasticNetGrid-080-v16-002809 | 2.3306 | +5.1% |
| Lasso | Lasso-092-v12-002811 | 2.3144 | +4.4% |
| RandomForest | RandomForest-106-v10-002813 | 3.6815 | +66.0% |
| Ridge | Ridge-124-v12-002815 | 2.3554 | +6.2% |
| StandardizedRidge | StandardizedRidge-132-v04-002815 | 2.3223 | +4.7% |

### Forecast Visualizations

#### 1. AR1 Model Forecast
![AR1 Forecast](2109_model_test-20250922-002632/visualizations/gdp_yoy_ar1_rank1.png)

#### 2. DFM2 Model Forecast
![DFM2 Forecast](2109_model_test-20250922-002632/visualizations/gdp_yoy_dfm2_rank2.png)

#### 3. Lasso Model Forecast
![Lasso Forecast](2109_model_test-20250922-002632/visualizations/gdp_yoy_lasso_rank3.png)

#### All Models Comparison
![GDP Year-over-Year Comparison](2109_model_test-20250922-002632/visualizations/gdp_yoy_comparison.png)

---

## 3. Policy Rate (7DRR)

### Top 5 Models (Diverse Selection)

**1. AR1 Model 🏆**
- ID: `AR1-007-v07-002816`
- RMSE (H=1): 0.3129
- MAE (H=1): 0.2625
- RMSE (H=3): 0.5851
- RMSE (H=6): 0.9634
- Degradation: H3=+87.0%, H6=+207.9%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**2. StandardizedRidge Model**
- ID: `StandardizedRidge-133-v05-002838`
- RMSE (H=1): 0.4993
- MAE (H=1): 0.4257
- RMSE (H=3): 0.9797
- RMSE (H=6): 1.6692
- Degradation: H3=+96.2%, H6=+234.3%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**3. Ridge Model**
- ID: `Ridge-114-v02-002838`
- RMSE (H=1): 0.5629
- MAE (H=1): 0.5037
- RMSE (H=3): 1.0549
- RMSE (H=6): 1.6053
- Degradation: H3=+87.4%, H6=+185.2%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**4. ElasticNetGrid Model**
- ID: `ElasticNetGrid-080-v16-002836`
- RMSE (H=1): 0.5941
- MAE (H=1): 0.4706
- RMSE (H=3): 0.9021
- RMSE (H=6): 1.6229
- Degradation: H3=+51.9%, H6=+173.2%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. DFM2 Model**
- ID: `DFM2-047-v15-002817`
- RMSE (H=1): 0.6182
- MAE (H=1): 0.5475
- RMSE (H=3): 1.0759
- RMSE (H=6): 1.5090
- Degradation: H3=+74.1%, H6=+144.1%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-007-v07-002816 | 0.3129 | 0.0% |
| DFM | DFM-030-v14-002817 | 0.9478 | +203.0% |
| DFM2 | DFM2-047-v15-002817 | 0.6182 | +97.6% |
| ElasticNet | ElasticNet-057-v09-002818 | 0.8584 | +174.4% |
| ElasticNetGrid | ElasticNetGrid-080-v16-002836 | 0.5941 | +89.9% |
| Lasso | Lasso-081-v01-002836 | 0.8036 | +156.9% |
| RandomForest | RandomForest-105-v09-002838 | 0.9330 | +198.2% |
| Ridge | Ridge-114-v02-002838 | 0.5629 | +79.9% |
| StandardizedRidge | StandardizedRidge-133-v05-002838 | 0.4993 | +59.6% |

### Forecast Visualizations

#### 1. AR1 Model Forecast
![AR1 Forecast](2109_model_test-20250922-002632/visualizations/policy_rate_7drr_ar1_rank1.png)

#### 2. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](2109_model_test-20250922-002632/visualizations/policy_rate_7drr_standardizedridge_rank2.png)

#### 3. Ridge Model Forecast
![Ridge Forecast](2109_model_test-20250922-002632/visualizations/policy_rate_7drr_ridge_rank3.png)

#### All Models Comparison
![Policy Rate (7DRR) Comparison](2109_model_test-20250922-002632/visualizations/policy_rate_7drr_comparison.png)

---

## 4. USD/IDR Exchange Rate

*No valid results found for USD/IDR Exchange Rate*

## Key Insights

1. **AR1 models** performed best on 2/4 targets, suggesting strong autoregressive patterns
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
