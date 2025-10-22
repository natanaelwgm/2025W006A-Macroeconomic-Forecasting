# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-10 11:11:13
**Output Directory:** `semesterly_advanced_robust_2025-20251010-094533`

## Executive Summary

This report presents nowcasting results for **11 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | *No valid models* | - | N/A | N/A | N/A |
| Cpi | StandardizedRidge-1299-v39-095249 | StandardizedRidge | 1.0193 | 0.8281 | 0.3746 |
| Deposit Rate 12M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 1M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 3M | *No valid models* | - | N/A | N/A | N/A |
| Deposit Rate 6M | *No valid models* | - | N/A | N/A | N/A |
| Fx | *No valid models* | - | N/A | N/A | N/A |
| Govt Bond Yield 10 Yr | Naive-918-v18-104711 | Naive | 0.5109 | 0.4353 | -4.3199 |
| Jisdor Exchange Rate | SeasonalNaive-1143-v03-105632 | SeasonalNaive | 637.4002 | 476.0515 | N/A |
| Real Gdp Growth | Ridge-1115-v35-100043 | Ridge | 2.1232 | 1.5168 | 0.1960 |
| Unemployment | PLS1-1000-v40-110708 | PLS1 | 0.1120 | 0.0936 | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 252.7522 | 0.8387 | 5 |
| ARp | 3073.0776 | 3.0049 | 5 |
| BVAR | 239.3163 | 0.8720 | 5 |
| Bagging | 244.0008 | 0.5000 | 5 |
| DFM | 219.5380 | 0.3796 | 5 |
| DFM2 | 323.8008 | 1.2702 | 5 |
| ElasticNet | 246.9857 | 0.9803 | 5 |
| ElasticNetGrid | 282.8243 | 0.2961 | 5 |
| ExtraTrees | 244.9533 | 0.5064 | 5 |
| GARCH | 37723.7772 | 2.8663 | 5 |
| GradientBoosting | 244.9533 | 0.5064 | 5 |
| Huber | 3073.0776 | 3.0049 | 5 |
| LSTM | 2701.9283 | 0.2908 | 5 |
| Lasso | 255.9023 | 0.8327 | 5 |
| Linear | 3073.0776 | 3.0049 | 5 |
| Naive | 128.7798 | 0.4794 | 5 |
| PLS1 | 247.6741 | 0.1120 | 5 |
| RandomForest | 244.1150 | 0.4851 | 5 |
| Ridge | 1356.4951 | 0.9101 | 5 |
| SeasonalNaive | 128.7798 | 0.4794 | 5 |
| StandardizedLinear | 3073.0776 | 3.0049 | 5 |
| StandardizedRidge | 223.4122 | 1.0193 | 5 |
| StochasticGB | 243.9627 | 0.4995 | 5 |
| Tree | 244.9533 | 0.5064 | 5 |
| XGBoost | 219.7590 | 0.2055 | 5 |

## 1. Bi7Drr

*No valid results found for Bi7Drr*

## 2. Cpi

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-1299-v39-095249`
- RMSE (H=1): 1.0193
- MAE (H=1): 0.8281
- R² (H=1): 0.3746
- MAPE: 33.9%
- Features: 35 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: technical

**2. PLS1 Model**
- ID: `PLS1-979-v19-095202`
- RMSE (H=1): 1.1929
- MAE (H=1): 0.9437
- R² (H=1): 0.1435
- MAPE: 36.7%
- Features: 35 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**3. Ridge Model**
- ID: `Ridge-1138-v58-095224`
- RMSE (H=1): 1.1967
- MAE (H=1): 0.9504
- R² (H=1): 0.1380
- MAPE: 35.0%
- Features: 25 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: statistical

**4. ElasticNetGrid Model**
- ID: `ElasticNetGrid-443-v23-094900`
- RMSE (H=1): 1.2393
- MAE (H=1): 1.0374
- R² (H=1): 0.0756
- MAPE: 45.3%
- Features: 35 variables
- Normalization: None
- Feature Pack: technical

**5. LSTM Model**
- ID: `LSTM-742-v22-094959`
- RMSE (H=1): 1.2514
- MAE (H=1): 1.0729
- R² (H=1): 0.0574
- MAPE: 53.0%
- Features: 25 variables
- Normalization: None
- Feature Pack: technical

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-021-v21-094559 | 1.5393 | +51.0% |
| ARp | ARp-063-v03-094615 | 3.0049 | +194.8% |
| BVAR | BVAR-153-v33-094652 | 1.8636 | +82.8% |
| Bagging | Bagging-194-v14-094655 | 1.3005 | +27.6% |
| DFM | DFM-273-v33-094712 | 1.2979 | +27.3% |
| DFM2 | DFM2-303-v03-094718 | 1.2702 | +24.6% |
| ElasticNet | ElasticNet-419-v59-094844 | 1.3170 | +29.2% |
| ElasticNetGrid | ElasticNetGrid-443-v23-094900 | 1.2393 | +21.6% |
| ExtraTrees | ExtraTrees-515-v35-094932 | 1.2975 | +27.3% |
| GARCH | GARCH-554-v14-094935 | 2.8663 | +181.2% |
| GradientBoosting | GradientBoosting-621-v21-094939 | 1.2975 | +27.3% |
| Huber | Huber-674-v14-094947 | 3.0049 | +194.8% |
| LSTM | LSTM-742-v22-094959 | 1.2514 | +22.8% |
| Lasso | Lasso-819-v39-095121 | 1.2921 | +26.8% |
| Linear | Linear-857-v17-095144 | 3.0049 | +194.8% |
| Naive | Naive-935-v35-095158 | 1.8179 | +78.4% |
| PLS1 | PLS1-979-v19-095202 | 1.1929 | +17.0% |
| RandomForest | RandomForest-1062-v42-095212 | 1.3007 | +27.6% |
| Ridge | Ridge-1138-v58-095224 | 1.1967 | +17.4% |
| SeasonalNaive | SeasonalNaive-1195-v55-095232 | 1.8179 | +78.4% |
| StandardizedLinear | StandardizedLinear-1242-v42-095239 | 3.0049 | +194.8% |
| StandardizedRidge | StandardizedRidge-1299-v39-095249 | 1.0193 | 0.0% |
| StochasticGB | StochasticGB-1323-v03-095253 | 1.2999 | +27.5% |
| Tree | Tree-1415-v35-095305 | 1.2975 | +27.3% |
| XGBoost | XGBoost-1462-v22-095334 | 1.2705 | +24.6% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/CPI_standardizedridge_rank1.png)

#### 2. PLS1 Model Forecast
![PLS1 Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/CPI_pls1_rank2.png)

#### 3. Ridge Model Forecast
![Ridge Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/CPI_ridge_rank3.png)

#### All Models Comparison
![Cpi Comparison](semesterly_advanced_robust_2025-20251010-094533/visualizations/CPI_comparison.png)

---

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

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-918-v18-104711`
- RMSE (H=1): 0.5109
- MAE (H=1): 0.4353
- R² (H=1): -4.3199
- MAPE: 6.4%
- Features: 25 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-1157-v17-104820`
- RMSE (H=1): 0.5109
- MAE (H=1): 0.4353
- R² (H=1): -4.3199
- MAPE: 6.4%
- Features: 15 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**3. ElasticNetGrid Model**
- ID: `ElasticNetGrid-463-v43-104500`
- RMSE (H=1): 0.7261
- MAE (H=1): 0.6801
- R² (H=1): -9.7463
- MAPE: 10.1%
- Features: 35 variables
- Normalization: None
- Feature Pack: statistical

**4. DFM Model**
- ID: `DFM-278-v38-104356`
- RMSE (H=1): 0.7612
- MAE (H=1): 0.7215
- R² (H=1): -10.8105
- MAPE: 10.7%
- Features: 25 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: technical

**5. StochasticGB Model**
- ID: `StochasticGB-1323-v03-104907`
- RMSE (H=1): 0.8206
- MAE (H=1): 0.7902
- R² (H=1): -12.7282
- MAPE: 11.7%
- Features: 35 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-017-v17-104250 | 1.1662 | +128.3% |
| ARp | ARp-103-v43-104310 | 6.8255 | +1236.1% |
| BVAR | BVAR-174-v54-104328 | 0.8720 | +70.7% |
| Bagging | Bagging-198-v18-104335 | 0.8336 | +63.2% |
| DFM | DFM-278-v38-104356 | 0.7612 | +49.0% |
| DFM2 | DFM2-313-v13-104405 | 1.8575 | +263.6% |
| ElasticNet | ElasticNet-419-v59-104433 | 1.0444 | +104.4% |
| ElasticNetGrid | ElasticNetGrid-463-v43-104500 | 0.7261 | +42.1% |
| ExtraTrees | ExtraTrees-497-v17-104513 | 0.8309 | +62.6% |
| GARCH | GARCH-561-v21-104531 | 6.5794 | +1187.9% |
| GradientBoosting | GradientBoosting-641-v41-104551 | 0.8309 | +62.6% |
| Huber | Huber-714-v54-104610 | 6.8255 | +1236.1% |
| LSTM | LSTM-761-v41-104623 | 12.2535 | +2298.6% |
| Lasso | Lasso-795-v15-104635 | 0.8327 | +63.0% |
| Linear | Linear-855-v15-104652 | 6.8255 | +1236.1% |
| Naive | Naive-918-v18-104711 | 0.5109 | 0.0% |
| PLS1 | PLS1-977-v17-104730 | 2.0138 | +294.2% |
| RandomForest | RandomForest-1037-v17-104747 | 0.8253 | +61.6% |
| Ridge | Ridge-1117-v37-104808 | 1.3267 | +159.7% |
| SeasonalNaive | SeasonalNaive-1157-v17-104820 | 0.5109 | 0.0% |
| StandardizedLinear | StandardizedLinear-1219-v19-104838 | 6.8255 | +1236.1% |
| StandardizedRidge | StandardizedRidge-1293-v33-104858 | 1.8593 | +263.9% |
| StochasticGB | StochasticGB-1323-v03-104907 | 0.8206 | +60.6% |
| Tree | Tree-1434-v54-104938 | 0.8309 | +62.6% |
| XGBoost | XGBoost-1499-v59-105011 | 1.1679 | +128.6% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Govt Bond Yield 10 Yr_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Govt Bond Yield 10 Yr_seasonalnaive_rank2.png)

#### 3. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Govt Bond Yield 10 Yr_elasticnetgrid_rank3.png)

#### All Models Comparison
![Govt Bond Yield 10 Yr Comparison](semesterly_advanced_robust_2025-20251010-094533/visualizations/Govt Bond Yield 10 Yr_comparison.png)

---

## 9. Jisdor Exchange Rate

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-1143-v03-105632`
- RMSE (H=1): 637.4002
- MAE (H=1): 476.0515
- Features: 35 variables
- Normalization: None
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-941-v41-105529`
- RMSE (H=1): 637.4002
- MAE (H=1): 476.0515
- Features: 15 variables
- Normalization: None
- Feature Pack: statistical

**3. DFM Model**
- ID: `DFM-274-v34-105132`
- RMSE (H=1): 1091.1570
- MAE (H=1): 843.3932
- Features: 25 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: technical

**4. XGBoost Model**
- ID: `XGBoost-1457-v17-105849`
- RMSE (H=1): 1092.3275
- MAE (H=1): 867.6511
- Features: 15 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**5. StandardizedRidge Model**
- ID: `StandardizedRidge-1274-v14-105712`
- RMSE (H=1): 1096.2265
- MAE (H=1): 1045.3121
- Features: 25 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-035-v35-105027 | 1212.6881 | +90.3% |
| ARp | ARp-074-v14-105036 | 15345.7545 | +2307.6% |
| BVAR | BVAR-177-v57-105106 | 1188.7192 | +86.5% |
| Bagging | Bagging-239-v59-105124 | 1214.9944 | +90.6% |
| DFM | DFM-274-v34-105132 | 1091.1570 | +71.2% |
| DFM2 | DFM2-342-v42-105151 | 1595.3878 | +150.3% |
| ElasticNet | ElasticNet-383-v23-105205 | 1229.3410 | +92.9% |
| ElasticNetGrid | ElasticNetGrid-462-v42-105253 | 1409.2957 | +121.1% |
| ExtraTrees | ExtraTrees-519-v39-105318 | 1219.7553 | +91.4% |
| GARCH | GARCH-557-v17-105331 | 188600.5075 | +29489.0% |
| GradientBoosting | GradientBoosting-618-v18-105350 | 1219.7553 | +91.4% |
| Huber | Huber-694-v34-105412 | 15345.7545 | +2307.6% |
| LSTM | LSTM-735-v15-105425 | 13439.1730 | +2008.4% |
| Lasso | Lasso-815-v35-105449 | 1273.8268 | +99.8% |
| Linear | Linear-857-v17-105501 | 15345.7545 | +2307.6% |
| Naive | Naive-941-v41-105529 | 637.4002 | 0.0% |
| PLS1 | PLS1-982-v22-105540 | 1192.4228 | +87.1% |
| RandomForest | RandomForest-1079-v59-105609 | 1215.5916 | +90.7% |
| Ridge | Ridge-1135-v55-105630 | 6776.9190 | +963.2% |
| SeasonalNaive | SeasonalNaive-1143-v03-105632 | 637.4002 | 0.0% |
| StandardizedLinear | StandardizedLinear-1215-v15-105656 | 15345.7545 | +2307.6% |
| StandardizedRidge | StandardizedRidge-1274-v14-105712 | 1096.2265 | +72.0% |
| StochasticGB | StochasticGB-1357-v37-105749 | 1214.8179 | +90.6% |
| Tree | Tree-1382-v02-105759 | 1219.7553 | +91.4% |
| XGBoost | XGBoost-1457-v17-105849 | 1092.3275 | +71.4% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/JISDOR Exchange Rate_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/JISDOR Exchange Rate_naive_rank2.png)

#### 3. DFM Model Forecast
![DFM Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/JISDOR Exchange Rate_dfm_rank3.png)

#### All Models Comparison
![Jisdor Exchange Rate Comparison](semesterly_advanced_robust_2025-20251010-094533/visualizations/JISDOR Exchange Rate_comparison.png)

---

## 10. Real Gdp Growth

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-1115-v35-100043`
- RMSE (H=1): 2.1232
- MAE (H=1): 1.5168
- R² (H=1): 0.1960
- MAPE: 35.4%
- Features: 35 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: technical

**2. ElasticNet Model**
- ID: `ElasticNet-403-v43-095548`
- RMSE (H=1): 2.2457
- MAE (H=1): 1.7710
- R² (H=1): 0.1005
- MAPE: 40.4%
- Features: 35 variables
- Normalization: None
- Feature Pack: statistical

**3. RandomForest Model**
- ID: `RandomForest-1034-v14-100013`
- RMSE (H=1): 2.3722
- MAE (H=1): 1.6282
- R² (H=1): -0.0036
- MAPE: 43.4%
- Features: 25 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: None

**4. Bagging Model**
- ID: `Bagging-199-v19-095511`
- RMSE (H=1): 2.3756
- MAE (H=1): 1.6576
- R² (H=1): -0.0065
- MAPE: 43.9%
- Features: 35 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**5. StochasticGB Model**
- ID: `StochasticGB-1354-v34-100150`
- RMSE (H=1): 2.3758
- MAE (H=1): 1.6589
- R² (H=1): -0.0067
- MAPE: 43.9%
- Features: 25 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: technical

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-053-v53-095424 | 47.5290 | +2138.5% |
| ARp | ARp-117-v57-095453 | 4.6838 | +120.6% |
| BVAR | BVAR-123-v03-095455 | 4.2194 | +98.7% |
| Bagging | Bagging-199-v19-095511 | 2.3756 | +11.9% |
| DFM | DFM-255-v15-095520 | 4.0942 | +92.8% |
| DFM2 | DFM2-334-v34-095534 | 18.3567 | +764.6% |
| ElasticNet | ElasticNet-403-v43-095548 | 2.2457 | +5.8% |
| ElasticNetGrid | ElasticNetGrid-463-v43-095707 | 2.5641 | +20.8% |
| ExtraTrees | ExtraTrees-535-v55-095808 | 2.3763 | +11.9% |
| GARCH | GARCH-573-v33-095815 | 4.5143 | +112.6% |
| GradientBoosting | GradientBoosting-637-v37-095826 | 2.3763 | +11.9% |
| Huber | Huber-682-v22-095836 | 4.6838 | +120.6% |
| LSTM | LSTM-721-v01-095846 | 56.6726 | +2569.2% |
| Lasso | Lasso-803-v23-095903 | 2.6711 | +25.8% |
| Linear | Linear-883-v43-095927 | 4.6838 | +120.6% |
| Naive | Naive-957-v57-095957 | 3.6907 | +73.8% |
| PLS1 | PLS1-979-v19-100002 | 42.6292 | +1907.8% |
| RandomForest | RandomForest-1034-v14-100013 | 2.3722 | +11.7% |
| Ridge | Ridge-1115-v35-100043 | 2.1232 | 0.0% |
| SeasonalNaive | SeasonalNaive-1154-v14-100052 | 3.6907 | +73.8% |
| StandardizedLinear | StandardizedLinear-1215-v15-100117 | 4.6838 | +120.6% |
| StandardizedRidge | StandardizedRidge-1263-v03-100128 | 16.7788 | +690.3% |
| StochasticGB | StochasticGB-1354-v34-100150 | 2.3758 | +11.9% |
| Tree | Tree-1398-v18-100157 | 2.3763 | +11.9% |
| XGBoost | XGBoost-1443-v03-100208 | 3.8234 | +80.1% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Real GDP Growth_ridge_rank1.png)

#### 2. ElasticNet Model Forecast
![ElasticNet Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Real GDP Growth_elasticnet_rank2.png)

#### 3. RandomForest Model Forecast
![RandomForest Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Real GDP Growth_randomforest_rank3.png)

#### All Models Comparison
![Real Gdp Growth Comparison](semesterly_advanced_robust_2025-20251010-094533/visualizations/Real GDP Growth_comparison.png)

---

## 11. Unemployment

### Top 5 Models (Diverse Selection)

**1. PLS1 Model 🏆**
- ID: `PLS1-1000-v40-110708`
- RMSE (H=1): 0.1120
- MAE (H=1): 0.0936
- Features: 43 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: technical

**2. XGBoost Model**
- ID: `XGBoost-1460-v20-111031`
- RMSE (H=1): 0.2055
- MAE (H=1): 0.2050
- Features: 43 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**3. LSTM Model**
- ID: `LSTM-744-v24-110528`
- RMSE (H=1): 0.2908
- MAE (H=1): 0.2727
- Features: 43 variables
- Normalization: None
- Feature Pack: technical

**4. ElasticNetGrid Model**
- ID: `ElasticNetGrid-480-v60-110331`
- RMSE (H=1): 0.2961
- MAE (H=1): 0.2215
- Features: 43 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: statistical

**5. DFM Model**
- ID: `DFM-276-v36-110142`
- RMSE (H=1): 0.3796
- MAE (H=1): 0.3576
- Features: 43 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: technical

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-056-v56-110013 | 0.8387 | +649.1% |
| ARp | ARp-100-v40-110028 | 5.1191 | +4472.6% |
| BVAR | BVAR-163-v43-110050 | 0.9072 | +710.4% |
| Bagging | Bagging-184-v04-110100 | 0.5000 | +346.6% |
| DFM | DFM-276-v36-110142 | 0.3796 | +239.0% |
| DFM2 | DFM2-340-v40-110203 | 2.1315 | +1804.0% |
| ElasticNet | ElasticNet-375-v15-110215 | 0.9803 | +775.7% |
| ElasticNetGrid | ElasticNetGrid-480-v60-110331 | 0.2961 | +164.5% |
| ExtraTrees | ExtraTrees-500-v20-110338 | 0.5064 | +352.3% |
| GARCH | GARCH-564-v24-110401 | 4.4185 | +3846.7% |
| GradientBoosting | GradientBoosting-656-v56-110447 | 0.5064 | +352.3% |
| Huber | Huber-720-v60-110514 | 5.1191 | +4472.6% |
| LSTM | LSTM-744-v24-110528 | 0.2908 | +159.8% |
| Lasso | Lasso-815-v35-110558 | 0.8887 | +693.8% |
| Linear | Linear-876-v36-110620 | 5.1191 | +4472.6% |
| Naive | Naive-960-v60-110653 | 0.4794 | +328.2% |
| PLS1 | PLS1-1000-v40-110708 | 0.1120 | 0.0% |
| RandomForest | RandomForest-1040-v20-110723 | 0.4851 | +333.3% |
| Ridge | Ridge-1103-v23-110750 | 0.9101 | +712.9% |
| SeasonalNaive | SeasonalNaive-1184-v44-110818 | 0.4794 | +328.2% |
| StandardizedLinear | StandardizedLinear-1224-v24-110834 | 5.1191 | +4472.6% |
| StandardizedRidge | StandardizedRidge-1297-v37-110904 | 1.1770 | +951.3% |
| StochasticGB | StochasticGB-1360-v40-110930 | 0.4995 | +346.2% |
| Tree | Tree-1420-v40-111000 | 0.5064 | +352.3% |
| XGBoost | XGBoost-1460-v20-111031 | 0.2055 | +83.6% |

### Forecast Visualizations

#### 1. PLS1 Model Forecast
![PLS1 Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Unemployment_pls1_rank1.png)

#### 2. XGBoost Model Forecast
![XGBoost Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Unemployment_xgboost_rank2.png)

#### 3. LSTM Model Forecast
![LSTM Forecast](semesterly_advanced_robust_2025-20251010-094533/visualizations/Unemployment_lstm_rank3.png)

#### All Models Comparison
![Unemployment Comparison](semesterly_advanced_robust_2025-20251010-094533/visualizations/Unemployment_comparison.png)

---

## Key Insights

1. **AR1 models** performed best on 0/11 targets, suggesting strong autoregressive patterns
2. **Ensemble methods** appeared in top 3 for 1/11 targets
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
