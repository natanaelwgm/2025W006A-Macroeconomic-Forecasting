# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-09 11:30:16
**Output Directory:** `corrected_comprehensive_quarterly-20251009-112642`

## Executive Summary

This report presents nowcasting results for **11 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | SeasonalNaive-057-v01-112806 | SeasonalNaive | 0.6564 | 0.4417 | 0.6383 |
| Cpi | SeasonalNaive-058-v02-112658 | SeasonalNaive | 1.2331 | 0.9181 | 0.1744 |
| Deposit Rate 12M | StandardizedRidge-066-v02-112924 | StandardizedRidge | 0.4768 | 0.4364 | 0.7121 |
| Deposit Rate 1M | Naive-042-v02-112823 | Naive | 0.6185 | 0.4869 | 0.3835 |
| Deposit Rate 3M | SeasonalNaive-058-v02-112845 | SeasonalNaive | 0.6834 | 0.5654 | 0.4939 |
| Deposit Rate 6M | SeasonalNaive-057-v01-112904 | SeasonalNaive | 0.6975 | 0.6188 | 0.4975 |
| Fx | *No valid models* | - | N/A | N/A | N/A |
| Money Supply | *No valid models* | - | N/A | N/A | N/A |
| Real Gdp Growth | Ridge-053-v01-112726 | Ridge | 3.2732 | 1.9351 | 0.0142 |
| Stock Index | *No valid models* | - | N/A | N/A | N/A |
| Informal Employment | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 1.7264 | 0.8139 | 7 |
| BVAR | 1.8512 | 0.5244 | 7 |
| DFM | 1.6804 | 0.5921 | 7 |
| DFM2 | 1.7736 | 0.5682 | 7 |
| ElasticNet | 1.8138 | 1.2103 | 7 |
| ElasticNetGrid | 1.8079 | 1.1867 | 7 |
| ExtraTrees | 2.0759 | 1.1176 | 7 |
| Huber | 2.2871 | 1.0366 | 7 |
| Lasso | 1.8856 | 1.1543 | 7 |
| Linear | 2.2871 | 1.0366 | 7 |
| Naive | 1.1773 | 0.6185 | 7 |
| PLS1 | 1.8671 | 0.5577 | 7 |
| RandomForest | 2.0429 | 1.1182 | 7 |
| Ridge | 1.6438 | 0.5633 | 7 |
| SeasonalNaive | 1.1773 | 0.6185 | 7 |
| StandardizedLinear | 2.2871 | 1.0366 | 7 |
| StandardizedRidge | 2.8640 | 0.4768 | 7 |
| Tree | 2.0317 | 1.1176 | 7 |
| XGBoost | 1.9109 | 1.3830 | 7 |

## 1. Bi7Drr

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-057-v01-112806`
- RMSE (H=1): 0.6564
- MAE (H=1): 0.4417
- R² (H=1): 0.6383
- MAPE: 9.1%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-041-v01-112803`
- RMSE (H=1): 0.6564
- MAE (H=1): 0.4417
- R² (H=1): 0.6383
- MAPE: 9.1%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-112753`
- RMSE (H=1): 0.8139
- MAE (H=1): 0.7740
- R² (H=1): 0.4437
- MAPE: 17.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. Tree Model**
- ID: `Tree-070-v02-112808`
- RMSE (H=1): 1.1176
- MAE (H=1): 1.0448
- R² (H=1): -0.0488
- MAPE: 24.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. ExtraTrees Model**
- ID: `ExtraTrees-025-v01-112759`
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
| AR1 | AR1-001-v01-112753 | 0.8139 | +24.0% |
| BVAR | BVAR-006-v02-112753 | 1.9187 | +192.3% |
| DFM | DFM-010-v02-112754 | 1.6851 | +156.7% |
| DFM2 | DFM2-014-v02-112755 | 1.4996 | +128.5% |
| ElasticNet | ElasticNet-018-v02-112756 | 1.2103 | +84.4% |
| ElasticNetGrid | ElasticNetGrid-022-v02-112758 | 1.1867 | +80.8% |
| ExtraTrees | ExtraTrees-025-v01-112759 | 1.1176 | +70.3% |
| Huber | Huber-029-v01-112800 | 2.3477 | +257.7% |
| Lasso | Lasso-034-v02-112801 | 1.1543 | +75.9% |
| Linear | Linear-037-v01-112802 | 2.3477 | +257.7% |
| Naive | Naive-041-v01-112803 | 0.6564 | 0.0% |
| PLS1 | PLS1-046-v02-112804 | 1.8488 | +181.7% |
| RandomForest | RandomForest-050-v02-112804 | 1.1182 | +70.4% |
| Ridge | Ridge-054-v02-112805 | 1.6004 | +143.8% |
| SeasonalNaive | SeasonalNaive-057-v01-112806 | 0.6564 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-112806 | 2.3477 | +257.7% |
| StandardizedRidge | StandardizedRidge-066-v02-112807 | 1.7549 | +167.4% |
| Tree | Tree-070-v02-112808 | 1.1176 | +70.3% |
| XGBoost | XGBoost-074-v02-112812 | 1.3830 | +110.7% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/BI7DRR_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/BI7DRR_naive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/BI7DRR_ar1_rank3.png)

#### All Models Comparison
![Bi7Drr Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/BI7DRR_comparison.png)

---

## 2. Cpi

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-058-v02-112658`
- RMSE (H=1): 1.2331
- MAE (H=1): 0.9181
- R² (H=1): 0.1744
- MAPE: 43.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-041-v01-112655`
- RMSE (H=1): 1.2331
- MAE (H=1): 0.9181
- R² (H=1): 0.1744
- MAPE: 43.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-112644`
- RMSE (H=1): 1.3163
- MAE (H=1): 1.1685
- R² (H=1): 0.0592
- MAPE: 68.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. XGBoost Model**
- ID: `XGBoost-073-v01-112703`
- RMSE (H=1): 1.4043
- MAE (H=1): 1.1973
- R² (H=1): -0.0706
- MAPE: 68.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. Tree Model**
- ID: `Tree-069-v01-112700`
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
| AR1 | AR1-001-v01-112644 | 1.3163 | +6.8% |
| BVAR | BVAR-006-v02-112645 | 3.0365 | +146.3% |
| DFM | DFM-009-v01-112646 | 1.4851 | +20.4% |
| DFM2 | DFM2-014-v02-112647 | 1.4976 | +21.4% |
| ElasticNet | ElasticNet-018-v02-112648 | 1.5514 | +25.8% |
| ElasticNetGrid | ElasticNetGrid-021-v01-112650 | 1.5580 | +26.3% |
| ExtraTrees | ExtraTrees-025-v01-112652 | 1.4514 | +17.7% |
| Huber | Huber-030-v02-112653 | 2.9426 | +138.6% |
| Lasso | Lasso-033-v01-112653 | 1.5380 | +24.7% |
| Linear | Linear-038-v02-112655 | 2.9426 | +138.6% |
| Naive | Naive-041-v01-112655 | 1.2331 | 0.0% |
| PLS1 | PLS1-046-v02-112656 | 1.6853 | +36.7% |
| RandomForest | RandomForest-049-v01-112657 | 1.4348 | +16.4% |
| Ridge | Ridge-053-v01-112658 | 2.1294 | +72.7% |
| SeasonalNaive | SeasonalNaive-058-v02-112658 | 1.2331 | 0.0% |
| StandardizedLinear | StandardizedLinear-062-v02-112659 | 2.9426 | +138.6% |
| StandardizedRidge | StandardizedRidge-065-v01-112700 | 2.7268 | +121.1% |
| Tree | Tree-069-v01-112700 | 1.4144 | +14.7% |
| XGBoost | XGBoost-073-v01-112703 | 1.4043 | +13.9% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/CPI_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/CPI_naive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/CPI_ar1_rank3.png)

#### All Models Comparison
![Cpi Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/CPI_comparison.png)

---

## 3. Deposit Rate 12M

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-066-v02-112924`
- RMSE (H=1): 0.4768
- MAE (H=1): 0.4364
- R² (H=1): 0.7121
- MAPE: 9.5%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. BVAR Model**
- ID: `BVAR-005-v01-112913`
- RMSE (H=1): 0.5244
- MAE (H=1): 0.3679
- R² (H=1): 0.6518
- MAPE: 7.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. PLS1 Model**
- ID: `PLS1-046-v02-112921`
- RMSE (H=1): 0.5577
- MAE (H=1): 0.4403
- R² (H=1): 0.6061
- MAPE: 10.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. Ridge Model**
- ID: `Ridge-054-v02-112922`
- RMSE (H=1): 0.5633
- MAE (H=1): 0.4690
- R² (H=1): 0.5981
- MAPE: 10.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. DFM2 Model**
- ID: `DFM2-014-v02-112914`
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
| AR1 | AR1-002-v02-112912 | 1.0211 | +114.2% |
| BVAR | BVAR-005-v01-112913 | 0.5244 | +10.0% |
| DFM | DFM-010-v02-112913 | 0.5921 | +24.2% |
| DFM2 | DFM2-014-v02-112914 | 0.5682 | +19.2% |
| ElasticNet | ElasticNet-017-v01-112915 | 1.2984 | +172.3% |
| ElasticNetGrid | ElasticNetGrid-022-v02-112917 | 1.2593 | +164.1% |
| ExtraTrees | ExtraTrees-026-v02-112917 | 1.9342 | +305.7% |
| Huber | Huber-029-v01-112918 | 1.0727 | +125.0% |
| Lasso | Lasso-034-v02-112919 | 1.4226 | +198.4% |
| Linear | Linear-037-v01-112919 | 1.0727 | +125.0% |
| Naive | Naive-041-v01-112920 | 0.7247 | +52.0% |
| PLS1 | PLS1-046-v02-112921 | 0.5577 | +17.0% |
| RandomForest | RandomForest-050-v02-112922 | 1.8829 | +294.9% |
| Ridge | Ridge-054-v02-112922 | 0.5633 | +18.2% |
| SeasonalNaive | SeasonalNaive-058-v02-112923 | 0.7247 | +52.0% |
| StandardizedLinear | StandardizedLinear-061-v01-112924 | 1.0727 | +125.0% |
| StandardizedRidge | StandardizedRidge-066-v02-112924 | 0.4768 | 0.0% |
| Tree | Tree-069-v01-112925 | 1.9013 | +298.8% |
| XGBoost | XGBoost-073-v01-112927 | 1.5970 | +235.0% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 12M_standardizedridge_rank1.png)

#### 2. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 12M_bvar_rank2.png)

#### 3. PLS1 Model Forecast
![PLS1 Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 12M_pls1_rank3.png)

#### All Models Comparison
![Deposit Rate 12M Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 12M_comparison.png)

---

## 4. Deposit Rate 1M

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-042-v02-112823`
- RMSE (H=1): 0.6185
- MAE (H=1): 0.4869
- R² (H=1): 0.3835
- MAPE: 12.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-058-v02-112826`
- RMSE (H=1): 0.6185
- MAE (H=1): 0.4869
- R² (H=1): 0.3835
- MAPE: 12.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-005-v01-112814`
- RMSE (H=1): 1.0949
- MAE (H=1): 0.8962
- R² (H=1): -0.9319
- MAPE: 24.6%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-066-v02-112827`
- RMSE (H=1): 1.5295
- MAE (H=1): 1.3542
- R² (H=1): -2.7698
- MAPE: 37.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. AR1 Model**
- ID: `AR1-001-v01-112813`
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
| AR1 | AR1-001-v01-112813 | 1.6149 | +161.1% |
| BVAR | BVAR-005-v01-112814 | 1.0949 | +77.0% |
| DFM | DFM-010-v02-112815 | 1.8444 | +198.2% |
| DFM2 | DFM2-013-v01-112816 | 1.8744 | +203.0% |
| ElasticNet | ElasticNet-017-v01-112816 | 1.9317 | +212.3% |
| ElasticNetGrid | ElasticNetGrid-022-v02-112819 | 2.3543 | +280.6% |
| ExtraTrees | ExtraTrees-026-v02-112820 | 2.2027 | +256.1% |
| Huber | Huber-029-v01-112821 | 2.4256 | +292.2% |
| Lasso | Lasso-034-v02-112822 | 2.1033 | +240.1% |
| Linear | Linear-037-v01-112822 | 2.4256 | +292.2% |
| Naive | Naive-042-v02-112823 | 0.6185 | 0.0% |
| PLS1 | PLS1-046-v02-112824 | 2.6405 | +326.9% |
| RandomForest | RandomForest-050-v02-112824 | 2.1732 | +251.4% |
| Ridge | Ridge-054-v02-112825 | 1.6870 | +172.8% |
| SeasonalNaive | SeasonalNaive-058-v02-112826 | 0.6185 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-112826 | 2.4256 | +292.2% |
| StandardizedRidge | StandardizedRidge-066-v02-112827 | 1.5295 | +147.3% |
| Tree | Tree-070-v02-112828 | 2.1241 | +243.4% |
| XGBoost | XGBoost-074-v02-112832 | 1.9898 | +221.7% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 1M_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 1M_seasonalnaive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 1M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 1M Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 1M_comparison.png)

---

## 5. Deposit Rate 3M

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-058-v02-112845`
- RMSE (H=1): 0.6834
- MAE (H=1): 0.5654
- R² (H=1): 0.4939
- MAPE: 13.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-042-v02-112842`
- RMSE (H=1): 0.6834
- MAE (H=1): 0.5654
- R² (H=1): 0.4939
- MAPE: 13.2%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-006-v02-112834`
- RMSE (H=1): 0.9461
- MAE (H=1): 0.7680
- R² (H=1): 0.0302
- MAPE: 20.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-066-v02-112846`
- RMSE (H=1): 0.9895
- MAE (H=1): 0.7261
- R² (H=1): -0.0609
- MAPE: 20.0%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. StandardizedLinear Model**
- ID: `StandardizedLinear-061-v01-112845`
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
| AR1 | AR1-002-v02-112834 | 1.4177 | +107.4% |
| BVAR | BVAR-006-v02-112834 | 0.9461 | +38.4% |
| DFM | DFM-010-v02-112835 | 1.4119 | +106.6% |
| DFM2 | DFM2-014-v02-112836 | 1.6452 | +140.7% |
| ElasticNet | ElasticNet-017-v01-112836 | 1.6230 | +137.5% |
| ElasticNetGrid | ElasticNetGrid-022-v02-112838 | 1.4024 | +105.2% |
| ExtraTrees | ExtraTrees-026-v02-112839 | 2.0866 | +205.3% |
| Huber | Huber-029-v01-112840 | 1.0366 | +51.7% |
| Lasso | Lasso-034-v02-112840 | 1.7667 | +158.5% |
| Linear | Linear-037-v01-112841 | 1.0366 | +51.7% |
| Naive | Naive-042-v02-112842 | 0.6834 | 0.0% |
| PLS1 | PLS1-046-v02-112843 | 1.5205 | +122.5% |
| RandomForest | RandomForest-050-v02-112844 | 2.0322 | +197.4% |
| Ridge | Ridge-054-v02-112844 | 1.1994 | +75.5% |
| SeasonalNaive | SeasonalNaive-058-v02-112845 | 0.6834 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-112845 | 1.0366 | +51.7% |
| StandardizedRidge | StandardizedRidge-066-v02-112846 | 0.9895 | +44.8% |
| Tree | Tree-070-v02-112847 | 2.0277 | +196.7% |
| XGBoost | XGBoost-073-v01-112849 | 1.9026 | +178.4% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 3M_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 3M_naive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 3M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 3M Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 3M_comparison.png)

---

## 6. Deposit Rate 6M

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-057-v01-112904`
- RMSE (H=1): 0.6975
- MAE (H=1): 0.6188
- R² (H=1): 0.4975
- MAPE: 13.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-042-v02-112901`
- RMSE (H=1): 0.6975
- MAE (H=1): 0.6188
- R² (H=1): 0.4975
- MAPE: 13.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-006-v02-112854`
- RMSE (H=1): 0.7013
- MAE (H=1): 0.5973
- R² (H=1): 0.4920
- MAPE: 14.3%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-066-v02-112905`
- RMSE (H=1): 0.7775
- MAE (H=1): 0.6347
- R² (H=1): 0.3756
- MAPE: 15.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. Ridge Model**
- ID: `Ridge-054-v02-112903`
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
| AR1 | AR1-002-v02-112853 | 1.3564 | +94.5% |
| BVAR | BVAR-006-v02-112854 | 0.7013 | +0.5% |
| DFM | DFM-010-v02-112854 | 1.1795 | +69.1% |
| DFM2 | DFM2-014-v02-112855 | 1.1652 | +67.0% |
| ElasticNet | ElasticNet-017-v01-112856 | 1.6182 | +132.0% |
| ElasticNetGrid | ElasticNetGrid-022-v02-112858 | 1.3252 | +90.0% |
| ExtraTrees | ExtraTrees-026-v02-112859 | 2.1746 | +211.8% |
| Huber | Huber-029-v01-112859 | 1.3067 | +87.3% |
| Lasso | Lasso-034-v02-112900 | 1.6966 | +143.2% |
| Linear | Linear-037-v01-112900 | 1.3067 | +87.3% |
| Naive | Naive-042-v02-112901 | 0.6975 | 0.0% |
| PLS1 | PLS1-046-v02-112902 | 1.1057 | +58.5% |
| RandomForest | RandomForest-050-v02-112903 | 2.1295 | +205.3% |
| Ridge | Ridge-054-v02-112903 | 1.0537 | +51.1% |
| SeasonalNaive | SeasonalNaive-057-v01-112904 | 0.6975 | 0.0% |
| StandardizedLinear | StandardizedLinear-061-v01-112904 | 1.3067 | +87.3% |
| StandardizedRidge | StandardizedRidge-066-v02-112905 | 0.7775 | +11.5% |
| Tree | Tree-070-v02-112906 | 2.0838 | +198.7% |
| XGBoost | XGBoost-074-v02-112910 | 1.8160 | +160.3% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 6M_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 6M_naive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 6M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 6M Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/Deposit Rate 6M_comparison.png)

---

## 7. Fx

*No valid results found for Fx*

## 8. Money Supply

*No valid results found for Money Supply*

## 9. Real Gdp Growth

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-053-v01-112726`
- RMSE (H=1): 3.2732
- MAE (H=1): 1.9351
- R² (H=1): 0.0142
- MAPE: 65.8%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**2. XGBoost Model**
- ID: `XGBoost-073-v01-112732`
- RMSE (H=1): 3.2839
- MAE (H=1): 1.9323
- R² (H=1): 0.0078
- MAPE: 67.6%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**3. ElasticNet Model**
- ID: `ElasticNet-018-v02-112713`
- RMSE (H=1): 3.4634
- MAE (H=1): 1.9534
- R² (H=1): -0.1037
- MAPE: 81.4%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**4. Lasso Model**
- ID: `Lasso-034-v02-112722`
- RMSE (H=1): 3.5174
- MAE (H=1): 1.8618
- R² (H=1): -0.1384
- MAPE: 81.7%
- Features: 6 variables
- Normalization: None
- Feature Pack: None

**5. RandomForest Model**
- ID: `RandomForest-049-v01-112725`
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
| AR1 | AR1-001-v01-112709 | 4.5448 | +38.8% |
| BVAR | BVAR-005-v01-112710 | 4.7362 | +44.7% |
| DFM | DFM-010-v02-112711 | 3.5645 | +8.9% |
| DFM2 | DFM2-013-v01-112712 | 4.1649 | +27.2% |
| ElasticNet | ElasticNet-018-v02-112713 | 3.4634 | +5.8% |
| ElasticNetGrid | ElasticNetGrid-021-v01-112714 | 3.5692 | +9.0% |
| ExtraTrees | ExtraTrees-025-v01-112720 | 3.5642 | +8.9% |
| Huber | Huber-030-v02-112721 | 4.8779 | +49.0% |
| Lasso | Lasso-034-v02-112722 | 3.5174 | +7.5% |
| Linear | Linear-038-v02-112723 | 4.8779 | +49.0% |
| Naive | Naive-041-v01-112724 | 3.6273 | +10.8% |
| PLS1 | PLS1-046-v02-112724 | 3.7111 | +13.4% |
| RandomForest | RandomForest-049-v01-112725 | 3.5293 | +7.8% |
| Ridge | Ridge-053-v01-112726 | 3.2732 | 0.0% |
| SeasonalNaive | SeasonalNaive-057-v01-112727 | 3.6273 | +10.8% |
| StandardizedLinear | StandardizedLinear-062-v02-112728 | 4.8779 | +49.0% |
| StandardizedRidge | StandardizedRidge-065-v01-112729 | 11.7932 | +260.3% |
| Tree | Tree-069-v01-112730 | 3.5529 | +8.5% |
| XGBoost | XGBoost-073-v01-112732 | 3.2839 | +0.3% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Real GDP Growth_ridge_rank1.png)

#### 2. XGBoost Model Forecast
![XGBoost Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Real GDP Growth_xgboost_rank2.png)

#### 3. ElasticNet Model Forecast
![ElasticNet Forecast](corrected_comprehensive_quarterly-20251009-112642/visualizations/Real GDP Growth_elasticnet_rank3.png)

#### All Models Comparison
![Real Gdp Growth Comparison](corrected_comprehensive_quarterly-20251009-112642/visualizations/Real GDP Growth_comparison.png)

---

## 10. Stock Index

*No valid results found for Stock Index*

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
