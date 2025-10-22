# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 08:57:53
**Output Directory:** `yearly_working_2025-20251010-085610`

## Executive Summary

This report presents nowcasting results for **11 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | RandomForest-070-v02-085655 | RandomForest | 1.2424 | 1.1166 | N/A |
| Cpi | Ridge-073-v01-085627 | Ridge | 0.8863 | 0.7184 | N/A |
| Deposit Rate 12M | StandardizedRidge-085-v01-085725 | StandardizedRidge | 0.9207 | 0.7659 | N/A |
| Deposit Rate 1M | Ridge-074-v02-085701 | Ridge | 1.0721 | 0.7321 | N/A |
| Deposit Rate 3M | StandardizedRidge-085-v01-085707 | StandardizedRidge | 0.9771 | 0.9131 | N/A |
| Deposit Rate 6M | StandardizedRidge-085-v01-085715 | StandardizedRidge | 0.8830 | 0.7866 | N/A |
| Fx | Ridge-074-v02-085647 | Ridge | 191533.0402 | 176889.9321 | N/A |
| Govt Bond Yield 10 Yr | Ridge-074-v02-085734 | Ridge | 0.4223 | 0.3871 | N/A |
| Jisdor Exchange Rate | StandardizedRidge-085-v01-085743 | StandardizedRidge | 591.8307 | 544.7044 | N/A |
| Real Gdp Growth | ElasticNetGrid-029-v01-085635 | ElasticNetGrid | 0.6600 | 0.4265 | N/A |
| Informal Employment | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 38588.4201 | 0.8655 | 10 |
| ARp | 668891.4250 | 3.1353 | 10 |
| BVAR | 47138.8754 | 0.7299 | 10 |
| Bagging | 46695.1235 | 0.7201 | 10 |
| DFM | 29645.9036 | 0.7842 | 10 |
| DFM2 | 668891.4250 | 3.1353 | 10 |
| ElasticNet | 44294.8827 | 0.7609 | 10 |
| ElasticNetGrid | 55971.3820 | 0.6600 | 10 |
| ExtraTrees | 47138.8754 | 0.7299 | 10 |
| GARCH | 3869177388.3626 | 2.8078 | 10 |
| GradientBoosting | 47138.8754 | 0.7299 | 10 |
| Huber | 668891.4250 | 3.1353 | 10 |
| LSTM | 444856.3587 | 1.4410 | 10 |
| Lasso | 43832.7817 | 0.7569 | 10 |
| Linear | 668891.4250 | 3.1353 | 10 |
| Naive | 46341.0416 | 0.5895 | 10 |
| PLS1 | 25134.1505 | 0.7896 | 10 |
| RandomForest | 45571.7312 | 0.7038 | 10 |
| Ridge | 19217.0406 | 0.4223 | 10 |
| SeasonalNaive | 46341.0416 | 0.5895 | 10 |
| StandardizedLinear | 668891.4250 | 3.1353 | 10 |
| StandardizedRidge | 25561.6921 | 0.6267 | 10 |
| StochasticGB | 46052.5048 | 0.7123 | 10 |
| Tree | 47138.8754 | 0.7299 | 10 |
| XGBoost | 29505.1894 | 0.6849 | 10 |

## 1. Bi7Drr

### Top 5 Models (Diverse Selection)

**1. RandomForest Model 🏆**
- ID: `RandomForest-070-v02-085655`
- RMSE (H=1): 1.2424
- MAE (H=1): 1.1166
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. ElasticNet Model**
- ID: `ElasticNet-026-v02-085653`
- RMSE (H=1): 1.2424
- MAE (H=1): 1.1166
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. XGBoost Model**
- ID: `XGBoost-097-v01-085656`
- RMSE (H=1): 1.2424
- MAE (H=1): 1.1166
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. Tree Model**
- ID: `Tree-093-v01-085656`
- RMSE (H=1): 1.2424
- MAE (H=1): 1.1166
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. BVAR Model**
- ID: `BVAR-009-v01-085652`
- RMSE (H=1): 1.2424
- MAE (H=1): 1.1166
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-085651 | 1.2424 | +0.0% |
| ARp | ARp-006-v02-085651 | 4.9546 | +298.8% |
| BVAR | BVAR-009-v01-085652 | 1.2424 | +0.0% |
| Bagging | Bagging-013-v01-085652 | 1.2424 | +0.0% |
| DFM | DFM-018-v02-085652 | 4.9546 | +298.8% |
| DFM2 | DFM2-021-v01-085652 | 4.9546 | +298.8% |
| ElasticNet | ElasticNet-026-v02-085653 | 1.2424 | +0.0% |
| ElasticNetGrid | ElasticNetGrid-029-v01-085653 | 1.2424 | +0.0% |
| ExtraTrees | ExtraTrees-034-v02-085653 | 1.2424 | +0.0% |
| GARCH | GARCH-038-v02-085654 | 4.9546 | +298.8% |
| GradientBoosting | GradientBoosting-042-v02-085654 | 1.2424 | +0.0% |
| Huber | Huber-045-v01-085654 | 4.9546 | +298.8% |
| LSTM | LSTM-050-v02-085654 | 3.9524 | +218.1% |
| Lasso | Lasso-054-v02-085654 | 1.2424 | +0.0% |
| Linear | Linear-057-v01-085654 | 4.9546 | +298.8% |
| Naive | Naive-062-v02-085654 | 1.9210 | +54.6% |
| PLS1 | PLS1-065-v01-085655 | 4.9546 | +298.8% |
| RandomForest | RandomForest-070-v02-085655 | 1.2424 | 0.0% |
| Ridge | Ridge-074-v02-085655 | 1.2424 | +0.0% |
| SeasonalNaive | SeasonalNaive-078-v02-085655 | 1.9210 | +54.6% |
| StandardizedLinear | StandardizedLinear-081-v01-085655 | 4.9546 | +298.8% |
| StandardizedRidge | StandardizedRidge-086-v02-085655 | 1.2424 | +0.0% |
| StochasticGB | StochasticGB-089-v01-085656 | 1.2424 | +0.0% |
| Tree | Tree-093-v01-085656 | 1.2424 | +0.0% |
| XGBoost | XGBoost-097-v01-085656 | 1.2424 | +0.0% |

### Forecast Visualizations

#### 1. RandomForest Model Forecast
![RandomForest Forecast](yearly_working_2025-20251010-085610/visualizations/BI7DRR_randomforest_rank1.png)

#### 2. ElasticNet Model Forecast
![ElasticNet Forecast](yearly_working_2025-20251010-085610/visualizations/BI7DRR_elasticnet_rank2.png)

#### 3. XGBoost Model Forecast
![XGBoost Forecast](yearly_working_2025-20251010-085610/visualizations/BI7DRR_xgboost_rank3.png)

#### All Models Comparison
![Bi7Drr Comparison](yearly_working_2025-20251010-085610/visualizations/BI7DRR_comparison.png)

---

## 2. Cpi

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-073-v01-085627`
- RMSE (H=1): 0.8863
- MAE (H=1): 0.7184
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Lasso Model**
- ID: `Lasso-054-v02-085626`
- RMSE (H=1): 0.9354
- MAE (H=1): 0.8901
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. ElasticNetGrid Model**
- ID: `ElasticNetGrid-030-v02-085625`
- RMSE (H=1): 0.9866
- MAE (H=1): 0.9201
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. ElasticNet Model**
- ID: `ElasticNet-026-v02-085622`
- RMSE (H=1): 1.0693
- MAE (H=1): 0.9426
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. Bagging Model**
- ID: `Bagging-014-v02-085616`
- RMSE (H=1): 1.0958
- MAE (H=1): 1.0177
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-085614 | 2.6292 | +196.6% |
| ARp | ARp-005-v01-085614 | 3.1353 | +253.7% |
| BVAR | BVAR-009-v01-085615 | 1.0967 | +23.7% |
| Bagging | Bagging-014-v02-085616 | 1.0958 | +23.6% |
| DFM | DFM-018-v02-085617 | 1.4485 | +63.4% |
| DFM2 | DFM2-022-v02-085618 | 3.1353 | +253.7% |
| ElasticNet | ElasticNet-026-v02-085622 | 1.0693 | +20.6% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085625 | 0.9866 | +11.3% |
| ExtraTrees | ExtraTrees-034-v02-085625 | 1.0967 | +23.7% |
| GARCH | GARCH-038-v02-085625 | 2.8078 | +216.8% |
| GradientBoosting | GradientBoosting-041-v01-085626 | 1.0967 | +23.7% |
| Huber | Huber-046-v02-085626 | 3.1353 | +253.7% |
| LSTM | LSTM-050-v02-085626 | 1.4410 | +62.6% |
| Lasso | Lasso-054-v02-085626 | 0.9354 | +5.5% |
| Linear | Linear-058-v02-085627 | 3.1353 | +253.7% |
| Naive | Naive-061-v01-085627 | 1.9112 | +115.6% |
| PLS1 | PLS1-066-v02-085627 | 1.3128 | +48.1% |
| RandomForest | RandomForest-069-v01-085627 | 1.1055 | +24.7% |
| Ridge | Ridge-073-v01-085627 | 0.8863 | 0.0% |
| SeasonalNaive | SeasonalNaive-077-v01-085627 | 1.9112 | +115.6% |
| StandardizedLinear | StandardizedLinear-082-v02-085627 | 3.1353 | +253.7% |
| StandardizedRidge | StandardizedRidge-086-v02-085628 | 1.2205 | +37.7% |
| StochasticGB | StochasticGB-089-v01-085628 | 1.1035 | +24.5% |
| Tree | Tree-093-v01-085628 | 1.0967 | +23.7% |
| XGBoost | XGBoost-097-v01-085628 | 1.4191 | +60.1% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/CPI_ridge_rank1.png)

#### 2. Lasso Model Forecast
![Lasso Forecast](yearly_working_2025-20251010-085610/visualizations/CPI_lasso_rank2.png)

#### 3. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](yearly_working_2025-20251010-085610/visualizations/CPI_elasticnetgrid_rank3.png)

#### All Models Comparison
![Cpi Comparison](yearly_working_2025-20251010-085610/visualizations/CPI_comparison.png)

---

## 3. Deposit Rate 12M

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-085-v01-085725`
- RMSE (H=1): 0.9207
- MAE (H=1): 0.7659
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-074-v02-085724`
- RMSE (H=1): 1.0822
- MAE (H=1): 0.6805
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. PLS1 Model**
- ID: `PLS1-065-v01-085723`
- RMSE (H=1): 1.1090
- MAE (H=1): 0.9806
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. XGBoost Model**
- ID: `XGBoost-098-v02-085726`
- RMSE (H=1): 1.6794
- MAE (H=1): 1.4827
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. AR1 Model**
- ID: `AR1-002-v02-085719`
- RMSE (H=1): 1.8619
- MAE (H=1): 1.6585
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-085719 | 1.8619 | +102.2% |
| ARp | ARp-006-v02-085719 | 4.8518 | +426.9% |
| BVAR | BVAR-009-v01-085720 | 1.9205 | +108.6% |
| Bagging | Bagging-013-v01-085720 | 1.8787 | +104.0% |
| DFM | DFM-018-v02-085720 | 1.9666 | +113.6% |
| DFM2 | DFM2-021-v01-085720 | 4.8518 | +426.9% |
| ElasticNet | ElasticNet-025-v01-085720 | 1.9008 | +106.4% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085721 | 1.9686 | +113.8% |
| ExtraTrees | ExtraTrees-033-v01-085722 | 1.9205 | +108.6% |
| GARCH | GARCH-037-v01-085722 | 4.7226 | +412.9% |
| GradientBoosting | GradientBoosting-042-v02-085722 | 1.9205 | +108.6% |
| Huber | Huber-045-v01-085722 | 4.8518 | +426.9% |
| LSTM | LSTM-049-v01-085722 | 7.8932 | +757.3% |
| Lasso | Lasso-053-v01-085722 | 1.9205 | +108.6% |
| Linear | Linear-058-v02-085723 | 4.8518 | +426.9% |
| Naive | Naive-062-v02-085723 | 2.0816 | +126.1% |
| PLS1 | PLS1-065-v01-085723 | 1.1090 | +20.5% |
| RandomForest | RandomForest-069-v01-085724 | 1.8666 | +102.7% |
| Ridge | Ridge-074-v02-085724 | 1.0822 | +17.5% |
| SeasonalNaive | SeasonalNaive-077-v01-085724 | 2.0816 | +126.1% |
| StandardizedLinear | StandardizedLinear-081-v01-085725 | 4.8518 | +426.9% |
| StandardizedRidge | StandardizedRidge-085-v01-085725 | 0.9207 | 0.0% |
| StochasticGB | StochasticGB-089-v01-085725 | 1.8891 | +105.2% |
| Tree | Tree-093-v01-085725 | 1.9205 | +108.6% |
| XGBoost | XGBoost-098-v02-085726 | 1.6794 | +82.4% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 12M_standardizedridge_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 12M_ridge_rank2.png)

#### 3. PLS1 Model Forecast
![PLS1 Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 12M_pls1_rank3.png)

#### All Models Comparison
![Deposit Rate 12M Comparison](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 12M_comparison.png)

---

## 4. Deposit Rate 1M

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-074-v02-085701`
- RMSE (H=1): 1.0721
- MAE (H=1): 0.7321
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. StandardizedRidge Model**
- ID: `StandardizedRidge-085-v01-085701`
- RMSE (H=1): 1.2407
- MAE (H=1): 1.1007
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-002-v02-085658`
- RMSE (H=1): 1.7681
- MAE (H=1): 1.3939
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. XGBoost Model**
- ID: `XGBoost-098-v02-085702`
- RMSE (H=1): 1.8029
- MAE (H=1): 1.6004
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. RandomForest Model**
- ID: `RandomForest-069-v01-085701`
- RMSE (H=1): 2.0988
- MAE (H=1): 1.9978
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-085658 | 1.7681 | +64.9% |
| ARp | ARp-006-v02-085658 | 3.9317 | +266.7% |
| BVAR | BVAR-010-v02-085658 | 2.1877 | +104.1% |
| Bagging | Bagging-014-v02-085658 | 2.1343 | +99.1% |
| DFM | DFM-018-v02-085658 | 2.1815 | +103.5% |
| DFM2 | DFM2-021-v01-085658 | 3.9317 | +266.7% |
| ElasticNet | ElasticNet-025-v01-085658 | 2.1751 | +102.9% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085659 | 2.5128 | +134.4% |
| ExtraTrees | ExtraTrees-033-v01-085659 | 2.1877 | +104.1% |
| GARCH | GARCH-037-v01-085659 | 3.5238 | +228.7% |
| GradientBoosting | GradientBoosting-042-v02-085659 | 2.1877 | +104.1% |
| Huber | Huber-046-v02-085700 | 3.9317 | +266.7% |
| LSTM | LSTM-049-v01-085700 | 4.3100 | +302.0% |
| Lasso | Lasso-053-v01-085700 | 2.2303 | +108.0% |
| Linear | Linear-058-v02-085700 | 3.9317 | +266.7% |
| Naive | Naive-061-v01-085700 | 2.1087 | +96.7% |
| PLS1 | PLS1-065-v01-085700 | 3.5596 | +232.0% |
| RandomForest | RandomForest-069-v01-085701 | 2.0988 | +95.8% |
| Ridge | Ridge-074-v02-085701 | 1.0721 | 0.0% |
| SeasonalNaive | SeasonalNaive-077-v01-085701 | 2.1087 | +96.7% |
| StandardizedLinear | StandardizedLinear-082-v02-085701 | 3.9317 | +266.7% |
| StandardizedRidge | StandardizedRidge-085-v01-085701 | 1.2407 | +15.7% |
| StochasticGB | StochasticGB-089-v01-085701 | 2.1325 | +98.9% |
| Tree | Tree-094-v02-085702 | 2.1877 | +104.1% |
| XGBoost | XGBoost-098-v02-085702 | 1.8029 | +68.2% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 1M_ridge_rank1.png)

#### 2. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 1M_standardizedridge_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 1M_ar1_rank3.png)

#### All Models Comparison
![Deposit Rate 1M Comparison](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 1M_comparison.png)

---

## 5. Deposit Rate 3M

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-085-v01-085707`
- RMSE (H=1): 0.9771
- MAE (H=1): 0.9131
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-074-v02-085707`
- RMSE (H=1): 0.9995
- MAE (H=1): 0.5365
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-001-v01-085704`
- RMSE (H=1): 1.7787
- MAE (H=1): 1.4683
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. XGBoost Model**
- ID: `XGBoost-097-v01-085708`
- RMSE (H=1): 1.9465
- MAE (H=1): 1.5654
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. RandomForest Model**
- ID: `RandomForest-069-v01-085707`
- RMSE (H=1): 1.9791
- MAE (H=1): 1.7827
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-085704 | 1.7787 | +82.0% |
| ARp | ARp-005-v01-085704 | 4.3211 | +342.2% |
| BVAR | BVAR-009-v01-085704 | 2.0603 | +110.8% |
| Bagging | Bagging-013-v01-085704 | 2.0083 | +105.5% |
| DFM | DFM-018-v02-085704 | 2.1704 | +122.1% |
| DFM2 | DFM2-022-v02-085704 | 4.3211 | +342.2% |
| ElasticNet | ElasticNet-025-v01-085705 | 2.0325 | +108.0% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085705 | 2.3010 | +135.5% |
| ExtraTrees | ExtraTrees-034-v02-085705 | 2.0603 | +110.8% |
| GARCH | GARCH-037-v01-085706 | 3.9778 | +307.1% |
| GradientBoosting | GradientBoosting-041-v01-085706 | 2.0603 | +110.8% |
| Huber | Huber-046-v02-085706 | 4.3211 | +342.2% |
| LSTM | LSTM-050-v02-085706 | 4.6171 | +372.5% |
| Lasso | Lasso-053-v01-085706 | 2.0678 | +111.6% |
| Linear | Linear-058-v02-085706 | 4.3211 | +342.2% |
| Naive | Naive-061-v01-085706 | 2.2502 | +130.3% |
| PLS1 | PLS1-065-v01-085707 | 2.8062 | +187.2% |
| RandomForest | RandomForest-069-v01-085707 | 1.9791 | +102.5% |
| Ridge | Ridge-074-v02-085707 | 0.9995 | +2.3% |
| SeasonalNaive | SeasonalNaive-077-v01-085707 | 2.2502 | +130.3% |
| StandardizedLinear | StandardizedLinear-082-v02-085707 | 4.3211 | +342.2% |
| StandardizedRidge | StandardizedRidge-085-v01-085707 | 0.9771 | 0.0% |
| StochasticGB | StochasticGB-089-v01-085707 | 2.0105 | +105.8% |
| Tree | Tree-093-v01-085708 | 2.0603 | +110.8% |
| XGBoost | XGBoost-097-v01-085708 | 1.9465 | +99.2% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 3M_standardizedridge_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 3M_ridge_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 3M_ar1_rank3.png)

#### All Models Comparison
![Deposit Rate 3M Comparison](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 3M_comparison.png)

---

## 6. Deposit Rate 6M

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-085-v01-085715`
- RMSE (H=1): 0.8830
- MAE (H=1): 0.7866
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-074-v02-085714`
- RMSE (H=1): 1.0316
- MAE (H=1): 0.5851
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-002-v02-085710`
- RMSE (H=1): 1.9738
- MAE (H=1): 1.6330
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. PLS1 Model**
- ID: `PLS1-065-v01-085714`
- RMSE (H=1): 2.0650
- MAE (H=1): 1.9441
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. RandomForest Model**
- ID: `RandomForest-069-v01-085714`
- RMSE (H=1): 2.1125
- MAE (H=1): 1.9444
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-085710 | 1.9738 | +123.5% |
| ARp | ARp-006-v02-085710 | 4.5724 | +417.9% |
| BVAR | BVAR-009-v01-085710 | 2.2002 | +149.2% |
| Bagging | Bagging-013-v01-085710 | 2.1393 | +142.3% |
| DFM | DFM-018-v02-085711 | 2.2647 | +156.5% |
| DFM2 | DFM2-021-v01-085711 | 4.5724 | +417.9% |
| ElasticNet | ElasticNet-025-v01-085711 | 2.1730 | +146.1% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085712 | 2.4334 | +175.6% |
| ExtraTrees | ExtraTrees-033-v01-085712 | 2.2002 | +149.2% |
| GARCH | GARCH-037-v01-085712 | 4.2214 | +378.1% |
| GradientBoosting | GradientBoosting-042-v02-085713 | 2.2002 | +149.2% |
| Huber | Huber-045-v01-085713 | 4.5724 | +417.9% |
| LSTM | LSTM-049-v01-085713 | 6.8699 | +678.1% |
| Lasso | Lasso-053-v01-085713 | 2.2002 | +149.2% |
| Linear | Linear-058-v02-085713 | 4.5724 | +417.9% |
| Naive | Naive-062-v02-085714 | 2.3162 | +162.3% |
| PLS1 | PLS1-065-v01-085714 | 2.0650 | +133.9% |
| RandomForest | RandomForest-069-v01-085714 | 2.1125 | +139.2% |
| Ridge | Ridge-074-v02-085714 | 1.0316 | +16.8% |
| SeasonalNaive | SeasonalNaive-077-v01-085714 | 2.3162 | +162.3% |
| StandardizedLinear | StandardizedLinear-081-v01-085715 | 4.5724 | +417.9% |
| StandardizedRidge | StandardizedRidge-085-v01-085715 | 0.8830 | 0.0% |
| StochasticGB | StochasticGB-089-v01-085715 | 2.1474 | +143.2% |
| Tree | Tree-093-v01-085715 | 2.2002 | +149.2% |
| XGBoost | XGBoost-098-v02-085716 | 2.6186 | +196.6% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 6M_standardizedridge_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 6M_ridge_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 6M_ar1_rank3.png)

#### All Models Comparison
![Deposit Rate 6M Comparison](yearly_working_2025-20251010-085610/visualizations/Deposit Rate 6M_comparison.png)

---

## 7. Fx

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-074-v02-085647`
- RMSE (H=1): 191533.0402
- MAE (H=1): 176889.9321
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. PLS1 Model**
- ID: `PLS1-065-v01-085647`
- RMSE (H=1): 249594.9596
- MAE (H=1): 180415.9920
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. StandardizedRidge Model**
- ID: `StandardizedRidge-085-v01-085647`
- RMSE (H=1): 254991.4911
- MAE (H=1): 223967.8000
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. XGBoost Model**
- ID: `XGBoost-098-v02-085648`
- RMSE (H=1): 294296.1496
- MAE (H=1): 244170.5875
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. DFM Model**
- ID: `DFM-017-v01-085640`
- RMSE (H=1): 295541.3700
- MAE (H=1): 232785.6341
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-085640 | 385064.5613 | +101.0% |
| ARp | ARp-005-v01-085640 | 6673803.2807 | +3384.4% |
| BVAR | BVAR-009-v01-085640 | 470444.6911 | +145.6% |
| Bagging | Bagging-013-v01-085640 | 466018.8848 | +143.3% |
| DFM | DFM-017-v01-085640 | 295541.3700 | +54.3% |
| DFM2 | DFM2-022-v02-085641 | 6673803.2807 | +3384.4% |
| ElasticNet | ElasticNet-025-v01-085642 | 441964.9794 | +130.8% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085645 | 558642.9871 | +191.7% |
| ExtraTrees | ExtraTrees-033-v01-085645 | 470444.6911 | +145.6% |
| GARCH | GARCH-038-v02-085646 | 38691736282.8700 | +20200976.7% |
| GradientBoosting | GradientBoosting-041-v01-085646 | 470444.6911 | +145.6% |
| Huber | Huber-046-v02-085646 | 6673803.2807 | +3384.4% |
| LSTM | LSTM-050-v02-085646 | 4440533.6380 | +2218.4% |
| Lasso | Lasso-053-v01-085646 | 437356.0881 | +128.3% |
| Linear | Linear-057-v01-085646 | 6673803.2807 | +3384.4% |
| Naive | Naive-061-v01-085646 | 462691.9857 | +141.6% |
| PLS1 | PLS1-065-v01-085647 | 249594.9596 | +30.3% |
| RandomForest | RandomForest-070-v02-085647 | 454796.1532 | +137.5% |
| Ridge | Ridge-074-v02-085647 | 191533.0402 | 0.0% |
| SeasonalNaive | SeasonalNaive-078-v02-085647 | 462691.9857 | +141.6% |
| StandardizedLinear | StandardizedLinear-082-v02-085647 | 6673803.2807 | +3384.4% |
| StandardizedRidge | StandardizedRidge-085-v01-085647 | 254991.4911 | +33.1% |
| StochasticGB | StochasticGB-090-v02-085647 | 459595.7141 | +140.0% |
| Tree | Tree-094-v02-085648 | 470444.6911 | +145.6% |
| XGBoost | XGBoost-098-v02-085648 | 294296.1496 | +53.7% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/FX_ridge_rank1.png)

#### 2. PLS1 Model Forecast
![PLS1 Forecast](yearly_working_2025-20251010-085610/visualizations/FX_pls1_rank2.png)

#### 3. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_working_2025-20251010-085610/visualizations/FX_standardizedridge_rank3.png)

#### All Models Comparison
![Fx Comparison](yearly_working_2025-20251010-085610/visualizations/FX_comparison.png)

---

## 8. Govt Bond Yield 10 Yr

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-074-v02-085734`
- RMSE (H=1): 0.4223
- MAE (H=1): 0.3871
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-078-v02-085734`
- RMSE (H=1): 0.5895
- MAE (H=1): 0.4126
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. Naive Model**
- ID: `Naive-061-v01-085734`
- RMSE (H=1): 0.5895
- MAE (H=1): 0.4126
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-085-v01-085735`
- RMSE (H=1): 0.6267
- MAE (H=1): 0.5927
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. XGBoost Model**
- ID: `XGBoost-098-v02-085736`
- RMSE (H=1): 0.6849
- MAE (H=1): 0.6171
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-085729 | 0.8655 | +104.9% |
| ARp | ARp-006-v02-085729 | 6.8051 | +1511.3% |
| BVAR | BVAR-010-v02-085730 | 0.7299 | +72.8% |
| Bagging | Bagging-014-v02-085730 | 0.7201 | +70.5% |
| DFM | DFM-018-v02-085731 | 0.7842 | +85.7% |
| DFM2 | DFM2-022-v02-085732 | 6.8051 | +1511.3% |
| ElasticNet | ElasticNet-025-v01-085732 | 0.7609 | +80.2% |
| ElasticNetGrid | ElasticNetGrid-030-v02-085733 | 0.8756 | +107.3% |
| ExtraTrees | ExtraTrees-034-v02-085733 | 0.7299 | +72.8% |
| GARCH | GARCH-038-v02-085733 | 6.7354 | +1494.8% |
| GradientBoosting | GradientBoosting-041-v01-085733 | 0.7299 | +72.8% |
| Huber | Huber-046-v02-085733 | 6.8051 | +1511.3% |
| LSTM | LSTM-050-v02-085733 | 10.4569 | +2375.9% |
| Lasso | Lasso-053-v01-085734 | 0.7569 | +79.2% |
| Linear | Linear-057-v01-085734 | 6.8051 | +1511.3% |
| Naive | Naive-061-v01-085734 | 0.5895 | +39.6% |
| PLS1 | PLS1-065-v01-085734 | 0.7896 | +87.0% |
| RandomForest | RandomForest-070-v02-085734 | 0.7038 | +66.6% |
| Ridge | Ridge-074-v02-085734 | 0.4223 | 0.0% |
| SeasonalNaive | SeasonalNaive-078-v02-085734 | 0.5895 | +39.6% |
| StandardizedLinear | StandardizedLinear-082-v02-085735 | 6.8051 | +1511.3% |
| StandardizedRidge | StandardizedRidge-085-v01-085735 | 0.6267 | +48.4% |
| StochasticGB | StochasticGB-090-v02-085735 | 0.7123 | +68.7% |
| Tree | Tree-094-v02-085735 | 0.7299 | +72.8% |
| XGBoost | XGBoost-098-v02-085736 | 0.6849 | +62.2% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/Govt Bond Yield 10 Yr_ridge_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](yearly_working_2025-20251010-085610/visualizations/Govt Bond Yield 10 Yr_seasonalnaive_rank2.png)

#### 3. Naive Model Forecast
![Naive Forecast](yearly_working_2025-20251010-085610/visualizations/Govt Bond Yield 10 Yr_naive_rank3.png)

#### All Models Comparison
![Govt Bond Yield 10 Yr Comparison](yearly_working_2025-20251010-085610/visualizations/Govt Bond Yield 10 Yr_comparison.png)

---

## 9. Jisdor Exchange Rate

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-085-v01-085743`
- RMSE (H=1): 591.8307
- MAE (H=1): 544.7044
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. AR1 Model**
- ID: `AR1-001-v01-085739`
- RMSE (H=1): 611.5212
- MAE (H=1): 499.6825
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. Ridge Model**
- ID: `Ridge-073-v01-085743`
- RMSE (H=1): 623.0967
- MAE (H=1): 515.8274
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. SeasonalNaive Model**
- ID: `SeasonalNaive-078-v02-085743`
- RMSE (H=1): 701.4815
- MAE (H=1): 590.5742
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. Naive Model**
- ID: `Naive-062-v02-085742`
- RMSE (H=1): 701.4815
- MAE (H=1): 590.5742
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-085739 | 611.5212 | +3.3% |
| ARp | ARp-005-v01-085739 | 15073.5767 | +2446.9% |
| BVAR | BVAR-010-v02-085739 | 930.4852 | +57.2% |
| Bagging | Bagging-014-v02-085739 | 918.8489 | +55.3% |
| DFM | DFM-018-v02-085739 | 884.9114 | +49.5% |
| DFM2 | DFM2-022-v02-085739 | 15073.5767 | +2446.9% |
| ElasticNet | ElasticNet-025-v01-085740 | 968.9160 | +63.7% |
| ElasticNetGrid | ElasticNetGrid-029-v01-085740 | 1057.8527 | +78.7% |
| ExtraTrees | ExtraTrees-033-v01-085741 | 930.4852 | +57.2% |
| GARCH | GARCH-037-v01-085741 | 37557.7671 | +6246.0% |
| GradientBoosting | GradientBoosting-042-v02-085741 | 930.4852 | +57.2% |
| Huber | Huber-045-v01-085741 | 15073.5767 | +2446.9% |
| LSTM | LSTM-049-v01-085742 | 7766.1544 | +1212.2% |
| Lasso | Lasso-053-v01-085742 | 955.9150 | +61.5% |
| Linear | Linear-057-v01-085742 | 15073.5767 | +2446.9% |
| Naive | Naive-062-v02-085742 | 701.4815 | +18.5% |
| PLS1 | PLS1-066-v02-085742 | 1360.7186 | +129.9% |
| RandomForest | RandomForest-070-v02-085743 | 907.5081 | +53.3% |
| Ridge | Ridge-073-v01-085743 | 623.0967 | +5.3% |
| SeasonalNaive | SeasonalNaive-078-v02-085743 | 701.4815 | +18.5% |
| StandardizedLinear | StandardizedLinear-081-v01-085743 | 15073.5767 | +2446.9% |
| StandardizedRidge | StandardizedRidge-085-v01-085743 | 591.8307 | 0.0% |
| StochasticGB | StochasticGB-090-v02-085743 | 915.6848 | +54.7% |
| Tree | Tree-094-v02-085744 | 930.4852 | +57.2% |
| XGBoost | XGBoost-098-v02-085744 | 740.7590 | +25.2% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](yearly_working_2025-20251010-085610/visualizations/JISDOR Exchange Rate_standardizedridge_rank1.png)

#### 2. AR1 Model Forecast
![AR1 Forecast](yearly_working_2025-20251010-085610/visualizations/JISDOR Exchange Rate_ar1_rank2.png)

#### 3. Ridge Model Forecast
![Ridge Forecast](yearly_working_2025-20251010-085610/visualizations/JISDOR Exchange Rate_ridge_rank3.png)

#### All Models Comparison
![Jisdor Exchange Rate Comparison](yearly_working_2025-20251010-085610/visualizations/JISDOR Exchange Rate_comparison.png)

---

## 10. Real Gdp Growth

### Top 5 Models (Diverse Selection)

**1. ElasticNetGrid Model 🏆**
- ID: `ElasticNetGrid-029-v01-085635`
- RMSE (H=1): 0.6600
- MAE (H=1): 0.4265
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. BVAR Model**
- ID: `BVAR-010-v02-085635`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. GradientBoosting Model**
- ID: `GradientBoosting-042-v02-085635`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. Tree Model**
- ID: `Tree-094-v02-085637`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. ExtraTrees Model**
- ID: `ExtraTrees-033-v01-085635`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-085634 | 195.9986 | +29597.9% |
| ARp | ARp-006-v02-085634 | 4.8200 | +630.3% |
| BVAR | BVAR-010-v02-085635 | 2.1405 | +224.3% |
| Bagging | Bagging-014-v02-085635 | 2.2823 | +245.8% |
| DFM | DFM-018-v02-085635 | 16.9839 | +2473.4% |
| DFM2 | DFM2-021-v01-085635 | 4.8200 | +630.3% |
| ElasticNet | ElasticNet-026-v02-085635 | 3.5773 | +442.0% |
| ElasticNetGrid | ElasticNetGrid-029-v01-085635 | 0.6600 | 0.0% |
| ExtraTrees | ExtraTrees-033-v01-085635 | 2.1405 | +224.3% |
| GARCH | GARCH-037-v01-085635 | 12.0452 | +1725.1% |
| GradientBoosting | GradientBoosting-042-v02-085635 | 2.1405 | +224.3% |
| Huber | Huber-045-v01-085636 | 4.8200 | +630.3% |
| LSTM | LSTM-050-v02-085636 | 224.2540 | +33879.2% |
| Lasso | Lasso-053-v01-085636 | 4.4604 | +575.8% |
| Linear | Linear-057-v01-085636 | 4.8200 | +630.3% |
| Naive | Naive-062-v02-085636 | 3.7703 | +471.3% |
| PLS1 | PLS1-066-v02-085636 | 369.2297 | +55846.1% |
| RandomForest | RandomForest-070-v02-085636 | 2.5422 | +285.2% |
| Ridge | Ridge-074-v02-085636 | 7.5325 | +1041.3% |
| SeasonalNaive | SeasonalNaive-078-v02-085636 | 3.7703 | +471.3% |
| StandardizedLinear | StandardizedLinear-081-v01-085636 | 4.8200 | +630.3% |
| StandardizedRidge | StandardizedRidge-086-v02-085637 | 26.4878 | +3913.5% |
| StochasticGB | StochasticGB-090-v02-085637 | 2.4115 | +265.4% |
| Tree | Tree-094-v02-085637 | 2.1405 | +224.3% |
| XGBoost | XGBoost-098-v02-085637 | 3.5912 | +444.1% |

### Forecast Visualizations

#### 1. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](yearly_working_2025-20251010-085610/visualizations/Real GDP Growth_elasticnetgrid_rank1.png)

#### 2. BVAR Model Forecast
![BVAR Forecast](yearly_working_2025-20251010-085610/visualizations/Real GDP Growth_bvar_rank2.png)

#### 3. GradientBoosting Model Forecast
![GradientBoosting Forecast](yearly_working_2025-20251010-085610/visualizations/Real GDP Growth_gradientboosting_rank3.png)

#### All Models Comparison
![Real Gdp Growth Comparison](yearly_working_2025-20251010-085610/visualizations/Real GDP Growth_comparison.png)

---

## 11. Informal Employment

*No valid results found for Informal Employment*

## Key Insights

1. **AR1 models** performed best on 0/11 targets, suggesting strong autoregressive patterns
2. **Ensemble methods** appeared in top 3 for 2/11 targets
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
