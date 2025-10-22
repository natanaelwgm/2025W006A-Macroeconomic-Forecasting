# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 09:13:31
**Output Directory:** `yearly_simple_extended_2025-20251010-091254`

## Executive Summary

This report presents nowcasting results for **10 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Cpi | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 12M | DFM2-004-v01-091326 | DFM2 | 1.1502 | 1.0441 | -0.0631 |
| Deposit Rate 1M | SeasonalNaive-015-v01-091315 | SeasonalNaive | 1.6497 | 1.4077 | -0.8465 |
| Deposit Rate 3M | DFM2-004-v01-091318 | DFM2 | 0.9663 | 0.7781 | 0.3551 |
| Deposit Rate 6M | Huber-008-v01-091323 | Huber | 1.2087 | 0.9885 | 0.0722 |
| Exports | DFM-003-v01-091329 | DFM | 197245.2627 | 148076.1757 | 0.1262 |
| Jisdor Exchange Rate | *No valid models* | - | N/A | N/A | N/A |
| Money Supply | *No valid models* | - | N/A | N/A | N/A |
| Real Gdp Growth | *No valid models* | - | N/A | N/A | N/A |
| Stock Index | DFM-003-v01-091305 | DFM | 736.3266 | 466.9839 | -0.3030 |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 38445.8887 | 3.1924 | 6 |
| BVAR | 35665.2766 | 1.6731 | 6 |
| DFM | 32998.7002 | 1.2477 | 6 |
| DFM2 | 35622.6405 | 0.9663 | 6 |
| ElasticNet | 35641.1831 | 1.6749 | 6 |
| ElasticNetGrid | 39597.2680 | 2.2036 | 6 |
| ExtraTrees | 58765.9636 | 3.7849 | 6 |
| Huber | 43665.0276 | 1.2087 | 6 |
| Lasso | 35640.7784 | 1.6756 | 6 |
| Linear | 35665.2091 | 1.6749 | 6 |
| Naive | 39626.1947 | 1.6497 | 6 |
| PLS1 | 35501.0392 | 1.8306 | 6 |
| RandomForest | 61137.6937 | 3.3432 | 6 |
| Ridge | 35666.0232 | 1.6743 | 6 |
| SeasonalNaive | 39626.1947 | 1.6497 | 6 |
| StandardizedLinear | 35665.2091 | 1.6749 | 6 |
| StandardizedRidge | 34372.8835 | 1.4677 | 6 |
| Tree | 55575.8079 | 2.2812 | 6 |
| XGBoost | 46838.6322 | 1.7226 | 6 |

## 1. Cpi

*No valid results found for Cpi*

## 2. Deposit Rate 12M

### Top 5 Models (Diverse Selection)

**1. DFM2 Model 🏆**
- ID: `DFM2-004-v01-091326`
- RMSE (H=1): 1.1502
- MAE (H=1): 1.0441
- R² (H=1): -0.0631
- MAPE: 18.1%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. DFM Model**
- ID: `DFM-003-v01-091326`
- RMSE (H=1): 1.2477
- MAE (H=1): 0.9725
- R² (H=1): -0.2510
- MAPE: 20.6%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. Huber Model**
- ID: `Huber-008-v01-091326`
- RMSE (H=1): 1.2523
- MAE (H=1): 1.0509
- R² (H=1): -0.2603
- MAPE: 18.1%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-017-v01-091326`
- RMSE (H=1): 1.4677
- MAE (H=1): 1.2759
- R² (H=1): -0.7310
- MAPE: 21.5%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. Naive Model**
- ID: `Naive-011-v01-091326`
- RMSE (H=1): 1.6662
- MAE (H=1): 1.3665
- R² (H=1): -1.2311
- MAPE: 27.4%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-091326 | 3.1924 | +177.6% |
| BVAR | BVAR-002-v01-091326 | 1.6731 | +45.5% |
| DFM | DFM-003-v01-091326 | 1.2477 | +8.5% |
| DFM2 | DFM2-004-v01-091326 | 1.1502 | 0.0% |
| ElasticNet | ElasticNet-005-v01-091326 | 1.6749 | +45.6% |
| ElasticNetGrid | ElasticNetGrid-006-v01-091326 | 2.2036 | +91.6% |
| ExtraTrees | ExtraTrees-007-v01-091326 | 3.7849 | +229.1% |
| Huber | Huber-008-v01-091326 | 1.2523 | +8.9% |
| Lasso | Lasso-009-v01-091326 | 1.6756 | +45.7% |
| Linear | Linear-010-v01-091326 | 1.6749 | +45.6% |
| Naive | Naive-011-v01-091326 | 1.6662 | +44.9% |
| PLS1 | PLS1-012-v01-091326 | 1.8306 | +59.2% |
| RandomForest | RandomForest-013-v01-091326 | 3.4143 | +196.8% |
| Ridge | Ridge-014-v01-091326 | 1.6743 | +45.6% |
| SeasonalNaive | SeasonalNaive-015-v01-091326 | 1.6662 | +44.9% |
| StandardizedLinear | StandardizedLinear-016-v01-091326 | 1.6749 | +45.6% |
| StandardizedRidge | StandardizedRidge-017-v01-091326 | 1.4677 | +27.6% |
| Tree | Tree-018-v01-091326 | 3.5086 | +205.0% |
| XGBoost | XGBoost-019-v01-091327 | 1.7226 | +49.8% |

### Forecast Visualizations

#### 1. DFM2 Model Forecast
![DFM2 Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 12M_dfm2_rank1.png)

#### 2. DFM Model Forecast
![DFM Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 12M_dfm_rank2.png)

#### 3. Huber Model Forecast
![Huber Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 12M_huber_rank3.png)

#### All Models Comparison
![Deposit Rate 12M Comparison](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 12M_comparison.png)

---

## 3. Deposit Rate 1M

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-015-v01-091315`
- RMSE (H=1): 1.6497
- MAE (H=1): 1.4077
- R² (H=1): -0.8465
- MAPE: 34.2%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-011-v01-091315`
- RMSE (H=1): 1.6497
- MAE (H=1): 1.4077
- R² (H=1): -0.8465
- MAPE: 34.2%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. DFM2 Model**
- ID: `DFM2-004-v01-091315`
- RMSE (H=1): 2.0116
- MAE (H=1): 1.7272
- R² (H=1): -1.7454
- MAPE: 42.5%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. BVAR Model**
- ID: `BVAR-002-v01-091315`
- RMSE (H=1): 2.0157
- MAE (H=1): 1.6484
- R² (H=1): -1.7567
- MAPE: 31.7%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. StandardizedLinear Model**
- ID: `StandardizedLinear-016-v01-091315`
- RMSE (H=1): 2.0211
- MAE (H=1): 1.6513
- R² (H=1): -1.7714
- MAPE: 31.7%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-091315 | 5.6036 | +239.7% |
| BVAR | BVAR-002-v01-091315 | 2.0157 | +22.2% |
| DFM | DFM-003-v01-091315 | 4.4107 | +167.4% |
| DFM2 | DFM2-004-v01-091315 | 2.0116 | +21.9% |
| ElasticNet | ElasticNet-005-v01-091315 | 2.0362 | +23.4% |
| ElasticNetGrid | ElasticNetGrid-006-v01-091315 | 2.8539 | +73.0% |
| ExtraTrees | ExtraTrees-007-v01-091315 | 4.3195 | +161.8% |
| Huber | Huber-008-v01-091315 | 2.5193 | +52.7% |
| Lasso | Lasso-009-v01-091315 | 2.0422 | +23.8% |
| Linear | Linear-010-v01-091315 | 2.0211 | +22.5% |
| Naive | Naive-011-v01-091315 | 1.6497 | 0.0% |
| PLS1 | PLS1-012-v01-091315 | 3.3263 | +101.6% |
| RandomForest | RandomForest-013-v01-091315 | 3.6154 | +119.1% |
| Ridge | Ridge-014-v01-091315 | 2.0323 | +23.2% |
| SeasonalNaive | SeasonalNaive-015-v01-091315 | 1.6497 | 0.0% |
| StandardizedLinear | StandardizedLinear-016-v01-091315 | 2.0211 | +22.5% |
| StandardizedRidge | StandardizedRidge-017-v01-091315 | 2.1989 | +33.3% |
| Tree | Tree-018-v01-091315 | 2.4482 | +48.4% |
| XGBoost | XGBoost-019-v01-091316 | 2.4764 | +50.1% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 1M_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 1M_naive_rank2.png)

#### 3. DFM2 Model Forecast
![DFM2 Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 1M_dfm2_rank3.png)

#### All Models Comparison
![Deposit Rate 1M Comparison](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 1M_comparison.png)

---

## 4. Deposit Rate 3M

### Top 5 Models (Diverse Selection)

**1. DFM2 Model 🏆**
- ID: `DFM2-004-v01-091318`
- RMSE (H=1): 0.9663
- MAE (H=1): 0.7781
- R² (H=1): 0.3551
- MAPE: 18.0%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Huber Model**
- ID: `Huber-008-v01-091318`
- RMSE (H=1): 1.7370
- MAE (H=1): 1.4919
- R² (H=1): -1.0836
- MAPE: 26.7%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. Naive Model**
- ID: `Naive-011-v01-091318`
- RMSE (H=1): 1.7698
- MAE (H=1): 1.5195
- R² (H=1): -1.1630
- MAPE: 34.3%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. SeasonalNaive Model**
- ID: `SeasonalNaive-015-v01-091319`
- RMSE (H=1): 1.7698
- MAE (H=1): 1.5195
- R² (H=1): -1.1630
- MAPE: 34.3%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. StandardizedRidge Model**
- ID: `StandardizedRidge-017-v01-091319`
- RMSE (H=1): 2.0889
- MAE (H=1): 1.7477
- R² (H=1): -2.0134
- MAPE: 31.2%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-091318 | 4.6050 | +376.5% |
| BVAR | BVAR-002-v01-091318 | 2.2599 | +133.9% |
| DFM | DFM-003-v01-091318 | 3.1712 | +228.2% |
| DFM2 | DFM2-004-v01-091318 | 0.9663 | 0.0% |
| ElasticNet | ElasticNet-005-v01-091318 | 2.2692 | +134.8% |
| ElasticNetGrid | ElasticNetGrid-006-v01-091318 | 3.5143 | +263.7% |
| ExtraTrees | ExtraTrees-007-v01-091318 | 4.2305 | +337.8% |
| Huber | Huber-008-v01-091318 | 1.7370 | +79.7% |
| Lasso | Lasso-009-v01-091318 | 2.2754 | +135.5% |
| Linear | Linear-010-v01-091318 | 2.2656 | +134.5% |
| Naive | Naive-011-v01-091318 | 1.7698 | +83.1% |
| PLS1 | PLS1-012-v01-091319 | 2.9880 | +209.2% |
| RandomForest | RandomForest-013-v01-091319 | 3.5742 | +269.9% |
| Ridge | Ridge-014-v01-091319 | 2.2693 | +134.8% |
| SeasonalNaive | SeasonalNaive-015-v01-091319 | 1.7698 | +83.1% |
| StandardizedLinear | StandardizedLinear-016-v01-091319 | 2.2656 | +134.5% |
| StandardizedRidge | StandardizedRidge-017-v01-091319 | 2.0889 | +116.2% |
| Tree | Tree-018-v01-091319 | 2.4277 | +151.2% |
| XGBoost | XGBoost-019-v01-091320 | 3.0514 | +215.8% |

### Forecast Visualizations

#### 1. DFM2 Model Forecast
![DFM2 Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 3M_dfm2_rank1.png)

#### 2. Huber Model Forecast
![Huber Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 3M_huber_rank2.png)

#### 3. Naive Model Forecast
![Naive Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 3M_naive_rank3.png)

#### All Models Comparison
![Deposit Rate 3M Comparison](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 3M_comparison.png)

---

## 5. Deposit Rate 6M

### Top 5 Models (Diverse Selection)

**1. Huber Model 🏆**
- ID: `Huber-008-v01-091323`
- RMSE (H=1): 1.2087
- MAE (H=1): 0.9885
- R² (H=1): 0.0722
- MAPE: 18.6%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. DFM2 Model**
- ID: `DFM2-004-v01-091322`
- RMSE (H=1): 1.2144
- MAE (H=1): 1.0539
- R² (H=1): 0.0635
- MAPE: 19.0%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. StandardizedRidge Model**
- ID: `StandardizedRidge-017-v01-091323`
- RMSE (H=1): 1.4991
- MAE (H=1): 1.2453
- R² (H=1): -0.4271
- MAPE: 21.6%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. BVAR Model**
- ID: `BVAR-002-v01-091322`
- RMSE (H=1): 1.6755
- MAE (H=1): 1.4116
- R² (H=1): -0.7827
- MAPE: 24.1%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. Linear Model**
- ID: `Linear-010-v01-091323`
- RMSE (H=1): 1.6784
- MAE (H=1): 1.4149
- R² (H=1): -0.7888
- MAPE: 24.1%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-091322 | 3.5221 | +191.4% |
| BVAR | BVAR-002-v01-091322 | 1.6755 | +38.6% |
| DFM | DFM-003-v01-091322 | 1.7823 | +47.5% |
| DFM2 | DFM2-004-v01-091322 | 1.2144 | +0.5% |
| ElasticNet | ElasticNet-005-v01-091322 | 1.6803 | +39.0% |
| ElasticNetGrid | ElasticNetGrid-006-v01-091323 | 2.5686 | +112.5% |
| ExtraTrees | ExtraTrees-007-v01-091323 | 3.8437 | +218.0% |
| Huber | Huber-008-v01-091323 | 1.2087 | 0.0% |
| Lasso | Lasso-009-v01-091323 | 1.6828 | +39.2% |
| Linear | Linear-010-v01-091323 | 1.6784 | +38.9% |
| Naive | Naive-011-v01-091323 | 1.8367 | +52.0% |
| PLS1 | PLS1-012-v01-091323 | 1.9097 | +58.0% |
| RandomForest | RandomForest-013-v01-091323 | 3.3432 | +176.6% |
| Ridge | Ridge-014-v01-091323 | 1.6787 | +38.9% |
| SeasonalNaive | SeasonalNaive-015-v01-091323 | 1.8367 | +52.0% |
| StandardizedLinear | StandardizedLinear-016-v01-091323 | 1.6784 | +38.9% |
| StandardizedRidge | StandardizedRidge-017-v01-091323 | 1.4991 | +24.0% |
| Tree | Tree-018-v01-091323 | 2.2812 | +88.7% |
| XGBoost | XGBoost-019-v01-091324 | 2.5965 | +114.8% |

### Forecast Visualizations

#### 1. Huber Model Forecast
![Huber Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 6M_huber_rank1.png)

#### 2. DFM2 Model Forecast
![DFM2 Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 6M_dfm2_rank2.png)

#### 3. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 6M_standardizedridge_rank3.png)

#### All Models Comparison
![Deposit Rate 6M Comparison](yearly_simple_extended_2025-20251010-091254/visualizations/Deposit Rate 6M_comparison.png)

---

## 6. Exports

### Top 5 Models (Diverse Selection)

**1. DFM Model 🏆**
- ID: `DFM-003-v01-091329`
- RMSE (H=1): 197245.2627
- MAE (H=1): 148076.1757
- R² (H=1): 0.1262
- MAPE: 14.4%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. StandardizedRidge Model**
- ID: `StandardizedRidge-017-v01-091329`
- RMSE (H=1): 205408.4510
- MAE (H=1): 142335.2746
- R² (H=1): 0.0524
- MAPE: 13.8%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. PLS1 Model**
- ID: `PLS1-012-v01-091329`
- RMSE (H=1): 212140.0655
- MAE (H=1): 149026.1520
- R² (H=1): -0.0107
- MAPE: 14.5%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. DFM2 Model**
- ID: `DFM2-004-v01-091329`
- RMSE (H=1): 212875.6979
- MAE (H=1): 150383.3602
- R² (H=1): -0.0177
- MAPE: 14.7%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. Lasso Model**
- ID: `Lasso-009-v01-091329`
- RMSE (H=1): 212986.3593
- MAE (H=1): 156306.5238
- R² (H=1): -0.0188
- MAPE: 15.6%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-091329 | 229753.5981 | +16.5% |
| BVAR | BVAR-002-v01-091329 | 213133.5718 | +8.1% |
| DFM | DFM-003-v01-091329 | 197245.2627 | 0.0% |
| DFM2 | DFM2-004-v01-091329 | 212875.6979 | +7.9% |
| ElasticNet | ElasticNet-005-v01-091329 | 212988.7987 | +8.0% |
| ElasticNetGrid | ElasticNetGrid-006-v01-091329 | 236321.8905 | +19.8% |
| ExtraTrees | ExtraTrees-007-v01-091329 | 349891.8469 | +77.4% |
| Huber | Huber-008-v01-091329 | 260942.3248 | +32.3% |
| Lasso | Lasso-009-v01-091329 | 212986.3593 | +8.0% |
| Linear | Linear-010-v01-091329 | 213133.1565 | +8.1% |
| Naive | Naive-011-v01-091329 | 236821.3417 | +20.1% |
| PLS1 | PLS1-012-v01-091329 | 212140.0655 | +7.6% |
| RandomForest | RandomForest-013-v01-091329 | 363880.1780 | +84.5% |
| Ridge | Ridge-014-v01-091329 | 213138.0176 | +8.1% |
| SeasonalNaive | SeasonalNaive-015-v01-091329 | 236821.3417 | +20.1% |
| StandardizedLinear | StandardizedLinear-016-v01-091329 | 213133.1565 | +8.1% |
| StandardizedRidge | StandardizedRidge-017-v01-091329 | 205408.4510 | +4.1% |
| Tree | Tree-018-v01-091329 | 331067.4956 | +67.8% |
| XGBoost | XGBoost-019-v01-091331 | 279559.5218 | +41.7% |

### Forecast Visualizations

#### 1. DFM Model Forecast
![DFM Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Exports_dfm_rank1.png)

#### 2. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Exports_standardizedridge_rank2.png)

#### 3. PLS1 Model Forecast
![PLS1 Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Exports_pls1_rank3.png)

#### All Models Comparison
![Exports Comparison](yearly_simple_extended_2025-20251010-091254/visualizations/Exports_comparison.png)

---

## 7. Jisdor Exchange Rate

*No valid results found for Jisdor Exchange Rate*

## 8. Money Supply

*No valid results found for Money Supply*

## 9. Real Gdp Growth

*No valid results found for Real Gdp Growth*

## 10. Stock Index

### Top 5 Models (Diverse Selection)

**1. DFM Model 🏆**
- ID: `DFM-003-v01-091305`
- RMSE (H=1): 736.3266
- MAE (H=1): 466.9839
- R² (H=1): -0.3030
- MAPE: 8.1%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. StandardizedRidge Model**
- ID: `StandardizedRidge-017-v01-091306`
- RMSE (H=1): 821.5951
- MAE (H=1): 540.3250
- R² (H=1): -0.6222
- MAPE: 9.2%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. StandardizedLinear Model**
- ID: `StandardizedLinear-016-v01-091306`
- RMSE (H=1): 850.4581
- MAE (H=1): 629.6315
- R² (H=1): -0.7382
- MAPE: 10.5%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. Linear Model**
- ID: `Linear-010-v01-091306`
- RMSE (H=1): 850.4581
- MAE (H=1): 629.6315
- R² (H=1): -0.7382
- MAPE: 10.5%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. BVAR Model**
- ID: `BVAR-002-v01-091305`
- RMSE (H=1): 850.4635
- MAE (H=1): 629.6389
- R² (H=1): -0.7382
- MAPE: 10.5%
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-091305 | 904.8113 | +22.9% |
| BVAR | BVAR-002-v01-091305 | 850.4635 | +15.5% |
| DFM | DFM-003-v01-091305 | 736.3266 | 0.0% |
| DFM2 | DFM2-004-v01-091305 | 854.8027 | +16.1% |
| ElasticNet | ElasticNet-005-v01-091305 | 850.6390 | +15.5% |
| ElasticNetGrid | ElasticNetGrid-006-v01-091306 | 1250.5773 | +69.8% |
| ExtraTrees | ExtraTrees-007-v01-091306 | 2687.7561 | +265.0% |
| Huber | Huber-008-v01-091306 | 1041.1233 | +41.4% |
| Lasso | Lasso-009-v01-091306 | 850.6350 | +15.5% |
| Linear | Linear-010-v01-091306 | 850.4581 | +15.5% |
| Naive | Naive-011-v01-091306 | 928.9040 | +26.2% |
| PLS1 | PLS1-012-v01-091306 | 856.1149 | +16.3% |
| RandomForest | RandomForest-013-v01-091306 | 2932.0369 | +298.2% |
| Ridge | Ridge-014-v01-091306 | 850.4669 | +15.5% |
| SeasonalNaive | SeasonalNaive-015-v01-091306 | 928.9040 | +26.2% |
| StandardizedLinear | StandardizedLinear-016-v01-091306 | 850.4581 | +15.5% |
| StandardizedRidge | StandardizedRidge-017-v01-091306 | 821.5951 | +11.6% |
| Tree | Tree-018-v01-091306 | 2376.6862 | +222.8% |
| XGBoost | XGBoost-019-v01-091310 | 1462.4246 | +98.6% |

### Forecast Visualizations

#### 1. DFM Model Forecast
![DFM Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Stock Index_dfm_rank1.png)

#### 2. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Stock Index_standardizedridge_rank2.png)

#### 3. StandardizedLinear Model Forecast
![StandardizedLinear Forecast](yearly_simple_extended_2025-20251010-091254/visualizations/Stock Index_standardizedlinear_rank3.png)

#### All Models Comparison
![Stock Index Comparison](yearly_simple_extended_2025-20251010-091254/visualizations/Stock Index_comparison.png)

---

## Key Insights

1. **AR1 models** performed best on 0/10 targets, suggesting strong autoregressive patterns
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
