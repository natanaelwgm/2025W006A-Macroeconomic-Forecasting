# Indonesia Macroeconomic Nowcasting Report

**Generated:** 2025-10-09 09:09:36
**Output Directory:** `updated_comprehensive_yearly-20251009-090809`

## Executive Summary

This report presents nowcasting results for **3 macroeconomic indicators** using multiple machine learning models.

## Model Performance Overview

### Best Performing Models by Target Variable

| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |
|-----------------|------------|------|------------|-----------|-----|
| Cpi | Ridge-073-v01-090836 | Ridge | 0.8863 | 0.7184 | N/A |
| Deposit Rate 6M | StandardizedRidge-085-v01-090931 | StandardizedRidge | 0.8830 | 0.7866 | N/A |
| Real Gdp Growth | ElasticNetGrid-029-v01-090852 | ElasticNetGrid | 0.6600 | 0.4265 | N/A |

### Model Type Performance Summary

Average performance across all targets by model type:

| Model Type | Avg RMSE | Min RMSE | # Targets |
|------------|----------|----------|-----------|
| AR1 | 66.8672 | 1.9738 | 3 |
| ARp | 4.1759 | 3.1353 | 3 |
| BVAR | 1.8125 | 1.0967 | 3 |
| Bagging | 1.8391 | 1.0958 | 3 |
| DFM | 6.8990 | 1.4485 | 3 |
| DFM2 | 4.1759 | 3.1353 | 3 |
| ElasticNet | 2.2732 | 1.0693 | 3 |
| ElasticNetGrid | 1.3600 | 0.6600 | 3 |
| ExtraTrees | 1.8125 | 1.0967 | 3 |
| GARCH | 6.3581 | 2.8078 | 3 |
| GradientBoosting | 1.8125 | 1.0967 | 3 |
| Huber | 4.1759 | 3.1353 | 3 |
| LSTM | 77.5216 | 1.4410 | 3 |
| Lasso | 2.5320 | 0.9354 | 3 |
| Linear | 4.1759 | 3.1353 | 3 |
| Naive | 2.6659 | 1.9112 | 3 |
| PLS1 | 124.2025 | 1.3128 | 3 |
| RandomForest | 1.9200 | 1.1055 | 3 |
| Ridge | 3.1501 | 0.8863 | 3 |
| SeasonalNaive | 2.6659 | 1.9112 | 3 |
| StandardizedLinear | 4.1759 | 3.1353 | 3 |
| StandardizedRidge | 9.5304 | 0.8830 | 3 |
| StochasticGB | 1.8874 | 1.1035 | 3 |
| Tree | 1.8125 | 1.0967 | 3 |
| XGBoost | 2.5429 | 1.4191 | 3 |

## 1. Cpi

### Top 5 Models (Diverse Selection)

**1. Ridge Model 🏆**
- ID: `Ridge-073-v01-090836`
- RMSE (H=1): 0.8863
- MAE (H=1): 0.7184
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Lasso Model**
- ID: `Lasso-054-v02-090829`
- RMSE (H=1): 0.9354
- MAE (H=1): 0.8901
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. ElasticNetGrid Model**
- ID: `ElasticNetGrid-030-v02-090823`
- RMSE (H=1): 0.9866
- MAE (H=1): 0.9201
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. ElasticNet Model**
- ID: `ElasticNet-026-v02-090822`
- RMSE (H=1): 1.0693
- MAE (H=1): 0.9426
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. Bagging Model**
- ID: `Bagging-014-v02-090816`
- RMSE (H=1): 1.0958
- MAE (H=1): 1.0177
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-090812 | 2.6292 | +196.6% |
| ARp | ARp-005-v01-090813 | 3.1353 | +253.7% |
| BVAR | BVAR-009-v01-090814 | 1.0967 | +23.7% |
| Bagging | Bagging-014-v02-090816 | 1.0958 | +23.6% |
| DFM | DFM-018-v02-090818 | 1.4485 | +63.4% |
| DFM2 | DFM2-022-v02-090820 | 3.1353 | +253.7% |
| ElasticNet | ElasticNet-026-v02-090822 | 1.0693 | +20.6% |
| ElasticNetGrid | ElasticNetGrid-030-v02-090823 | 0.9866 | +11.3% |
| ExtraTrees | ExtraTrees-034-v02-090824 | 1.0967 | +23.7% |
| GARCH | GARCH-038-v02-090825 | 2.8078 | +216.8% |
| GradientBoosting | GradientBoosting-041-v01-090826 | 1.0967 | +23.7% |
| Huber | Huber-046-v02-090827 | 3.1353 | +253.7% |
| LSTM | LSTM-050-v02-090828 | 1.4410 | +62.6% |
| Lasso | Lasso-054-v02-090829 | 0.9354 | +5.5% |
| Linear | Linear-057-v01-090831 | 3.1353 | +253.7% |
| Naive | Naive-062-v02-090832 | 1.9112 | +115.6% |
| PLS1 | PLS1-066-v02-090833 | 1.3128 | +48.1% |
| RandomForest | RandomForest-069-v01-090835 | 1.1055 | +24.7% |
| Ridge | Ridge-073-v01-090836 | 0.8863 | 0.0% |
| SeasonalNaive | SeasonalNaive-078-v02-090837 | 1.9112 | +115.6% |
| StandardizedLinear | StandardizedLinear-081-v01-090838 | 3.1353 | +253.7% |
| StandardizedRidge | StandardizedRidge-086-v02-090839 | 1.2205 | +37.7% |
| StochasticGB | StochasticGB-090-v02-090840 | 1.1035 | +24.5% |
| Tree | Tree-094-v02-090841 | 1.0967 | +23.7% |
| XGBoost | XGBoost-097-v01-090842 | 1.4191 | +60.1% |

### Forecast Visualizations

#### 1. Ridge Model Forecast
![Ridge Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/CPI_ridge_rank1.png)

#### 2. Lasso Model Forecast
![Lasso Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/CPI_lasso_rank2.png)

#### 3. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/CPI_elasticnetgrid_rank3.png)

#### All Models Comparison
![Cpi Comparison](updated_comprehensive_yearly-20251009-090809/visualizations/CPI_comparison.png)

---

## 2. Deposit Rate 6M

### Top 5 Models (Diverse Selection)

**1. StandardizedRidge Model 🏆**
- ID: `StandardizedRidge-085-v01-090931`
- RMSE (H=1): 0.8830
- MAE (H=1): 0.7866
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Ridge Model**
- ID: `Ridge-074-v02-090929`
- RMSE (H=1): 1.0316
- MAE (H=1): 0.5851
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. AR1 Model**
- ID: `AR1-002-v02-090913`
- RMSE (H=1): 1.9738
- MAE (H=1): 1.6330
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. PLS1 Model**
- ID: `PLS1-065-v01-090927`
- RMSE (H=1): 2.0650
- MAE (H=1): 1.9441
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. RandomForest Model**
- ID: `RandomForest-070-v02-090928`
- RMSE (H=1): 2.1125
- MAE (H=1): 1.9444
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-002-v02-090913 | 1.9738 | +123.5% |
| ARp | ARp-006-v02-090914 | 4.5724 | +417.9% |
| BVAR | BVAR-010-v02-090915 | 2.2002 | +149.2% |
| Bagging | Bagging-013-v01-090915 | 2.1393 | +142.3% |
| DFM | DFM-018-v02-090916 | 2.2647 | +156.5% |
| DFM2 | DFM2-021-v01-090917 | 4.5724 | +417.9% |
| ElasticNet | ElasticNet-025-v01-090919 | 2.1730 | +146.1% |
| ElasticNetGrid | ElasticNetGrid-030-v02-090920 | 2.4334 | +175.6% |
| ExtraTrees | ExtraTrees-034-v02-090921 | 2.2002 | +149.2% |
| GARCH | GARCH-037-v01-090922 | 4.2214 | +378.1% |
| GradientBoosting | GradientBoosting-042-v02-090923 | 2.2002 | +149.2% |
| Huber | Huber-045-v01-090923 | 4.5724 | +417.9% |
| LSTM | LSTM-050-v02-090924 | 6.8699 | +678.1% |
| Lasso | Lasso-053-v01-090925 | 2.2002 | +149.2% |
| Linear | Linear-057-v01-090926 | 4.5724 | +417.9% |
| Naive | Naive-062-v02-090927 | 2.3162 | +162.3% |
| PLS1 | PLS1-065-v01-090927 | 2.0650 | +133.9% |
| RandomForest | RandomForest-070-v02-090928 | 2.1125 | +139.2% |
| Ridge | Ridge-074-v02-090929 | 1.0316 | +16.8% |
| SeasonalNaive | SeasonalNaive-077-v01-090930 | 2.3162 | +162.3% |
| StandardizedLinear | StandardizedLinear-082-v02-090931 | 4.5724 | +417.9% |
| StandardizedRidge | StandardizedRidge-085-v01-090931 | 0.8830 | 0.0% |
| StochasticGB | StochasticGB-090-v02-090932 | 2.1474 | +143.2% |
| Tree | Tree-094-v02-090933 | 2.2002 | +149.2% |
| XGBoost | XGBoost-098-v02-090935 | 2.6186 | +196.6% |

### Forecast Visualizations

#### 1. StandardizedRidge Model Forecast
![StandardizedRidge Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/Deposit Rate 6M_standardizedridge_rank1.png)

#### 2. Ridge Model Forecast
![Ridge Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/Deposit Rate 6M_ridge_rank2.png)

#### 3. AR1 Model Forecast
![AR1 Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/Deposit Rate 6M_ar1_rank3.png)

#### All Models Comparison
![Deposit Rate 6M Comparison](updated_comprehensive_yearly-20251009-090809/visualizations/Deposit Rate 6M_comparison.png)

---

## 3. Real Gdp Growth

### Top 5 Models (Diverse Selection)

**1. ElasticNetGrid Model 🏆**
- ID: `ElasticNetGrid-029-v01-090852`
- RMSE (H=1): 0.6600
- MAE (H=1): 0.4265
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**2. Tree Model**
- ID: `Tree-093-v01-090906`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**3. BVAR Model**
- ID: `BVAR-009-v01-090847`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**4. GradientBoosting Model**
- ID: `GradientBoosting-042-v02-090855`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

**5. ExtraTrees Model**
- ID: `ExtraTrees-034-v02-090853`
- RMSE (H=1): 2.1405
- MAE (H=1): 2.0511
- Features: 5 variables
- Normalization: None
- Feature Pack: None

### Best Model by Type

| Model Type | Best Config | RMSE (H=1) | vs Best |
|------------|-------------|------------|---------|
| AR1 | AR1-001-v01-090845 | 195.9986 | +29597.9% |
| ARp | ARp-005-v01-090846 | 4.8200 | +630.3% |
| BVAR | BVAR-009-v01-090847 | 2.1405 | +224.3% |
| Bagging | Bagging-013-v01-090848 | 2.2823 | +245.8% |
| DFM | DFM-018-v02-090849 | 16.9839 | +2473.4% |
| DFM2 | DFM2-021-v01-090849 | 4.8200 | +630.3% |
| ElasticNet | ElasticNet-026-v02-090851 | 3.5773 | +442.0% |
| ElasticNetGrid | ElasticNetGrid-029-v01-090852 | 0.6600 | 0.0% |
| ExtraTrees | ExtraTrees-034-v02-090853 | 2.1405 | +224.3% |
| GARCH | GARCH-038-v02-090854 | 12.0452 | +1725.1% |
| GradientBoosting | GradientBoosting-042-v02-090855 | 2.1405 | +224.3% |
| Huber | Huber-045-v01-090856 | 4.8200 | +630.3% |
| LSTM | LSTM-049-v01-090857 | 224.2540 | +33879.2% |
| Lasso | Lasso-053-v01-090857 | 4.4604 | +575.8% |
| Linear | Linear-058-v02-090859 | 4.8200 | +630.3% |
| Naive | Naive-061-v01-090859 | 3.7703 | +471.3% |
| PLS1 | PLS1-066-v02-090901 | 369.2297 | +55846.1% |
| RandomForest | RandomForest-069-v01-090901 | 2.5422 | +285.2% |
| Ridge | Ridge-074-v02-090902 | 7.5325 | +1041.3% |
| SeasonalNaive | SeasonalNaive-078-v02-090903 | 3.7703 | +471.3% |
| StandardizedLinear | StandardizedLinear-082-v02-090904 | 4.8200 | +630.3% |
| StandardizedRidge | StandardizedRidge-086-v02-090905 | 26.4878 | +3913.5% |
| StochasticGB | StochasticGB-089-v01-090906 | 2.4115 | +265.4% |
| Tree | Tree-093-v01-090906 | 2.1405 | +224.3% |
| XGBoost | XGBoost-097-v01-090908 | 3.5912 | +444.1% |

### Forecast Visualizations

#### 1. ElasticNetGrid Model Forecast
![ElasticNetGrid Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/Real GDP Growth_elasticnetgrid_rank1.png)

#### 2. Tree Model Forecast
![Tree Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/Real GDP Growth_tree_rank2.png)

#### 3. BVAR Model Forecast
![BVAR Forecast](updated_comprehensive_yearly-20251009-090809/visualizations/Real GDP Growth_bvar_rank3.png)

#### All Models Comparison
![Real Gdp Growth Comparison](updated_comprehensive_yearly-20251009-090809/visualizations/Real GDP Growth_comparison.png)

---

## Key Insights

1. **AR1 models** performed best on 0/3 targets, suggesting strong autoregressive patterns
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
