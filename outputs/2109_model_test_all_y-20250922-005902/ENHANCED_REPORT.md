# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-09-22 01:05:21
**Output Directory:** `2109_model_test_all_y-20250922-005902`

## Executive Summary

This report presents nowcasting results for **8 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| CPI Year-over-Year | DFM2-044-v12-005903 | DFM2 | 0.6013 | 0.5062 | N/A |
| 12-Month Deposit Rate | ElasticNetGrid-070-v06-010430 | ElasticNetGrid | 0.2063 | 0.1282 | N/A |
| 1-Month Deposit Rate | ElasticNetGrid-072-v08-010145 | ElasticNetGrid | 0.1975 | 0.1624 | N/A |
| 3-Month Deposit Rate | StandardizedRidge-133-v05-010313 | StandardizedRidge | 0.1663 | 0.1238 | N/A |
| 6-Month Deposit Rate | StandardizedRidge-142-v14-010410 | StandardizedRidge | 0.1499 | 0.1282 | N/A |
| GDP Year-over-Year | AR1-004-v04-005957 | AR1 | 2.2174 | 0.9495 | N/A |
| Policy Rate (7DRR) | AR1-016-v16-010055 | AR1 | 0.3129 | 0.2625 | N/A |
| USD/IDR Exchange Rate | *No valid models* | - | N/A | N/A | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 0.6206 | 0.2606 | 7 |
| DFM | 1.0922 | 0.3000 | 7 |
| DFM2 | 0.6472 | 0.2279 | 7 |
| ElasticNet | 0.7204 | 0.2337 | 7 |
| ElasticNetGrid | 0.6497 | 0.1695 | 7 |
| Lasso | 0.7119 | 0.2376 | 7 |
| RandomForest | 1.7891 | 0.9330 | 7 |
| Ridge | 0.6570 | 0.1516 | 7 |
| StandardizedRidge | 0.6406 | 0.1499 | 7 |

## 1. CPI Year-over-Year

### Top 5 Models (Diverse Selection)

**1. DFM2 Model 🏆**
- ID: `DFM2-044-v12-005903`
- RMSE (H=1): 0.6013
- MAE (H=1): 0.5062
- RMSE (H=3): 1.0647
- RMSE (H=6): 1.5228
- Degradation: H3=+77.1%, H6=+153.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-122-v10-005956`
- RMSE (H=1): 0.6401
- MAE (H=1): 0.5462
- RMSE (H=3): 1.2042
- RMSE (H=6): 1.8836
- Degradation: H3=+88.1%, H6=+194.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**3. ElasticNet Model**
- ID: `ElasticNet-057-v09-005905`
- RMSE (H=1): 0.6426
- MAE (H=1): 0.5446
- RMSE (H=3): 1.1344
- RMSE (H=6): 1.6314
- Degradation: H3=+76.5%, H6=+153.9%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-142-v14-005956`
- RMSE (H=1): 0.6437
- MAE (H=1): 0.5480
- RMSE (H=3): 1.2141
- RMSE (H=6): 1.9114
- Degradation: H3=+88.6%, H6=+196.9%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. Lasso Model**
- ID: `Lasso-085-v05-005950`
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
| AR1 | AR1-012-v12-005902 | 0.6510 | +8.3% |
| DFM | DFM-026-v10-005903 | 1.7394 | +189.3% |
| DFM2 | DFM2-044-v12-005903 | 0.6013 | 0.0% |
| ElasticNet | ElasticNet-057-v09-005905 | 0.6426 | +6.9% |
| ElasticNetGrid | ElasticNetGrid-068-v04-005917 | 0.8452 | +40.6% |
| Lasso | Lasso-085-v05-005950 | 0.6484 | +7.8% |
| RandomForest | RandomForest-111-v15-005955 | 1.4117 | +134.8% |
| Ridge | Ridge-122-v10-005956 | 0.6401 | +6.5% |
| StandardizedRidge | StandardizedRidge-142-v14-005956 | 0.6437 | +7.1% |

### Forecast Visualizations

#### 1. DFM2 Model Forecast
![DFM2 Forecast](2109_model_test_all_y-20250922-005902/visualizations/cpi_yoy_dfm2_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](2109_model_test_all_y-20250922-005902/visualizations/cpi_yoy_ridge_rank2.png)

#### 3. ElasticNet Model Forecast
![ElasticNet Forecast](2109_model_test_all_y-20250922-005902/visualizations/cpi_yoy_elasticnet_rank3.png)

#### All Models Comparison
![CPI Year-over-Year Comparison](2109_model_test_all_y-20250922-005902/visualizations/cpi_yoy_comparison.png)

---

## 2. 12-Month Deposit Rate

### Top 5 Models (Diverse Selection)

**1. ElasticNetGrid Model 🏆**
- ID: `ElasticNetGrid-070-v06-010430`
- RMSE (H=1): 0.2063
- MAE (H=1): 0.1282
- RMSE (H=3): 0.3314
- RMSE (H=6): 0.4434
- Degradation: H3=+60.6%, H6=+114.9%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**2. ElasticNet Model**
- ID: `ElasticNet-053-v05-010413`
- RMSE (H=1): 0.2337
- MAE (H=1): 0.1805
- RMSE (H=3): 0.3351
- RMSE (H=6): 0.5072
- Degradation: H3=+43.4%, H6=+117.0%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**3. Lasso Model**
- ID: `Lasso-090-v10-010458`
- RMSE (H=1): 0.2376
- MAE (H=1): 0.1869
- RMSE (H=3): 0.3424
- RMSE (H=6): 0.5263
- Degradation: H3=+44.2%, H6=+121.5%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**4. DFM Model**
- ID: `DFM-025-v09-010411`
- RMSE (H=1): 0.3020
- MAE (H=1): 0.2623
- RMSE (H=3): 0.3863
- RMSE (H=6): 0.5835
- Degradation: H3=+27.9%, H6=+93.2%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. DFM2 Model**
- ID: `DFM2-042-v10-010412`
- RMSE (H=1): 0.3275
- MAE (H=1): 0.2380
- RMSE (H=3): 0.4537
- RMSE (H=6): 0.5053
- Degradation: H3=+38.5%, H6=+54.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-012-v12-010410 | 0.3352 | +62.5% |
| DFM | DFM-025-v09-010411 | 0.3020 | +46.4% |
| DFM2 | DFM2-042-v10-010412 | 0.3275 | +58.8% |
| ElasticNet | ElasticNet-053-v05-010413 | 0.2337 | +13.3% |
| ElasticNetGrid | ElasticNetGrid-070-v06-010430 | 0.2063 | 0.0% |
| Lasso | Lasso-090-v10-010458 | 0.2376 | +15.2% |
| RandomForest | RandomForest-110-v14-010502 | 1.3694 | +563.8% |
| Ridge | Ridge-117-v05-010503 | 0.3350 | +62.4% |
| StandardizedRidge | StandardizedRidge-133-v05-010504 | 0.3308 | +60.4% |

### Forecast Visualizations

#### 1. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_12m_elasticnetgrid_rank1.png)

#### 2. ElasticNet Model Forecast
![ElasticNet Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_12m_elasticnet_rank2.png)

#### 3. Lasso Model Forecast
![Lasso Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_12m_lasso_rank3.png)

#### All Models Comparison
![12-Month Deposit Rate Comparison](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_12m_comparison.png)

---

## 3. 1-Month Deposit Rate

### Top 5 Models (Diverse Selection)

**1. ElasticNetGrid Model 🏆**
- ID: `ElasticNetGrid-072-v08-010145`
- RMSE (H=1): 0.1975
- MAE (H=1): 0.1624
- RMSE (H=3): 0.4031
- RMSE (H=6): 0.8445
- Degradation: H3=+104.1%, H6=+327.7%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**2. AR1 Model**
- ID: `AR1-001-v01-010120`
- RMSE (H=1): 0.2606
- MAE (H=1): 0.2067
- RMSE (H=3): 0.5566
- RMSE (H=6): 1.0766
- Degradation: H3=+113.6%, H6=+313.1%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**3. DFM2 Model**
- ID: `DFM2-034-v02-010121`
- RMSE (H=1): 0.2612
- MAE (H=1): 0.2209
- RMSE (H=3): 0.5981
- RMSE (H=6): 1.1889
- Degradation: H3=+129.0%, H6=+355.2%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**4. StandardizedRidge Model**
- ID: `StandardizedRidge-133-v05-010216`
- RMSE (H=1): 0.3716
- MAE (H=1): 0.3346
- RMSE (H=3): 0.7307
- RMSE (H=6): 1.4838
- Degradation: H3=+96.6%, H6=+299.3%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**5. Ridge Model**
- ID: `Ridge-121-v09-010215`
- RMSE (H=1): 0.3832
- MAE (H=1): 0.3458
- RMSE (H=3): 0.7349
- RMSE (H=6): 1.4702
- Degradation: H3=+91.8%, H6=+283.7%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-010120 | 0.2606 | +32.0% |
| DFM | DFM-029-v13-010120 | 0.5505 | +178.8% |
| DFM2 | DFM2-034-v02-010121 | 0.2612 | +32.3% |
| ElasticNet | ElasticNet-057-v09-010123 | 0.4295 | +117.5% |
| ElasticNetGrid | ElasticNetGrid-072-v08-010145 | 0.1975 | 0.0% |
| Lasso | Lasso-085-v05-010209 | 0.4240 | +114.8% |
| RandomForest | RandomForest-097-v01-010211 | 1.7932 | +808.2% |
| Ridge | Ridge-121-v09-010215 | 0.3832 | +94.1% |
| StandardizedRidge | StandardizedRidge-133-v05-010216 | 0.3716 | +88.2% |

### Forecast Visualizations

#### 1. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_1m_elasticnetgrid_rank1.png)

#### 2. AR1 Model Forecast
![AR1 Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_1m_ar1_rank2.png)

#### 3. DFM2 Model Forecast
![DFM2 Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_1m_dfm2_rank3.png)

#### All Models Comparison
![1-Month Deposit Rate Comparison](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_1m_comparison.png)

---

## 4. 3-Month Deposit Rate

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-133-v05-010313`
- RMSE (H=1): 0.1663
- MAE (H=1): 0.1238
- RMSE (H=3): 0.3363
- RMSE (H=6): 0.7692
- Degradation: H3=+102.3%, H6=+362.6%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-125-v13-010312`
- RMSE (H=1): 0.1711
- MAE (H=1): 0.1278
- RMSE (H=3): 0.3428
- RMSE (H=6): 0.7719
- Degradation: H3=+100.3%, H6=+351.1%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**3. ElasticNetGrid Model**
- ID: `ElasticNetGrid-076-v12-010255`
- RMSE (H=1): 0.2048
- MAE (H=1): 0.1744
- RMSE (H=3): 0.3932
- RMSE (H=6): 0.7338
- Degradation: H3=+92.0%, H6=+258.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**4. DFM2 Model**
- ID: `DFM2-041-v09-010218`
- RMSE (H=1): 0.2618
- MAE (H=1): 0.2191
- RMSE (H=3): 0.5438
- RMSE (H=6): 1.0211
- Degradation: H3=+107.7%, H6=+290.0%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. AR1 Model**
- ID: `AR1-009-v09-010217`
- RMSE (H=1): 0.2852
- MAE (H=1): 0.2218
- RMSE (H=3): 0.5693
- RMSE (H=6): 1.0215
- Degradation: H3=+99.6%, H6=+258.2%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-009-v09-010217 | 0.2852 | +71.5% |
| DFM | DFM-021-v05-010217 | 0.3637 | +118.7% |
| DFM2 | DFM2-041-v09-010218 | 0.2618 | +57.5% |
| ElasticNet | ElasticNet-053-v05-010219 | 0.3043 | +83.0% |
| ElasticNetGrid | ElasticNetGrid-076-v12-010255 | 0.2048 | +23.2% |
| Lasso | Lasso-081-v01-010306 | 0.2962 | +78.2% |
| RandomForest | RandomForest-109-v13-010311 | 1.6808 | +910.9% |
| Ridge | Ridge-125-v13-010312 | 0.1711 | +2.9% |
| StandardizedRidge | StandardizedRidge-133-v05-010313 | 0.1663 | 0.0% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_3m_standardizedridge_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_3m_ridge_rank2.png)

#### 3. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_3m_elasticnetgrid_rank3.png)

#### All Models Comparison
![3-Month Deposit Rate Comparison](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_3m_comparison.png)

---

## 5. 6-Month Deposit Rate

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-142-v14-010410`
- RMSE (H=1): 0.1499
- MAE (H=1): 0.1282
- RMSE (H=3): 0.3257
- RMSE (H=6): 0.7042
- Degradation: H3=+117.3%, H6=+369.7%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-126-v14-010409`
- RMSE (H=1): 0.1516
- MAE (H=1): 0.1301
- RMSE (H=3): 0.3280
- RMSE (H=6): 0.7083
- Degradation: H3=+116.3%, H6=+367.1%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**3. ElasticNetGrid Model**
- ID: `ElasticNetGrid-069-v05-010332`
- RMSE (H=1): 0.1695
- MAE (H=1): 0.1357
- RMSE (H=3): 0.3318
- RMSE (H=6): 0.6190
- Degradation: H3=+95.8%, H6=+265.2%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**4. DFM2 Model**
- ID: `DFM2-041-v09-010315`
- RMSE (H=1): 0.2279
- MAE (H=1): 0.1906
- RMSE (H=3): 0.4653
- RMSE (H=6): 0.8730
- Degradation: H3=+104.2%, H6=+283.0%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. ElasticNet Model**
- ID: `ElasticNet-057-v09-010317`
- RMSE (H=1): 0.2573
- MAE (H=1): 0.2212
- RMSE (H=3): 0.4614
- RMSE (H=6): 0.8726
- Degradation: H3=+79.3%, H6=+239.2%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-010313 | 0.2816 | +87.9% |
| DFM | DFM-029-v13-010314 | 0.3000 | +100.1% |
| DFM2 | DFM2-041-v09-010315 | 0.2279 | +52.0% |
| ElasticNet | ElasticNet-057-v09-010317 | 0.2573 | +71.6% |
| ElasticNetGrid | ElasticNetGrid-069-v05-010332 | 0.1695 | +13.1% |
| Lasso | Lasso-085-v05-010403 | 0.2593 | +72.9% |
| RandomForest | RandomForest-105-v09-010407 | 1.6543 | +1003.5% |
| Ridge | Ridge-126-v14-010409 | 0.1516 | +1.2% |
| StandardizedRidge | StandardizedRidge-142-v14-010410 | 0.1499 | 0.0% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_6m_standardizedridge_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_6m_ridge_rank2.png)

#### 3. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_6m_elasticnetgrid_rank3.png)

#### All Models Comparison
![6-Month Deposit Rate Comparison](2109_model_test_all_y-20250922-005902/visualizations/deposit_rate_6m_comparison.png)

---

## 6. GDP Year-over-Year

### Top 5 Models (Diverse Selection)

**1. AR1 Model 🏆**
- ID: `AR1-004-v04-005957`
- RMSE (H=1): 2.2174
- MAE (H=1): 0.9495
- RMSE (H=3): 3.0399
- RMSE (H=6): 4.2724
- Degradation: H3=+37.1%, H6=+92.7%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**2. DFM2 Model**
- ID: `DFM2-044-v12-005958`
- RMSE (H=1): 2.2327
- MAE (H=1): 0.9892
- RMSE (H=3): 3.0983
- RMSE (H=6): 4.6517
- Degradation: H3=+38.8%, H6=+108.3%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**3. Lasso Model**
- ID: `Lasso-096-v16-010046`
- RMSE (H=1): 2.3144
- MAE (H=1): 1.3265
- RMSE (H=3): 2.7908
- RMSE (H=6): 3.5068
- Degradation: H3=+20.6%, H6=+51.5%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**4. ElasticNet Model**
- ID: `ElasticNet-060-v12-010000`
- RMSE (H=1): 2.3169
- MAE (H=1): 1.3320
- RMSE (H=3): 2.7863
- RMSE (H=6): 3.5102
- Degradation: H3=+20.3%, H6=+51.5%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. StandardizedRidge Model**
- ID: `StandardizedRidge-140-v12-010050`
- RMSE (H=1): 2.3223
- MAE (H=1): 1.0691
- RMSE (H=3): 3.2700
- RMSE (H=6): 5.1546
- Degradation: H3=+40.8%, H6=+122.0%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-004-v04-005957 | 2.2174 | 0.0% |
| DFM | DFM-024-v08-005957 | 3.4423 | +55.2% |
| DFM2 | DFM2-044-v12-005958 | 2.2327 | +0.7% |
| ElasticNet | ElasticNet-060-v12-010000 | 2.3169 | +4.5% |
| ElasticNetGrid | ElasticNetGrid-076-v12-010033 | 2.3306 | +5.1% |
| Lasso | Lasso-096-v16-010046 | 2.3144 | +4.4% |
| RandomForest | RandomForest-106-v10-010048 | 3.6815 | +66.0% |
| Ridge | Ridge-116-v04-010049 | 2.3554 | +6.2% |
| StandardizedRidge | StandardizedRidge-140-v12-010050 | 2.3223 | +4.7% |

### Forecast Visualizations

#### 1. AR1 Model Forecast
![AR1 Forecast](2109_model_test_all_y-20250922-005902/visualizations/gdp_yoy_ar1_rank1.png)

#### 2. DFM2 Model Forecast
![DFM2 Forecast](2109_model_test_all_y-20250922-005902/visualizations/gdp_yoy_dfm2_rank2.png)

#### 3. Lasso Model Forecast
![Lasso Forecast](2109_model_test_all_y-20250922-005902/visualizations/gdp_yoy_lasso_rank3.png)

#### All Models Comparison
![GDP Year-over-Year Comparison](2109_model_test_all_y-20250922-005902/visualizations/gdp_yoy_comparison.png)

---

## 7. Policy Rate (7DRR)

### Top 5 Models (Diverse Selection)

**1. AR1 Model 🏆**
- ID: `AR1-016-v16-010055`
- RMSE (H=1): 0.3129
- MAE (H=1): 0.2625
- RMSE (H=3): 0.5851
- RMSE (H=6): 0.9634
- Degradation: H3=+87.0%, H6=+207.9%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**2. StandardizedRidge Model**
- ID: `StandardizedRidge-133-v05-010119`
- RMSE (H=1): 0.4993
- MAE (H=1): 0.4257
- RMSE (H=3): 0.9797
- RMSE (H=6): 1.6692
- Degradation: H3=+96.2%, H6=+234.3%
- Features: 12 variables
- Normalization: None
- Feature Pack: None

**3. Ridge Model**
- ID: `Ridge-126-v14-010119`
- RMSE (H=1): 0.5629
- MAE (H=1): 0.5037
- RMSE (H=3): 1.0549
- RMSE (H=6): 1.6053
- Degradation: H3=+87.4%, H6=+185.2%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**4. ElasticNetGrid Model**
- ID: `ElasticNetGrid-080-v16-010116`
- RMSE (H=1): 0.5941
- MAE (H=1): 0.4706
- RMSE (H=3): 0.9021
- RMSE (H=6): 1.6229
- Degradation: H3=+51.9%, H6=+173.2%
- Features: 12 variables
- Normalization: {'method': 'standardize'}
- Feature Pack: None

**5. DFM2 Model**
- ID: `DFM2-047-v15-010056`
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
| AR1 | AR1-016-v16-010055 | 0.3129 | 0.0% |
| DFM | DFM-022-v06-010055 | 0.9478 | +203.0% |
| DFM2 | DFM2-047-v15-010056 | 0.6182 | +97.6% |
| ElasticNet | ElasticNet-049-v01-010056 | 0.8584 | +174.4% |
| ElasticNetGrid | ElasticNetGrid-080-v16-010116 | 0.5941 | +89.9% |
| Lasso | Lasso-089-v09-010117 | 0.8036 | +156.9% |
| RandomForest | RandomForest-105-v09-010118 | 0.9330 | +198.2% |
| Ridge | Ridge-126-v14-010119 | 0.5629 | +79.9% |
| StandardizedRidge | StandardizedRidge-133-v05-010119 | 0.4993 | +59.6% |

### Forecast Visualizations

#### 1. AR1 Model Forecast
![AR1 Forecast](2109_model_test_all_y-20250922-005902/visualizations/policy_rate_7drr_ar1_rank1.png)

#### 2. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](2109_model_test_all_y-20250922-005902/visualizations/policy_rate_7drr_standardizedridge_rank2.png)

#### 3. Ridge Model Forecast
![Ridge Forecast](2109_model_test_all_y-20250922-005902/visualizations/policy_rate_7drr_ridge_rank3.png)

#### All Models Comparison
![Policy Rate (7DRR) Comparison](2109_model_test_all_y-20250922-005902/visualizations/policy_rate_7drr_comparison.png)

---

## 8. USD/IDR Exchange Rate

*No valid results found for USD/IDR Exchange Rate*

## Key Insights

1. **AR1 models** performed best on 2/8 targets, suggesting strong autoregressive patterns
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
