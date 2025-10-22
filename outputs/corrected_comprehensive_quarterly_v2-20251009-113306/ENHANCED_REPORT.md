# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:11:41
**Output Directory:** `corrected_comprehensive_quarterly_v2-20251009-113306`

## Executive Summary

This report presents nowcasting results for **11 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | Naive-041-v01-113421 | Naive | 0.6564 | 0.4417 | 0.6383 |
| Cpi | Naive-041-v01-113318 | Naive | 1.2331 | 0.9181 | 0.1744 |
| Deposit Rate 12M | StandardizedRidge-066-v02-113601 | StandardizedRidge | 0.4768 | 0.4364 | 0.7121 |
| Deposit Rate 1M | Naive-042-v02-113445 | Naive | 0.6185 | 0.4869 | 0.3835 |
| Deposit Rate 3M | Naive-042-v02-113507 | Naive | 0.6834 | 0.5654 | 0.4939 |
| Deposit Rate 6M | Naive-042-v02-113531 | Naive | 0.6975 | 0.6188 | 0.4975 |
| Fx | *No valid models* | - | N/A | N/A | N/A |
| Govt Bond Yield 10 Yr | SeasonalNaive-058-v02-113621 | SeasonalNaive | 0.4582 | 0.3338 | -0.7902 |
| Jisdor Exchange Rate | SeasonalNaive-057-v01-113646 | SeasonalNaive | 518.6005 | 428.5853 | N/A |
| Real Gdp Growth | Ridge-053-v01-113343 | Ridge | 3.2732 | 1.9351 | 0.0142 |
| Informal Employment | Naive-002-v01-080648 | Naive | 2486.8733 | 2073.5012 | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 530.3676 | 0.6435 | 10 |
| BVAR | 143.8055 | 0.5244 | 9 |
| DFM | 121.6453 | 0.5921 | 9 |
| DFM2 | 89.8379 | 0.5682 | 9 |
| ElasticNet | 167.5354 | 0.7829 | 9 |
| ElasticNetGrid | 138.1801 | 0.7341 | 9 |
| ExtraTrees | 160.5125 | 0.7325 | 9 |
| Huber | 95.0774 | 1.0366 | 9 |
| Lasso | 170.8853 | 0.7676 | 9 |
| Linear | 161.6738 | 1.0366 | 9 |
| Naive | 301.4173 | 0.4582 | 10 |
| PLS1 | 89.9650 | 0.5577 | 9 |
| RandomForest | 150.7849 | 0.7269 | 9 |
| Ridge | 108.1676 | 0.5633 | 9 |
| SeasonalNaive | 301.4173 | 0.4582 | 10 |
| StandardizedLinear | 161.6738 | 1.0366 | 9 |
| StandardizedRidge | 109.6841 | 0.4768 | 9 |
| Tree | 155.8952 | 0.7528 | 9 |
| XGBoost | 130.0301 | 1.1513 | 9 |

## 1. Bi7Drr

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-041-v01-113421`
- RMSE (H=1): 0.6564
- MAE (H=1): 0.4417
- R² (H=1): 0.6383
- MAPE: 9.1%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-058-v02-113425`
- RMSE (H=1): 0.6564
- MAE (H=1): 0.4417
- R² (H=1): 0.6383
- MAPE: 9.1%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-113412`
- RMSE (H=1): 0.8139
- MAE (H=1): 0.7740
- R² (H=1): 0.4437
- MAPE: 17.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. Tree Model**
- ID: `Tree-070-v02-113428`
- RMSE (H=1): 1.1176
- MAE (H=1): 1.0448
- R² (H=1): -0.0488
- MAPE: 24.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. ExtraTrees Model**
- ID: `ExtraTrees-025-v01-113418`
- RMSE (H=1): 1.1176
- MAE (H=1): 1.0448
- R² (H=1): -0.0488
- MAPE: 24.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-113412 | 0.8139 | +24.0% |
| BVAR | BVAR-006-v02-113413 | 1.9187 | +192.3% |
| DFM | DFM-010-v02-113414 | 1.6851 | +156.7% |
| DFM2 | DFM2-014-v02-113414 | 1.4996 | +128.5% |
| ElasticNet | ElasticNet-018-v02-113415 | 1.2103 | +84.4% |
| ElasticNetGrid | ElasticNetGrid-022-v02-113418 | 1.1867 | +80.8% |
| ExtraTrees | ExtraTrees-025-v01-113418 | 1.1176 | +70.3% |
| Huber | Huber-029-v01-113419 | 2.3477 | +257.7% |
| Lasso | Lasso-034-v02-113420 | 1.1543 | +75.9% |
| Linear | Linear-037-v01-113421 | 2.3477 | +257.7% |
| Naive | Naive-041-v01-113421 | 0.6564 | 0.0% |
| PLS1 | PLS1-046-v02-113422 | 1.8488 | +181.7% |
| RandomForest | RandomForest-050-v02-113423 | 1.1182 | +70.4% |
| Ridge | Ridge-054-v02-113424 | 1.6004 | +143.8% |
| SeasonalNaive | SeasonalNaive-058-v02-113425 | 0.6564 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113426 | 2.3477 | +257.7% |
| StandardizedRidge | StandardizedRidge-066-v02-113427 | 1.7549 | +167.4% |
| Tree | Tree-070-v02-113428 | 1.1176 | +70.3% |
| XGBoost | XGBoost-074-v02-113432 | 1.3830 | +110.7% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/BI7DRR_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/BI7DRR_seasonalnaive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/BI7DRR_ar1_rank3.png)

#### All Models Comparison
![Bi7Drr Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/BI7DRR_comparison.png)

---

## 2. Cpi

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-041-v01-113318`
- RMSE (H=1): 1.2331
- MAE (H=1): 0.9181
- R² (H=1): 0.1744
- MAPE: 43.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-057-v01-113321`
- RMSE (H=1): 1.2331
- MAE (H=1): 0.9181
- R² (H=1): 0.1744
- MAPE: 43.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-113309`
- RMSE (H=1): 1.3163
- MAE (H=1): 1.1685
- R² (H=1): 0.0592
- MAPE: 68.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. XGBoost Model**
- ID: `XGBoost-073-v01-113326`
- RMSE (H=1): 1.4043
- MAE (H=1): 1.1973
- R² (H=1): -0.0706
- MAPE: 68.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. Tree Model**
- ID: `Tree-069-v01-113324`
- RMSE (H=1): 1.4144
- MAE (H=1): 1.2213
- R² (H=1): -0.0862
- MAPE: 70.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-113309 | 1.3163 | +6.8% |
| BVAR | BVAR-006-v02-113310 | 3.0365 | +146.3% |
| DFM | DFM-009-v01-113311 | 1.4851 | +20.4% |
| DFM2 | DFM2-014-v02-113312 | 1.4976 | +21.4% |
| ElasticNet | ElasticNet-018-v02-113313 | 1.5514 | +25.8% |
| ElasticNetGrid | ElasticNetGrid-021-v01-113313 | 1.5580 | +26.3% |
| ExtraTrees | ExtraTrees-025-v01-113315 | 1.4514 | +17.7% |
| Huber | Huber-030-v02-113316 | 2.9426 | +138.6% |
| Lasso | Lasso-033-v01-113317 | 1.5380 | +24.7% |
| Linear | Linear-038-v02-113318 | 2.9426 | +138.6% |
| Naive | Naive-041-v01-113318 | 1.2331 | 0.0% |
| PLS1 | PLS1-046-v02-113319 | 1.6853 | +36.7% |
| RandomForest | RandomForest-049-v01-113320 | 1.4348 | +16.4% |
| Ridge | Ridge-053-v01-113320 | 2.1294 | +72.7% |
| SeasonalNaive | SeasonalNaive-057-v01-113321 | 1.2331 | 0.0% |
| StandardizedLinear | StandardizedLinear-062-v02-113323 | 2.9426 | +138.6% |
| StandardizedRidge | StandardizedRidge-065-v01-113323 | 2.7268 | +121.1% |
| Tree | Tree-069-v01-113324 | 1.4144 | +14.7% |
| XGBoost | XGBoost-073-v01-113326 | 1.4043 | +13.9% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/CPI_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/CPI_seasonalnaive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/CPI_ar1_rank3.png)

#### All Models Comparison
![Cpi Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/CPI_comparison.png)

---

## 3. Deposit Rate 12M

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-066-v02-113601`
- RMSE (H=1): 0.4768
- MAE (H=1): 0.4364
- R² (H=1): 0.7121
- MAPE: 9.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. BVAR Model**
- ID: `BVAR-005-v01-113545`
- RMSE (H=1): 0.5244
- MAE (H=1): 0.3679
- R² (H=1): 0.6518
- MAPE: 7.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. PLS1 Model**
- ID: `PLS1-046-v02-113556`
- RMSE (H=1): 0.5577
- MAE (H=1): 0.4403
- R² (H=1): 0.6061
- MAPE: 10.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. Ridge Model**
- ID: `Ridge-054-v02-113558`
- RMSE (H=1): 0.5633
- MAE (H=1): 0.4690
- R² (H=1): 0.5981
- MAPE: 10.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. DFM2 Model**
- ID: `DFM2-014-v02-113547`
- RMSE (H=1): 0.5682
- MAE (H=1): 0.4493
- R² (H=1): 0.5911
- MAPE: 10.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-113545 | 1.0211 | +114.2% |
| BVAR | BVAR-005-v01-113545 | 0.5244 | +10.0% |
| DFM | DFM-010-v02-113546 | 0.5921 | +24.2% |
| DFM2 | DFM2-014-v02-113547 | 0.5682 | +19.2% |
| ElasticNet | ElasticNet-017-v01-113548 | 1.2984 | +172.3% |
| ElasticNetGrid | ElasticNetGrid-022-v02-113550 | 1.2593 | +164.1% |
| ExtraTrees | ExtraTrees-026-v02-113551 | 1.9342 | +305.7% |
| Huber | Huber-029-v01-113551 | 1.0727 | +125.0% |
| Lasso | Lasso-034-v02-113552 | 1.4226 | +198.4% |
| Linear | Linear-037-v01-113553 | 1.0727 | +125.0% |
| Naive | Naive-042-v02-113555 | 0.7247 | +52.0% |
| PLS1 | PLS1-046-v02-113556 | 0.5577 | +17.0% |
| RandomForest | RandomForest-050-v02-113558 | 1.8829 | +294.9% |
| Ridge | Ridge-054-v02-113558 | 0.5633 | +18.2% |
| SeasonalNaive | SeasonalNaive-058-v02-113559 | 0.7247 | +52.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113600 | 1.0727 | +125.0% |
| StandardizedRidge | StandardizedRidge-066-v02-113601 | 0.4768 | 0.0% |
| Tree | Tree-069-v01-113601 | 1.9013 | +298.8% |
| XGBoost | XGBoost-073-v01-113603 | 1.5970 | +235.0% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 12M_standardizedridge_rank1.png)

#### 2. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 12M_bvar_rank2.png)

#### 3. PLS1 Model Forecast
![PLS1 Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 12M_pls1_rank3.png)

#### All Models Comparison
![Deposit Rate 12M Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 12M_comparison.png)

---

## 4. Deposit Rate 1M

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-042-v02-113445`
- RMSE (H=1): 0.6185
- MAE (H=1): 0.4869
- R² (H=1): 0.3835
- MAPE: 12.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-058-v02-113449`
- RMSE (H=1): 0.6185
- MAE (H=1): 0.4869
- R² (H=1): 0.3835
- MAPE: 12.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-005-v01-113435`
- RMSE (H=1): 1.0949
- MAE (H=1): 0.8962
- R² (H=1): -0.9319
- MAPE: 24.6%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-066-v02-113450`
- RMSE (H=1): 1.5295
- MAE (H=1): 1.3542
- R² (H=1): -2.7698
- MAPE: 37.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. AR1 Model**
- ID: `AR1-002-v02-113435`
- RMSE (H=1): 1.6149
- MAE (H=1): 1.4998
- R² (H=1): -3.2022
- MAPE: 40.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-113435 | 1.6149 | +161.1% |
| BVAR | BVAR-005-v01-113435 | 1.0949 | +77.0% |
| DFM | DFM-010-v02-113436 | 1.8444 | +198.2% |
| DFM2 | DFM2-013-v01-113437 | 1.8744 | +203.0% |
| ElasticNet | ElasticNet-017-v01-113438 | 1.9317 | +212.3% |
| ElasticNetGrid | ElasticNetGrid-022-v02-113440 | 2.3543 | +280.6% |
| ExtraTrees | ExtraTrees-026-v02-113442 | 2.2027 | +256.1% |
| Huber | Huber-029-v01-113442 | 2.4256 | +292.2% |
| Lasso | Lasso-034-v02-113443 | 2.1033 | +240.1% |
| Linear | Linear-037-v01-113444 | 2.4256 | +292.2% |
| Naive | Naive-042-v02-113445 | 0.6185 | 0.0% |
| PLS1 | PLS1-046-v02-113446 | 2.6405 | +326.9% |
| RandomForest | RandomForest-050-v02-113447 | 2.1732 | +251.4% |
| Ridge | Ridge-054-v02-113448 | 1.6870 | +172.8% |
| SeasonalNaive | SeasonalNaive-058-v02-113449 | 0.6185 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113449 | 2.4256 | +292.2% |
| StandardizedRidge | StandardizedRidge-066-v02-113450 | 1.5295 | +147.3% |
| Tree | Tree-070-v02-113451 | 2.1241 | +243.4% |
| XGBoost | XGBoost-074-v02-113456 | 1.9898 | +221.7% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 1M_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 1M_seasonalnaive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 1M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 1M Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 1M_comparison.png)

---

## 5. Deposit Rate 3M

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-042-v02-113507`
- RMSE (H=1): 0.6834
- MAE (H=1): 0.5654
- R² (H=1): 0.4939
- MAPE: 13.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-058-v02-113511`
- RMSE (H=1): 0.6834
- MAE (H=1): 0.5654
- R² (H=1): 0.4939
- MAPE: 13.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-006-v02-113459`
- RMSE (H=1): 0.9461
- MAE (H=1): 0.7680
- R² (H=1): 0.0302
- MAPE: 20.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-066-v02-113513`
- RMSE (H=1): 0.9895
- MAE (H=1): 0.7261
- R² (H=1): -0.0609
- MAPE: 20.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. StandardizedLinear Model**
- ID: `StandardizedLinear-061-v01-113511`
- RMSE (H=1): 1.0366
- MAE (H=1): 0.8258
- R² (H=1): -0.1643
- MAPE: 21.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-113458 | 1.4177 | +107.4% |
| BVAR | BVAR-006-v02-113459 | 0.9461 | +38.4% |
| DFM | DFM-010-v02-113459 | 1.4119 | +106.6% |
| DFM2 | DFM2-014-v02-113500 | 1.6452 | +140.7% |
| ElasticNet | ElasticNet-017-v01-113501 | 1.6230 | +137.5% |
| ElasticNetGrid | ElasticNetGrid-022-v02-113503 | 1.4024 | +105.2% |
| ExtraTrees | ExtraTrees-026-v02-113504 | 2.0866 | +205.3% |
| Huber | Huber-029-v01-113505 | 1.0366 | +51.7% |
| Lasso | Lasso-034-v02-113506 | 1.7667 | +158.5% |
| Linear | Linear-037-v01-113506 | 1.0366 | +51.7% |
| Naive | Naive-042-v02-113507 | 0.6834 | 0.0% |
| PLS1 | PLS1-046-v02-113508 | 1.5205 | +122.5% |
| RandomForest | RandomForest-050-v02-113509 | 2.0322 | +197.4% |
| Ridge | Ridge-054-v02-113510 | 1.1994 | +75.5% |
| SeasonalNaive | SeasonalNaive-058-v02-113511 | 0.6834 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113511 | 1.0366 | +51.7% |
| StandardizedRidge | StandardizedRidge-066-v02-113513 | 0.9895 | +44.8% |
| Tree | Tree-070-v02-113514 | 2.0277 | +196.7% |
| XGBoost | XGBoost-073-v01-113515 | 1.9026 | +178.4% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 3M_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 3M_seasonalnaive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 3M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 3M Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 3M_comparison.png)

---

## 6. Deposit Rate 6M

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-042-v02-113531`
- RMSE (H=1): 0.6975
- MAE (H=1): 0.6188
- R² (H=1): 0.4975
- MAPE: 13.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-058-v02-113534`
- RMSE (H=1): 0.6975
- MAE (H=1): 0.6188
- R² (H=1): 0.4975
- MAPE: 13.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-006-v02-113521`
- RMSE (H=1): 0.7013
- MAE (H=1): 0.5973
- R² (H=1): 0.4920
- MAPE: 14.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-066-v02-113536`
- RMSE (H=1): 0.7775
- MAE (H=1): 0.6347
- R² (H=1): 0.3756
- MAPE: 15.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. Ridge Model**
- ID: `Ridge-054-v02-113533`
- RMSE (H=1): 1.0537
- MAE (H=1): 0.9061
- R² (H=1): -0.1469
- MAPE: 22.1%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-113521 | 1.3564 | +94.5% |
| BVAR | BVAR-006-v02-113521 | 0.7013 | +0.5% |
| DFM | DFM-010-v02-113522 | 1.1795 | +69.1% |
| DFM2 | DFM2-014-v02-113523 | 1.1652 | +67.0% |
| ElasticNet | ElasticNet-017-v01-113524 | 1.6182 | +132.0% |
| ElasticNetGrid | ElasticNetGrid-022-v02-113526 | 1.3252 | +90.0% |
| ExtraTrees | ExtraTrees-026-v02-113527 | 2.1746 | +211.8% |
| Huber | Huber-029-v01-113528 | 1.3067 | +87.3% |
| Lasso | Lasso-034-v02-113529 | 1.6966 | +143.2% |
| Linear | Linear-037-v01-113530 | 1.3067 | +87.3% |
| Naive | Naive-042-v02-113531 | 0.6975 | 0.0% |
| PLS1 | PLS1-046-v02-113531 | 1.1057 | +58.5% |
| RandomForest | RandomForest-050-v02-113532 | 2.1295 | +205.3% |
| Ridge | Ridge-054-v02-113533 | 1.0537 | +51.1% |
| SeasonalNaive | SeasonalNaive-058-v02-113534 | 0.6975 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113534 | 1.3067 | +87.3% |
| StandardizedRidge | StandardizedRidge-066-v02-113536 | 0.7775 | +11.5% |
| Tree | Tree-070-v02-113537 | 2.0838 | +198.7% |
| XGBoost | XGBoost-074-v02-113542 | 1.8160 | +160.3% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 6M_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 6M_seasonalnaive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 6M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 6M Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Deposit Rate 6M_comparison.png)

---

## 7. Fx

*No valid results found for Fx*

## 8. Govt Bond Yield 10 Yr

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-058-v02-113621`
- RMSE (H=1): 0.4582
- MAE (H=1): 0.3338
- R² (H=1): -0.7902
- MAPE: 4.9%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-042-v02-113618`
- RMSE (H=1): 0.4582
- MAE (H=1): 0.3338
- R² (H=1): -0.7902
- MAPE: 4.9%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-002-v02-113608`
- RMSE (H=1): 0.6435
- MAE (H=1): 0.5872
- R² (H=1): -2.5302
- MAPE: 8.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. RandomForest Model**
- ID: `RandomForest-049-v01-113619`
- RMSE (H=1): 0.7269
- MAE (H=1): 0.6762
- R² (H=1): -3.5050
- MAPE: 10.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. ExtraTrees Model**
- ID: `ExtraTrees-025-v01-113614`
- RMSE (H=1): 0.7325
- MAE (H=1): 0.6801
- R² (H=1): -3.5745
- MAPE: 10.1%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-113608 | 0.6435 | +40.4% |
| BVAR | BVAR-005-v01-113608 | 1.1500 | +151.0% |
| DFM | DFM-009-v01-113609 | 0.7960 | +73.7% |
| DFM2 | DFM2-013-v01-113610 | 1.0164 | +121.8% |
| ElasticNet | ElasticNet-018-v02-113611 | 0.7829 | +70.9% |
| ElasticNetGrid | ElasticNetGrid-021-v01-113612 | 0.7341 | +60.2% |
| ExtraTrees | ExtraTrees-025-v01-113614 | 0.7325 | +59.9% |
| Huber | Huber-029-v01-113615 | 1.5661 | +241.8% |
| Lasso | Lasso-033-v01-113616 | 0.7676 | +67.5% |
| Linear | Linear-037-v01-113617 | 1.5661 | +241.8% |
| Naive | Naive-042-v02-113618 | 0.4582 | 0.0% |
| PLS1 | PLS1-045-v01-113618 | 1.1605 | +153.3% |
| RandomForest | RandomForest-049-v01-113619 | 0.7269 | +58.6% |
| Ridge | Ridge-053-v01-113620 | 1.0524 | +129.7% |
| SeasonalNaive | SeasonalNaive-058-v02-113621 | 0.4582 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113622 | 1.5661 | +241.8% |
| StandardizedRidge | StandardizedRidge-065-v01-113623 | 0.9770 | +113.2% |
| Tree | Tree-070-v02-113624 | 0.7528 | +64.3% |
| XGBoost | XGBoost-073-v01-113626 | 1.1513 | +151.2% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Govt Bond Yield 10 Yr_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Govt Bond Yield 10 Yr_naive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Govt Bond Yield 10 Yr_ar1_rank3.png)

#### All Models Comparison
![Govt Bond Yield 10 Yr Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Govt Bond Yield 10 Yr_comparison.png)

---

## 9. Jisdor Exchange Rate

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-057-v01-113646`
- RMSE (H=1): 518.6005
- MAE (H=1): 428.5853
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-042-v02-113643`
- RMSE (H=1): 518.6005
- MAE (H=1): 428.5853
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-113631`
- RMSE (H=1): 757.5115
- MAE (H=1): 639.2490
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. DFM2 Model**
- ID: `DFM2-013-v01-113634`
- RMSE (H=1): 795.1095
- MAE (H=1): 714.8473
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. PLS1 Model**
- ID: `PLS1-045-v01-113644`
- RMSE (H=1): 795.4546
- MAE (H=1): 748.1710
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-113631 | 757.5115 | +46.1% |
| BVAR | BVAR-005-v01-113632 | 1280.1414 | +146.8% |
| DFM | DFM-010-v02-113633 | 1082.2487 | +108.7% |
| DFM2 | DFM2-013-v01-113634 | 795.1095 | +53.3% |
| ElasticNet | ElasticNet-018-v02-113635 | 1494.3390 | +188.1% |
| ElasticNetGrid | ElasticNetGrid-022-v02-113638 | 1230.2317 | +137.2% |
| ExtraTrees | ExtraTrees-026-v02-113639 | 1429.3490 | +175.6% |
| Huber | Huber-029-v01-113639 | 838.1210 | +61.6% |
| Lasso | Lasso-034-v02-113641 | 1524.0017 | +193.9% |
| Linear | Linear-037-v01-113642 | 1437.4881 | +177.2% |
| Naive | Naive-042-v02-113643 | 518.6005 | 0.0% |
| PLS1 | PLS1-045-v01-113644 | 795.4546 | +53.4% |
| RandomForest | RandomForest-050-v02-113645 | 1342.0373 | +158.8% |
| Ridge | Ridge-053-v01-113646 | 960.9493 | +85.3% |
| SeasonalNaive | SeasonalNaive-057-v01-113646 | 518.6005 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-113647 | 1437.4881 | +177.2% |
| StandardizedRidge | StandardizedRidge-065-v01-113648 | 966.1314 | +86.3% |
| Tree | Tree-070-v02-113649 | 1388.0822 | +167.7% |
| XGBoost | XGBoost-074-v02-113655 | 1155.7428 | +122.9% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/JISDOR Exchange Rate_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/JISDOR Exchange Rate_naive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/JISDOR Exchange Rate_ar1_rank3.png)

#### All Models Comparison
![Jisdor Exchange Rate Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/JISDOR Exchange Rate_comparison.png)

---

## 10. Real Gdp Growth

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-053-v01-113343`
- RMSE (H=1): 3.2732
- MAE (H=1): 1.9351
- R² (H=1): 0.0142
- MAPE: 65.8%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. XGBoost Model**
- ID: `XGBoost-073-v01-113348`
- RMSE (H=1): 3.2839
- MAE (H=1): 1.9323
- R² (H=1): 0.0078
- MAPE: 67.6%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. ElasticNet Model**
- ID: `ElasticNet-018-v02-113333`
- RMSE (H=1): 3.4634
- MAE (H=1): 1.9534
- R² (H=1): -0.1037
- MAPE: 81.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. Lasso Model**
- ID: `Lasso-034-v02-113339`
- RMSE (H=1): 3.5174
- MAE (H=1): 1.8618
- R² (H=1): -0.1384
- MAPE: 81.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. RandomForest Model**
- ID: `RandomForest-049-v01-113342`
- RMSE (H=1): 3.5293
- MAE (H=1): 1.7932
- R² (H=1): -0.1461
- MAPE: 80.6%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-113330 | 4.5448 | +38.8% |
| BVAR | BVAR-005-v01-113331 | 4.7362 | +44.7% |
| DFM | DFM-010-v02-113332 | 3.5645 | +8.9% |
| DFM2 | DFM2-013-v01-113332 | 4.1649 | +27.2% |
| ElasticNet | ElasticNet-018-v02-113333 | 3.4634 | +5.8% |
| ElasticNetGrid | ElasticNetGrid-021-v01-113334 | 3.5692 | +9.0% |
| ExtraTrees | ExtraTrees-025-v01-113336 | 3.5642 | +8.9% |
| Huber | Huber-030-v02-113338 | 4.8779 | +49.0% |
| Lasso | Lasso-034-v02-113339 | 3.5174 | +7.5% |
| Linear | Linear-038-v02-113340 | 4.8779 | +49.0% |
| Naive | Naive-041-v01-113341 | 3.6273 | +10.8% |
| PLS1 | PLS1-046-v02-113341 | 3.7111 | +13.4% |
| RandomForest | RandomForest-049-v01-113342 | 3.5293 | +7.8% |
| Ridge | Ridge-053-v01-113343 | 3.2732 | 0.0% |
| SeasonalNaive | SeasonalNaive-057-v01-113344 | 3.6273 | +10.8% |
| StandardizedLinear | StandardizedLinear-062-v02-113345 | 4.8779 | +49.0% |
| StandardizedRidge | StandardizedRidge-065-v01-113345 | 11.7932 | +260.3% |
| Tree | Tree-069-v01-113346 | 3.5529 | +8.5% |
| XGBoost | XGBoost-073-v01-113348 | 3.2839 | +0.3% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Real GDP Growth_ridge_rank1.png)

#### 2. XGBoost Model Forecast
![XGBoost Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Real GDP Growth_xgboost_rank2.png)

#### 3. ElasticNet Model Forecast
![ElasticNet Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Real GDP Growth_elasticnet_rank3.png)

#### All Models Comparison
![Real Gdp Growth Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/Real GDP Growth_comparison.png)

---

## 11. Informal Employment

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
![Naive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/informal_employment_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/informal_employment_seasonalnaive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/informal_employment_ar1_rank3.png)

#### All Models Comparison
![Informal Employment Comparison](corrected_comprehensive_quarterly_v2-20251009-113306/visualizations/informal_employment_comparison.png)

---

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
