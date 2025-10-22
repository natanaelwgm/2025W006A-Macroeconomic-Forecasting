# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-09 13:32:28
**Output Directory:** `enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053`

## Executive Summary

This report presents nowcasting results for **6 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Bi7Drr | Naive-917-v17-124753 | Naive | 0.6564 | 0.4417 | 0.6383 |
| Cpi | Naive-958-v58-122713 | Naive | 1.2331 | 0.9181 | 0.1744 |
| Deposit Rate 1M | Naive-915-v15-125833 | Naive | 0.6185 | 0.4869 | 0.3835 |
| Deposit Rate 3M | SeasonalNaive-1158-v18-131239 | SeasonalNaive | 0.6834 | 0.5654 | 0.4939 |
| Deposit Rate 6M | Naive-959-v59-132632 | Naive | 0.6975 | 0.6188 | 0.4975 |
| Real Gdp Growth | Ridge-1136-v56-123835 | Ridge | 3.2092 | 2.1336 | 0.0524 |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 1.8482 | 0.8393 | 6 |
| ARp | 2.7333 | 1.0644 | 6 |
| BVAR | 2.1102 | 0.7603 | 6 |
| Bagging | 2.0481 | 1.1376 | 6 |
| DFM | 1.8037 | 1.1674 | 6 |
| DFM2 | 2.0957 | 1.0633 | 6 |
| ElasticNet | 1.8580 | 1.0318 | 6 |
| ElasticNetGrid | 1.9569 | 1.1708 | 6 |
| ExtraTrees | 2.1071 | 1.1515 | 6 |
| GARCH | 4.1835 | 2.7994 | 6 |
| GradientBoosting | 1.9520 | 1.1515 | 6 |
| Huber | 2.7333 | 1.0644 | 6 |
| LSTM | 2.2162 | 1.3550 | 6 |
| Lasso | 1.8868 | 1.0315 | 6 |
| Linear | 2.7333 | 1.0644 | 6 |
| Naive | 1.2527 | 0.6185 | 6 |
| PLS1 | 2.3467 | 0.9728 | 6 |
| RandomForest | 2.0657 | 1.1460 | 6 |
| Ridge | 1.8227 | 0.9656 | 6 |
| SeasonalNaive | 1.2527 | 0.6185 | 6 |
| StandardizedLinear | 2.7333 | 1.0644 | 6 |
| StandardizedRidge | 3.0875 | 0.7718 | 6 |
| StochasticGB | 2.1792 | 1.1505 | 6 |
| Tree | 2.0449 | 1.1515 | 6 |
| XGBoost | 1.9329 | 1.3190 | 6 |

## 1. Bi7Drr

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-917-v17-124753`
- RMSE (H=1): 0.6564
- MAE (H=1): 0.4417
- R² (H=1): 0.6383
- MAPE: 9.1%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-1158-v18-124911`
- RMSE (H=1): 0.6564
- MAE (H=1): 0.4417
- R² (H=1): 0.6383
- MAPE: 9.1%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-015-v15-124228`
- RMSE (H=1): 0.8393
- MAE (H=1): 0.7696
- R² (H=1): 0.4086
- MAPE: 18.2%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: None

**4. Lasso Model**
- ID: `Lasso-782-v02-124657`
- RMSE (H=1): 1.0315
- MAE (H=1): 0.9872
- R² (H=1): 0.1066
- MAPE: 21.6%
- Features: 7 variables
- Normalization: None
- Feature Pack: None

**5. ElasticNet Model**
- ID: `ElasticNet-420-v60-124429`
- RMSE (H=1): 1.0318
- MAE (H=1): 0.9914
- R² (H=1): 0.1060
- MAPE: 21.6%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-015-v15-124228 | 0.8393 | +27.9% |
| ARp | ARp-098-v38-124251 | 4.9309 | +651.3% |
| BVAR | BVAR-159-v39-124308 | 2.2391 | +241.1% |
| Bagging | Bagging-181-v01-124314 | 1.1376 | +73.3% |
| DFM | DFM-282-v42-124347 | 1.1674 | +77.9% |
| DFM2 | DFM2-334-v34-124403 | 1.8649 | +184.1% |
| ElasticNet | ElasticNet-420-v60-124429 | 1.0318 | +57.2% |
| ElasticNetGrid | ElasticNetGrid-477-v57-124508 | 1.1708 | +78.4% |
| ExtraTrees | ExtraTrees-533-v53-124530 | 1.1515 | +75.4% |
| GARCH | GARCH-573-v33-124542 | 4.4471 | +577.5% |
| GradientBoosting | GradientBoosting-602-v02-124550 | 1.1515 | +75.4% |
| Huber | Huber-661-v01-124607 | 4.9309 | +651.3% |
| LSTM | LSTM-741-v21-124635 | 3.4816 | +430.4% |
| Lasso | Lasso-782-v02-124657 | 1.0315 | +57.2% |
| Linear | Linear-877-v37-124739 | 4.9309 | +651.3% |
| Naive | Naive-917-v17-124753 | 0.6564 | 0.0% |
| PLS1 | PLS1-998-v38-124818 | 2.6641 | +305.9% |
| RandomForest | RandomForest-1077-v57-124843 | 1.1460 | +74.6% |
| Ridge | Ridge-1119-v39-124857 | 2.1217 | +223.3% |
| SeasonalNaive | SeasonalNaive-1158-v18-124911 | 0.6564 | 0.0% |
| StandardizedLinear | StandardizedLinear-1203-v03-124924 | 4.9309 | +651.3% |
| StandardizedRidge | StandardizedRidge-1299-v39-124954 | 2.2470 | +242.3% |
| StochasticGB | StochasticGB-1354-v34-125014 | 1.1505 | +75.3% |
| Tree | Tree-1393-v13-125025 | 1.1515 | +75.4% |
| XGBoost | XGBoost-1498-v58-125138 | 1.3868 | +111.3% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/BI7DRR_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/BI7DRR_seasonalnaive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/BI7DRR_ar1_rank3.png)

#### All Models Comparison
![Bi7Drr Comparison](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/BI7DRR_comparison.png)

---

## 2. Cpi

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-958-v58-122713`
- RMSE (H=1): 1.2331
- MAE (H=1): 0.9181
- R² (H=1): 0.1744
- MAPE: 43.5%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-1174-v34-122827`
- RMSE (H=1): 1.2331
- MAE (H=1): 0.9181
- R² (H=1): 0.1744
- MAPE: 43.5%
- Features: 14 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: ta_basic

**3. AR1 Model**
- ID: `AR1-054-v54-122108`
- RMSE (H=1): 1.3163
- MAE (H=1): 1.1685
- R² (H=1): 0.0592
- MAPE: 68.0%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: ta_advanced

**4. XGBoost Model**
- ID: `XGBoost-1500-v60-123144`
- RMSE (H=1): 1.3190
- MAE (H=1): 1.1105
- R² (H=1): 0.0555
- MAPE: 63.7%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

**5. LSTM Model**
- ID: `LSTM-721-v01-122516`
- RMSE (H=1): 1.3550
- MAE (H=1): 1.0850
- R² (H=1): 0.0032
- MAPE: 58.3%
- Features: 7 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-054-v54-122108 | 1.3163 | +6.8% |
| ARp | ARp-077-v17-122113 | 2.4308 | +97.1% |
| BVAR | BVAR-157-v37-122133 | 2.0012 | +62.3% |
| Bagging | Bagging-181-v01-122138 | 1.4304 | +16.0% |
| DFM | DFM-241-v01-122157 | 1.4907 | +20.9% |
| DFM2 | DFM2-338-v38-122225 | 1.5797 | +28.1% |
| ElasticNet | ElasticNet-403-v43-122248 | 1.5086 | +22.3% |
| ElasticNetGrid | ElasticNetGrid-453-v33-122329 | 1.7193 | +39.4% |
| ExtraTrees | ExtraTrees-493-v13-122402 | 1.4521 | +17.8% |
| GARCH | GARCH-559-v19-122425 | 2.7994 | +127.0% |
| GradientBoosting | GradientBoosting-602-v02-122435 | 1.4048 | +13.9% |
| Huber | Huber-681-v21-122500 | 2.4308 | +97.1% |
| LSTM | LSTM-721-v01-122516 | 1.3550 | +9.9% |
| Lasso | Lasso-784-v04-122626 | 1.4705 | +19.3% |
| Linear | Linear-857-v17-122645 | 2.4308 | +97.1% |
| Naive | Naive-958-v58-122713 | 1.2331 | 0.0% |
| PLS1 | PLS1-1002-v42-122732 | 1.8217 | +47.7% |
| RandomForest | RandomForest-1077-v57-122801 | 1.4366 | +16.5% |
| Ridge | Ridge-1097-v17-122807 | 1.7967 | +45.7% |
| SeasonalNaive | SeasonalNaive-1174-v34-122827 | 1.2331 | 0.0% |
| StandardizedLinear | StandardizedLinear-1217-v17-122838 | 2.4308 | +97.1% |
| StandardizedRidge | StandardizedRidge-1297-v37-122857 | 1.9467 | +57.9% |
| StochasticGB | StochasticGB-1358-v38-122912 | 1.4956 | +21.3% |
| Tree | Tree-1422-v42-122928 | 1.4895 | +20.8% |
| XGBoost | XGBoost-1500-v60-123144 | 1.3190 | +7.0% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/CPI_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/CPI_seasonalnaive_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/CPI_ar1_rank3.png)

#### All Models Comparison
![Cpi Comparison](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/CPI_comparison.png)

---

## 3. Deposit Rate 1M

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-915-v15-125833`
- RMSE (H=1): 0.6185
- MAE (H=1): 0.4869
- R² (H=1): 0.3835
- MAPE: 12.3%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: None

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-1196-v56-130005`
- RMSE (H=1): 0.6185
- MAE (H=1): 0.4869
- R² (H=1): 0.3835
- MAPE: 12.3%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: ta_advanced

**3. BVAR Model**
- ID: `BVAR-121-v01-125230`
- RMSE (H=1): 1.0601
- MAE (H=1): 0.8420
- R² (H=1): -0.8108
- MAPE: 23.2%
- Features: 7 variables
- Normalization: None
- Feature Pack: None

**4. ARp Model**
- ID: `ARp-101-v41-125224`
- RMSE (H=1): 1.2324
- MAE (H=1): 1.0708
- R² (H=1): -1.4473
- MAPE: 26.9%
- Features: 7 variables
- Normalization: None
- Feature Pack: ta_advanced

**5. Huber Model**
- ID: `Huber-717-v57-125633`
- RMSE (H=1): 1.2324
- MAE (H=1): 1.0708
- R² (H=1): -1.4473
- MAPE: 26.9%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-053-v53-125201 | 1.6149 | +161.1% |
| ARp | ARp-101-v41-125224 | 1.2324 | +99.2% |
| BVAR | BVAR-121-v01-125230 | 1.0601 | +71.4% |
| Bagging | Bagging-236-v56-125309 | 2.1225 | +243.2% |
| DFM | DFM-242-v02-125311 | 1.9051 | +208.0% |
| DFM2 | DFM2-317-v17-125338 | 2.1126 | +241.6% |
| ElasticNet | ElasticNet-376-v16-125357 | 1.8815 | +204.2% |
| ElasticNetGrid | ElasticNetGrid-480-v60-125502 | 2.0769 | +235.8% |
| ExtraTrees | ExtraTrees-494-v14-125508 | 2.2005 | +255.8% |
| GARCH | GARCH-543-v03-125529 | 4.0611 | +556.6% |
| GradientBoosting | GradientBoosting-643-v43-125603 | 1.9949 | +222.5% |
| Huber | Huber-717-v57-125633 | 1.2324 | +99.2% |
| LSTM | LSTM-757-v37-125716 | 1.8477 | +198.7% |
| Lasso | Lasso-840-v60-125811 | 1.9649 | +217.7% |
| Linear | Linear-861-v21-125817 | 1.2324 | +99.2% |
| Naive | Naive-915-v15-125833 | 0.6185 | 0.0% |
| PLS1 | PLS1-979-v19-125853 | 2.4925 | +303.0% |
| RandomForest | RandomForest-1022-v02-125907 | 2.1741 | +251.5% |
| Ridge | Ridge-1102-v22-125934 | 1.6742 | +170.7% |
| SeasonalNaive | SeasonalNaive-1196-v56-130005 | 0.6185 | 0.0% |
| StandardizedLinear | StandardizedLinear-1237-v37-130017 | 1.2324 | +99.2% |
| StandardizedRidge | StandardizedRidge-1282-v22-130032 | 1.5811 | +155.6% |
| StochasticGB | StochasticGB-1334-v14-130049 | 2.3221 | +275.4% |
| Tree | Tree-1402-v22-130111 | 2.0326 | +228.6% |
| XGBoost | XGBoost-1444-v04-130143 | 1.9965 | +222.8% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 1M_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 1M_seasonalnaive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 1M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 1M Comparison](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 1M_comparison.png)

---

## 4. Deposit Rate 3M

### Top 5 Models (Diverse Selection)

**1. SeasonalNaive Model 🏆**
- ID: `SeasonalNaive-1158-v18-131239`
- RMSE (H=1): 0.6834
- MAE (H=1): 0.5654
- R² (H=1): 0.4939
- MAPE: 13.2%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**2. Naive Model**
- ID: `Naive-954-v54-131049`
- RMSE (H=1): 0.6834
- MAE (H=1): 0.5654
- R² (H=1): 0.4939
- MAPE: 13.2%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: ta_advanced

**3. BVAR Model**
- ID: `BVAR-178-v58-130438`
- RMSE (H=1): 0.9270
- MAE (H=1): 0.7150
- R² (H=1): 0.0689
- MAPE: 19.2%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-1318-v58-131401`
- RMSE (H=1): 1.0322
- MAE (H=1): 0.7756
- R² (H=1): -0.1545
- MAPE: 21.5%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

**5. StandardizedLinear Model**
- ID: `StandardizedLinear-1241-v41-131323`
- RMSE (H=1): 1.0644
- MAE (H=1): 0.8329
- R² (H=1): -0.2277
- MAPE: 22.0%
- Features: 7 variables
- Normalization: None
- Feature Pack: ta_advanced

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-060-v60-130358 | 1.4177 | +107.4% |
| ARp | ARp-073-v13-130404 | 1.0644 | +55.7% |
| BVAR | BVAR-178-v58-130438 | 0.9270 | +35.6% |
| Bagging | Bagging-240-v60-130502 | 1.9890 | +191.0% |
| DFM | DFM-254-v14-130506 | 1.4595 | +113.6% |
| DFM2 | DFM2-302-v02-130521 | 1.5476 | +126.5% |
| ElasticNet | ElasticNet-401-v41-130557 | 1.5901 | +132.7% |
| ElasticNetGrid | ElasticNetGrid-479-v59-130656 | 1.5306 | +124.0% |
| ExtraTrees | ExtraTrees-494-v14-130703 | 2.0899 | +205.8% |
| GARCH | GARCH-600-v60-130744 | 4.5047 | +559.1% |
| GradientBoosting | GradientBoosting-659-v59-130809 | 1.8097 | +164.8% |
| Huber | Huber-693-v33-130822 | 1.0644 | +55.7% |
| LSTM | LSTM-734-v14-130847 | 1.4524 | +112.5% |
| Lasso | Lasso-796-v16-130952 | 1.7136 | +150.7% |
| Linear | Linear-893-v53-131027 | 1.0644 | +55.7% |
| Naive | Naive-954-v54-131049 | 0.6834 | 0.0% |
| PLS1 | PLS1-978-v18-131059 | 1.4039 | +105.4% |
| RandomForest | RandomForest-1064-v44-131149 | 2.0227 | +196.0% |
| Ridge | Ridge-1118-v38-131219 | 1.1685 | +71.0% |
| SeasonalNaive | SeasonalNaive-1158-v18-131239 | 0.6834 | 0.0% |
| StandardizedLinear | StandardizedLinear-1241-v41-131323 | 1.0644 | +55.7% |
| StandardizedRidge | StandardizedRidge-1318-v58-131401 | 1.0322 | +51.0% |
| StochasticGB | StochasticGB-1338-v18-131410 | 2.2205 | +224.9% |
| Tree | Tree-1402-v22-131438 | 1.9809 | +189.8% |
| XGBoost | XGBoost-1497-v57-131713 | 1.7981 | +163.1% |

### Forecast Visualizations

#### 1. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 3M_seasonalnaive_rank1.png)

#### 2. Naive Model Forecast
![Naive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 3M_naive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 3M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 3M Comparison](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 3M_comparison.png)

---

## 5. Deposit Rate 6M

### Top 5 Models (Diverse Selection)

**1. Naive Model 🏆**
- ID: `Naive-959-v59-132632`
- RMSE (H=1): 0.6975
- MAE (H=1): 0.6188
- R² (H=1): 0.4975
- MAPE: 13.4%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: ta_advanced

**2. SeasonalNaive Model**
- ID: `SeasonalNaive-1142-v02-132758`
- RMSE (H=1): 0.6975
- MAE (H=1): 0.6188
- R² (H=1): 0.4975
- MAPE: 13.4%
- Features: 7 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-138-v18-131844`
- RMSE (H=1): 0.7603
- MAE (H=1): 0.6350
- R² (H=1): 0.4029
- MAPE: 15.6%
- Features: 7 variables
- Normalization: {'method': 'robust', 'window': 4}
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-1302-v42-132901`
- RMSE (H=1): 0.7718
- MAE (H=1): 0.6345
- R² (H=1): 0.3847
- MAPE: 15.8%
- Features: 7 variables
- Normalization: None
- Feature Pack: ta_advanced

**5. Ridge Model**
- ID: `Ridge-1094-v14-132734`
- RMSE (H=1): 0.9656
- MAE (H=1): 0.8330
- R² (H=1): 0.0369
- MAPE: 20.3%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-058-v58-131807 | 1.3564 | +94.5% |
| ARp | ARp-113-v53-131833 | 1.8634 | +167.1% |
| BVAR | BVAR-138-v18-131844 | 0.7603 | +9.0% |
| Bagging | Bagging-239-v59-131927 | 2.0537 | +194.4% |
| DFM | DFM-258-v18-131936 | 1.2355 | +77.1% |
| DFM2 | DFM2-338-v38-132018 | 1.0633 | +52.4% |
| ElasticNet | ElasticNet-417-v57-132056 | 1.6753 | +140.2% |
| ElasticNetGrid | ElasticNetGrid-480-v60-132200 | 1.6915 | +142.5% |
| ExtraTrees | ExtraTrees-498-v18-132209 | 2.1837 | +213.1% |
| GARCH | GARCH-582-v42-132250 | 4.7730 | +584.3% |
| GradientBoosting | GradientBoosting-620-v20-132308 | 1.9137 | +174.4% |
| Huber | Huber-661-v01-132330 | 1.8634 | +167.1% |
| LSTM | LSTM-738-v18-132427 | 1.7923 | +156.9% |
| Lasso | Lasso-836-v56-132541 | 1.6230 | +132.7% |
| Linear | Linear-841-v01-132544 | 1.8634 | +167.1% |
| Naive | Naive-959-v59-132632 | 0.6975 | 0.0% |
| PLS1 | PLS1-982-v22-132642 | 0.9728 | +39.5% |
| RandomForest | RandomForest-1076-v56-132727 | 2.0802 | +198.2% |
| Ridge | Ridge-1094-v14-132734 | 0.9656 | +38.4% |
| SeasonalNaive | SeasonalNaive-1142-v02-132758 | 0.6975 | 0.0% |
| StandardizedLinear | StandardizedLinear-1213-v13-132826 | 1.8634 | +167.1% |
| StandardizedRidge | StandardizedRidge-1302-v42-132901 | 0.7718 | +10.6% |
| StochasticGB | StochasticGB-1358-v38-132923 | 2.3344 | +234.7% |
| Tree | Tree-1418-v38-132952 | 2.0623 | +195.7% |
| XGBoost | XGBoost-1443-v03-133012 | 1.8160 | +160.3% |

### Forecast Visualizations

#### 1. Naive Model Forecast
![Naive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 6M_naive_rank1.png)

#### 2. SeasonalNaive Model Forecast
![SeasonalNaive Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 6M_seasonalnaive_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 6M_bvar_rank3.png)

#### All Models Comparison
![Deposit Rate 6M Comparison](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Deposit Rate 6M_comparison.png)

---

## 6. Real Gdp Growth

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-1136-v56-123835`
- RMSE (H=1): 3.2092
- MAE (H=1): 2.1336
- R² (H=1): 0.0524
- MAPE: 61.2%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: ta_advanced

**2. XGBoost Model**
- ID: `XGBoost-1461-v21-124103`
- RMSE (H=1): 3.2813
- MAE (H=1): 1.9310
- R² (H=1): 0.0094
- MAPE: 67.6%
- Features: 10 variables
- Normalization: None
- Feature Pack: ta_basic

**3. LSTM Model**
- ID: `LSTM-721-v01-123550`
- RMSE (H=1): 3.3684
- MAE (H=1): 2.0408
- R² (H=1): -0.0440
- MAPE: 84.0%
- Features: 7 variables
- Normalization: None
- Feature Pack: None

**4. GradientBoosting Model**
- ID: `GradientBoosting-641-v41-123522`
- RMSE (H=1): 3.4375
- MAE (H=1): 1.8196
- R² (H=1): -0.0872
- MAPE: 79.4%
- Features: 7 variables
- Normalization: None
- Feature Pack: ta_advanced

**5. ElasticNet Model**
- ID: `ElasticNet-375-v15-123331`
- RMSE (H=1): 3.4605
- MAE (H=1): 1.9598
- R² (H=1): -0.1018
- MAPE: 81.4%
- Features: 7 variables
- Normalization: {'method': 'minmax', 'window': 4}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-056-v56-123200 | 4.5448 | +41.6% |
| ARp | ARp-102-v42-123211 | 4.8779 | +52.0% |
| BVAR | BVAR-162-v42-123228 | 5.6738 | +76.8% |
| Bagging | Bagging-237-v57-123252 | 3.5554 | +10.8% |
| DFM | DFM-255-v15-123258 | 3.5643 | +11.1% |
| DFM2 | DFM2-353-v53-123324 | 4.4060 | +37.3% |
| ElasticNet | ElasticNet-375-v15-123331 | 3.4605 | +7.8% |
| ElasticNetGrid | ElasticNetGrid-473-v53-123421 | 3.5525 | +10.7% |
| ExtraTrees | ExtraTrees-497-v17-123438 | 3.5649 | +11.1% |
| GARCH | GARCH-557-v17-123458 | 4.5154 | +40.7% |
| GradientBoosting | GradientBoosting-641-v41-123522 | 3.4375 | +7.1% |
| Huber | Huber-694-v34-123540 | 4.8779 | +52.0% |
| LSTM | LSTM-721-v01-123550 | 3.3684 | +5.0% |
| Lasso | Lasso-798-v18-123700 | 3.5174 | +9.6% |
| Linear | Linear-894-v54-123728 | 4.8779 | +52.0% |
| Naive | Naive-959-v59-123747 | 3.6273 | +13.0% |
| PLS1 | PLS1-1002-v42-123758 | 4.7253 | +47.2% |
| RandomForest | RandomForest-1073-v53-123818 | 3.5347 | +10.1% |
| Ridge | Ridge-1136-v56-123835 | 3.2092 | 0.0% |
| SeasonalNaive | SeasonalNaive-1194-v54-123851 | 3.6273 | +13.0% |
| StandardizedLinear | StandardizedLinear-1222-v22-123900 | 4.8779 | +52.0% |
| StandardizedRidge | StandardizedRidge-1261-v01-123911 | 10.9460 | +241.1% |
| StochasticGB | StochasticGB-1323-v03-123927 | 3.5522 | +10.7% |
| Tree | Tree-1437-v57-124001 | 3.5529 | +10.7% |
| XGBoost | XGBoost-1461-v21-124103 | 3.2813 | +2.2% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Real GDP Growth_ridge_rank1.png)

#### 2. XGBoost Model Forecast
![XGBoost Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Real GDP Growth_xgboost_rank2.png)

#### 3. LSTM Model Forecast
![LSTM Forecast](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Real GDP Growth_lstm_rank3.png)

#### All Models Comparison
![Real Gdp Growth Comparison](enhanced_comprehensive_all_models_indonesia_macro_quarterly-20251009-122053/visualizations/Real GDP Growth_comparison.png)

---

## Key Insights

1. **AR1 models** performed best on 0/6 targets, suggesting strong autoregressive patterns
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
