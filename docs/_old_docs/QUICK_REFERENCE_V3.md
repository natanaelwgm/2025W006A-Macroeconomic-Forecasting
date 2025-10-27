# 🚀 QUICK REFERENCE - Recipe Dashboard V3

## ⚡ What's New

### Date-Based Train/Test ✅
- Set exact date ranges (like your recipe files)
- Train: 2005-01-01 to 2019-12-31
- Test: 2020-01-01 to 2024-12-31

### Real Models from Config ✅
- Backcast uses YOUR selected models
- No more dummy/fake models
- Actual performance metrics

### 44 Models Total ✅
- Up from 33 models
- All your repos combined
- Check/uncheck in Recipe_Config

---

## 🎯 Quick Start

### 1. Setup (One Time)
```
Click: [Setup Recipe Dashboard]
→ Creates all sheets with 44 models
```

### 2. Load Data
```
Option A: [Load Real Data]
→ Uses path from Recipe_Config B5
→ Default: smf_monthly_data.csv

Option B: [Generate Dummy Data]
→ For testing only
```

### 3. Configure
```
Click: [View Config]
→ Check models (rows 10-53)
→ Set dates (rows 57-60)
→ Edit hyperparameters (column G)
```

### 4. Analyze
```
[Run Backcast] → Test on historical data
[Refresh Charts] → Visualize results
[View Rankings] → See best models
```

### 5. Save
```
[Save Recipe] → Save your config
→ Name in Recipe_Config B4
```

---

## 📍 Important Cell Locations

### Recipe_Config Sheet
| Cell | Content | Purpose |
|------|---------|---------|
| B4 | Recipe Name | For saving custom recipes |
| B5 | Data Path | Path to CSV file |
| A10-C53 | Models (44) | Check to select |
| E9-H40 | Hyperparams | Edit values in column G |
| B56 | Horizons | 1,3,6,12 |
| B57 | Train Start | 2005-01-01 |
| B58 | Train End | 2019-12-31 |
| B59 | Test Start | 2020-01-01 |
| B60 | Test End | 2024-12-31 |
| B61 | Date Column | date |

### Dashboard Sheet
| Cell | Content |
|------|---------|
| B4 | Frequency (M/Q/S/Y) |
| G5 | Top N models (3/5/10) |
| B27 | Status messages |

---

## 🔧 VBA Macros

### Data
```vba
LoadRealData()          ' Load from path in B5
GenerateDummyData()     ' Generate test data
```

### Analysis
```vba
RunBackcast()           ' Date-based backtesting
RunForecast()           ' Future predictions
RefreshCharts()         ' Create visualizations
ViewRankings()          ' Model comparison
```

### Config
```vba
SetupRecipeDashboard()  ' Initial setup
ViewConfiguration()     ' Open Recipe_Config
SaveRecipe()            ' Save custom recipe
```

---

## 📊 44 Models Available

### Basic (5)
- Naive, SeasonalNaive, Drift
- MovingAverage, ExponentialSmoothing

### Linear (10)
- Linear, StandardizedLinear
- Ridge, StandardizedRidge
- Lasso, ElasticNet, ElasticNetGrid
- Huber, PLS1, QuantileRegression

### Time Series (7)
- AR1, ARp, ARIMA, SARIMAX
- TVP, BVAR, VAR

### Tree-Based (9)
- DecisionTree
- RandomForest, ExtraTrees
- GradientBoosting, StochasticGB
- XGBoost, LightGBM, CatBoost
- Bagging

### Advanced ML (3)
- KNN, SVR, NeuralNetwork

### Factor Models (3)
- DFM, DFM2, PCA

### Financial (4)
- GARCH, NeuroGARCH, DNS, MIDAS

### Deep Learning (3)
- LSTM, GRU, Transformer

---

## 💡 Pro Tips

### For Fast Testing
1. Select only 5-10 models
2. Limit to 5 variables (first 5 in code)
3. Use shorter date ranges

### For Production
1. Select all relevant models
2. Use full dataset
3. Set appropriate train/test split
4. Save multiple recipes for comparison

### Date Format
Always use: `YYYY-MM-DD`
- ✅ 2005-01-01
- ❌ 01/01/2005
- ❌ 2005-1-1

### Model Selection
- Start with Naive, Linear, Ridge (fast baselines)
- Add RandomForest, XGBoost (good performance)
- Try ARIMA for time series patterns
- Test advanced models last (slower)

---

## 🐛 Troubleshooting

### "No data loaded"
→ Click "Load Real Data" first
→ Or "Generate Dummy Data"

### "No models selected"
→ Open Recipe_Config
→ Check boxes in column A (rows 10-53)

### "Date parse error"
→ Check date format: YYYY-MM-DD
→ Verify date column exists

### "Template overlap"
→ Fixed! Template now starts row 63
→ No overlap with 44 models

### Models not showing
→ Close Excel completely
→ Run: python force_refresh_config.py
→ Reopen and "Setup Recipe Dashboard"

---

## 📂 File Structure

```
SMFdashboard/
├── SMFdashboard_recipe.py          ← Main code (date-based backcast!)
├── SMFdashboard.xlsm                ← Excel file
├── VBA_CODE_RECIPE_V2.txt           ← VBA macros
├── force_refresh_config.py          ← Fix cache issues
├── DATE_BASED_BACKCAST_UPDATE.md    ← Detailed changelog
├── QUICK_REFERENCE_V3.md            ← This file!
├── data/
│   └── merged/
│       ├── smf_monthly_data.csv     ← Default data
│       ├── smf_quarterly_data.csv
│       ├── smf_semesterly_data.csv
│       ├── smf_yearly_data.csv
│       └── smf_daily_data.csv
└── custom_recipes/
    └── *.json                        ← Saved recipes
```

---

## ✅ Workflow Example

```
1. [Setup Recipe Dashboard]
2. [Load Real Data]
3. [View Config]
   - Check: Naive, Linear, Ridge, RandomForest, XGBoost
   - Dates: 2005-2019 train, 2020-2024 test
4. [Run Backcast]
   - See performance metrics
   - Check Actual vs Predicted
5. [View Rankings]
   - Compare all models
   - See best performers
6. [Refresh Charts]
   - Visualize for each variable
7. [Save Recipe]
   - Name: "my_monthly_recipe"
```

---

## 🎓 Learning Path

### Beginner
1. Use dummy data
2. Select 3-5 simple models
3. Default date ranges
4. Run backcast
5. View charts

### Intermediate
1. Load real merged data
2. Select 10-15 models
3. Adjust date ranges
4. Compare results
5. Save recipes

### Advanced
1. Multiple frequency tests
2. All 44 models
3. Custom hyperparameters
4. Cross-validation periods
5. Recipe library

---

**Version:** 3.0  
**Updated:** 2025-10-26  
**Key Features:** Date-based split + Real models + 44 models

