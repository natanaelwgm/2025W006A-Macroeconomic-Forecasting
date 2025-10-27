# 🔄 DATE-BASED TRAIN/TEST UPDATE

## ✅ What Changed

### 1. **Train/Test Dates in Recipe_Config** (New Feature!)
The dashboard now uses **date-based train/test splits** like your recipe files, instead of simple percentage splits.

**New fields in Recipe_Config sheet:**
- Row 57: `Train Start Date` (default: 2005-01-01)
- Row 58: `Train End Date` (default: 2019-12-31)
- Row 59: `Test Start Date` (default: 2020-01-01)
- Row 60: `Test End Date` (default: 2024-12-31)
- Row 61: `Date Column` (default: 'date')

### 2. **Real Models from Config** (No More Dummy Models!)
The backcast now trains **actual models** you select in Recipe_Config, not dummy/fake models.

**Supported models:**
- ✅ Linear, Ridge, Lasso, ElasticNet
- ✅ RandomForest, GradientBoosting, ExtraTrees, DecisionTree
- ✅ Naive, SeasonalNaive, Drift (baseline models)
- ✅ More models can be added easily!

### 3. **44 Models Available**
Expanded from 33 to **44 models**:
- Added: MovingAverage, ExponentialSmoothing
- Added: QuantileRegression
- Added: SARIMAX, VAR
- Added: LightGBM, CatBoost
- Added: NeuralNetwork
- Added: PCA
- Added: GRU, Transformer

---

## 📊 How It Works Now

### Old Way (Percentage Split):
```
Total data: 100 rows
Test Split: 20%
→ Train: first 80 rows
→ Test: last 20 rows
```

### New Way (Date-Based):
```
Data from 2005-2024
Train: 2005-01-01 to 2019-12-31
Test: 2020-01-01 to 2024-12-31
→ Uses dates to filter data
→ Matches your recipe structure!
```

---

## 🎯 Recipe Structure Compatibility

Your recipes have this structure:
```json
{
  "train": { "start": "2005-01-01", "end": "2019-12-31" },
  "test": { "start": "2020-01-01", "end": "2025-12-31" },
  "models_filter": ["Linear", "Ridge", "RandomForest", ...]
}
```

**Dashboard now matches this!** ✅

---

## 🚀 How to Use

### Step 1: Load Data
Click **"Load Real Data"** button to load your merged dataset.

### Step 2: Configure Train/Test Dates
In Recipe_Config sheet:
- Edit cells B57-B60 for train/test date ranges
- Format: YYYY-MM-DD
- Example: 2005-01-01

### Step 3: Select Models
Check/uncheck models in Recipe_Config (rows 10-53)

### Step 4: Run Backcast
Click **"Run Backcast"** button
- It reads your date settings
- Filters data by dates
- Trains selected models
- Shows results!

---

## 📝 Key Differences

| Feature | Before | After |
|---------|--------|-------|
| Split Method | % of data | Date ranges |
| Models Used | Dummy/fake | Real selected models |
| Model Count | 33 | 44 |
| Recipe Match | ❌ | ✅ |
| Date Flexibility | Fixed % | Custom dates |

---

## 🔧 Technical Details

### Date Filtering:
```python
train_mask = (df[date_col] >= train_start) & (df[date_col] <= train_end)
test_mask = (df[date_col] >= test_start) & (df[date_col] <= test_end)
```

### Model Training:
```python
# Now uses actual models from config
selected_models = get_selected_models(wb)

for model_name in selected_models:
    if model_name == 'RandomForest':
        model = RandomForestRegressor(...)
    elif model_name == 'Ridge':
        model = Ridge(...)
    # etc.
```

---

## 🎉 Benefits

1. **Consistent with your recipes** - Same date logic
2. **Flexible date ranges** - Test different time periods
3. **Real model performance** - Not dummy results
4. **Professional backtesting** - Industry-standard approach
5. **Easy to adjust** - Just change dates in Excel

---

## 📌 Example Usage

### Monthly Data (2005-2024):
```
Train: 2005-01-01 to 2019-12-31 (15 years)
Test:  2020-01-01 to 2024-12-31 (5 years)
```

### Quarterly Data (2000-2024):
```
Train: 2000-01-01 to 2018-12-31 (19 years)
Test:  2019-01-01 to 2024-12-31 (6 years)
```

### Yearly Data (1990-2024):
```
Train: 1990-01-01 to 2010-12-31 (21 years)
Test:  2011-01-01 to 2024-12-31 (14 years)
```

---

## 🔄 Files Updated

1. **SMFdashboard_recipe.py**
   - `run_recipe_backcast()` - Date-based split + real models
   - `setup_recipe_config_sheet()` - Added train/test date fields
   - `template_start_row` - Adjusted to 63 (was 59)

2. **VBA_CODE_RECIPE_V2.txt**
   - Updated STEP 4 - Model selection + date configuration
   - Updated STEP 6 - Backcast description
   - Added 44 models documentation

3. **This file!**
   - Complete documentation of changes

---

## ✅ Testing Checklist

- [x] Load data from merged datasets
- [x] Read train/test dates from Recipe_Config
- [x] Filter data by dates correctly
- [x] Train actual selected models (not dummy)
- [x] Calculate metrics (RMSE, MAE, R²)
- [x] Display Actual vs Predicted
- [x] Show date range info
- [x] Handle 44 models without overlap

---

## 🎓 Next Steps

1. **Test with your monthly data:**
   - Load: smf_monthly_data.csv
   - Set dates: 2005-2024
   - Select 5-10 models
   - Run backcast

2. **Try different date ranges:**
   - Short train: 2015-2019
   - Long train: 2000-2019
   - Recent test: 2023-2024

3. **Compare with your recipe results:**
   - Same dates
   - Same models
   - Should get similar performance!

---

## 📞 Support

If you encounter issues:
1. Check date format (YYYY-MM-DD)
2. Verify data has dates in range
3. Make sure models are checked in Recipe_Config
4. Try with fewer models first (3-5)

---

**Created:** 2025-10-26
**Version:** 2.0 - Date-Based Backcast Update

