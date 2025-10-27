# SMF Dashboard - Macroeconomic Forecasting Tool

A comprehensive Excel-based dashboard for macroeconomic forecasting using multiple machine learning models, built with xlwings and Python.

## 🎯 Overview

This dashboard provides an interactive Excel interface for:
- **Time Series Forecasting** - Predict future values using multiple models
- **Backcast Validation** - Test model performance on historical data
- **Visual Comparisons** - Side-by-side backcast and forecast charts
- **45+ Models** - Linear, Tree-based, Neural Networks, GARCH, and more
- **Multiple Frequencies** - Daily, Weekly, Monthly, Quarterly, Semesterly, Yearly data

## 🚀 Quick Start

### First Time Setup

#### 1. Install Python (if needed)

**Check if Python is installed:**
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Type: `python --version`
3. If you see a version number → **Ready!** ✅
4. If you see "command not found" → **Install Python** (see below)

**Install Python:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or later
3. Run the installer
4. **IMPORTANT:** ✅ Check "Add Python to PATH"
5. Click "Install Now"
6. Restart Terminal/Command Prompt
7. Verify: `python --version`

#### 2. Install Required Packages

Open Terminal/Command Prompt and run:

```bash
# Navigate to project folder
cd /Users/schalkeanindya/SMFdashboard

# Install dependencies
pip install -r requirements.txt
```

Wait 2-3 minutes for installation to complete.

#### 3. Open the Excel File

**Note:** The `SMFdashboard.xlsm` file is already created and configured!

Simply:
1. Open `SMFdashboard.xlsm` in Excel (it's in the project folder)
2. Enable macros when prompted
3. Dashboard is ready to use

#### 4. Run the Dashboard

1. Open Terminal/Command Prompt
2. Navigate to project folder:
   ```bash
   cd /Users/schalkeanindya/SMFdashboard
   ```
3. Run:
   ```bash
   python SMFdashboard_recipe.py
   ```
4. Excel should open automatically! ✅

**Dashboard will auto-create 5 sheets:**
- `Dashboard` - Main control center
- `Recipe_Config` - Model and variable selection
- `Data_View` - Data preview
- `Backcast_Results` - Performance metrics
- `Forecast_Results` - Future predictions

## 📋 Workflow

### 1. Load Your Data

Click **"Load Data"** button and specify path to your CSV file:
- CSV should have a date column
- Date column will be auto-detected
- Target and exogenous variables populated automatically

**Pre-loaded datasets available:**
- `data/merged/smf_monthly_data.csv`
- `data/merged/smf_quarterly_data.csv`
- `data/merged/smf_weekly_data.csv`
- `data/merged/smf_yearly_data.csv`
- `data/merged/smf_daily_data.csv`
- `data/merged/smf_semesterly_data.csv`

### 2. Configure Settings (in Dashboard)

**Quick Settings** (Editable cells G5-G8):
- **Top N Models:** How many top-performing models to display (default: 3)
- **Use Exog Variables:** Whether to use exogenous features (Yes/No)
- **Forecast Horizons:** Comma-separated list (e.g., "1,3,6,12")
- **Max Forecast Periods:** Maximum steps ahead to forecast (default: 12)

### 3. Select Variables (in Recipe_Config)

**Target Variables** (Columns E-G):
- Check **✓** next to variables you want to forecast
- Set **Horizon** for each (how many periods ahead)

**Exogenous Variables** (Columns I-K):
- Check **✓** next to features to use
- Set **Lags** for each (historical periods to include)

**Models** (Columns A-C):
- Check **✓** next to models you want to test (44 models available!)

### 4. Set Train/Test Dates (in Recipe_Config)

**Training Period:**
- Start: `B58` (e.g., "2005-01-01")
- End: `B59` (e.g., "2019-12-31")

**Testing Period:**
- Start: `B60` (e.g., "2020-01-01")
- End: `B61` (e.g., "2024-12-31")

**Data Frequency:** Auto-detected or set in `B56`

### 5. Run Analysis

Click these buttons in sequence:

1. **"Run Backcast"**
   - Trains models on training data
   - Validates on test data
   - Shows actual vs predicted in `Backcast_Results`
   - Displays RMSE, MAE, R² for each model

2. **"Refresh Charts"**
   - Creates visualization for each selected variable
   - **Left panel:** Backcast (past validation)
   - **Right panel:** Forecast (future predictions)
   - Shows top N models with different colors

3. **"Run Forecast"** (Optional)
   - Generates future predictions
   - Saves detailed results to `Forecast_Results`
   - Shows actual dates for each forecast period

4. **"View Rankings"** (Optional)
   - Consolidated model performance rankings
   - Across all variables and metrics

## 📊 Sheet Descriptions

### Dashboard
- **Main control center**
- Quick settings (Top N, Horizons, Max Periods)
- Workflow buttons
- Parameter inputs
- Status messages

### Recipe_Config
- **Model selection** (Columns A-C)
- **Target variables** (Columns E-G)
- **Exogenous variables** (Columns I-K)
- **Hyperparameters** (Columns E-H, rows 67-110)
- **Train/Test dates** (B58-B62)
- **Data frequency** (B56)

### Data_View
- Displays loaded dataset
- All variables and dates
- Read-only (for viewing)

### Backcast_Results
- **Model Rankings** by variable
- **Performance Metrics:** RMSE, MAE, R²
- **Actual vs Predicted** values for test period

### Forecast_Results
- **Future Predictions** by horizon and model
- **Actual Dates** for each forecast period
- **Last Observed Date** reference

## 🎨 Features

### 1. Flexible Model Selection
- **44 Models Available:** Linear, Ridge, Lasso, RandomForest, GradientBoosting, LSTM, ARIMA, GARCH, and more
- Check **✓** to enable, **✗** to disable
- Visual indicators (green ✓, red ✗)

### 2. Target & Exogenous Variables
- **Target Variables:** Outcomes to forecast
- **Exogenous Variables:** Features to use as inputs
- Set horizons and lags independently
- Visual selection with checkmarks

### 3. Date-Based Train/Test Split
- Specify exact date ranges
- Training on historical period
- Testing on recent period
- Validates model performance on unseen data

### 4. Multi-Horizon Forecasting
- Customize horizons (e.g., 1, 3, 6, 12 periods ahead)
- Different forecast lengths
- Recursive multi-step prediction

### 5. Dynamic Charts
- **Backcast:** Actual vs Predicted on test data
- **Forecast:** Future predictions with historical context
- Red vertical line marks forecast start
- Color-coded by model (top N)
- Automatic spacing based on number of variables

### 6. Model Comparison
- RMSE (Root Mean Squared Error) - lower is better
- MAE (Mean Absolute Error) - lower is better
- R² (Coefficient of Determination) - higher is better

## 📁 Project Structure

```
SMFdashboard/
├── SMFdashboard_recipe.py      # Main Python code
├── SMFdashboard.xlsm             # Excel dashboard
├── requirements.txt            # Dependencies
├── README.md                    # This file
├── VBA_CODE_RECIPE_V2.txt      # VBA macros
├── data/
│   ├── merged/                 # Pre-processed datasets
│   │   ├── smf_monthly_data.csv
│   │   ├── smf_quarterly_data.csv
│   │   ├── smf_weekly_data.csv
│   │   ├── smf_yearly_data.csv
│   │   ├── smf_daily_data.csv
│   │   └── smf_semesterly_data.csv
│   ├── SMF_Datasets_Y_Vars.xlsx
│   └── SMF_Datasets_X_Vars.xlsx
├── src/
│   ├── core/                   # Core modules
│   │   ├── base.py            # BaseModel interface
│   │   ├── registry.py        # Model discovery
│   │   └── ...
│   └── models/                 # Model implementations
│       ├── linear/
│       ├── random_forest/
│       ├── lstm/
│       └── ... (40+ models)
└── custom_recipes/              # Saved recipe configs
    └── ...
```

## 🔧 Available Models

### Linear Models
- Linear Regression
- Ridge
- Lasso
- Elastic Net
- Huber Regression
- PLS1
- StandardizedLinear
- StandardizedRidge

### Tree-Based Models
- Decision Tree
- Random Forest
- Extra Trees
- Gradient Boosting
- Stochastic Gradient Boosting
- XGBoost
- Bagging

### Neural Networks
- LSTM
- Neural Network

### Time Series Models
- AR1
- ARp (AR with p lags)
- ARIMA
- SARIMAX
- GARCH
- NeuroGARCH
- VAR (Vector Autoregression)
- TVP (Time-Varying Parameter)
- DFM (Dynamic Factor Model)
- DFM2
- DNS (Diebold-Li)

### Econometric Models
- BVAR (Bayesian VAR)
- MIDAS

### Simple Benchmark Models
- Naive (Last value)
- Seasonal Naive
- Drift

### Other
- KNN
- Quantile Regression
- PCA

## 💡 Tips

1. **Start with Default Settings**
   - Load a pre-merged dataset
   - Use 3-5 target variables
   - Select 5-10 models
   - Set horizons to "1,3,6"

2. **Check Data Quality**
   - View `Data_View` sheet to inspect your data
   - Look for missing values
   - Check date column format

3. **Iterate on Models**
   - Start with simple models (Linear, Ridge, RandomForest)
   - Compare performance in backcast results
   - Add complex models (LSTM, GARCH) if needed

4. **Adjust Horizons**
   - Short-term: "1,3" periods
   - Medium-term: "3,6,12" periods
   - Long-term: "6,12,24" periods

5. **Save Recipes**
   - Configure once
   - Click "Save Custom Recipe" in `Recipe_Config`
   - Reuse for different datasets

## 🐛 Troubleshooting

**"Connection Failed" Error:**
- Ensure Python is running
- Check `xlwings` add-in is enabled
- Try: `python -c "import xlwings; xlwings.view(1)"`

**Charts Don't Appear:**
- Run "Refresh Charts" after "Run Backcast"
- Check if models are selected (✓ in Recipe_Config)
- Verify data is loaded in `Data_View`

**Python Path Issues:**
- Update xlwings add-in settings
- Tools → References → xlwings

**Models Not Training:**
- Check if enough data (min 12 periods)
- Verify date column exists
- Ensure train/test dates are valid

## 📝 Notes

- **Custom Model Library:** Models are in `src/models/` following a modular `BaseModel` interface
- **Recipe System:** Save and reuse configurations as JSON files
- **Frequency Detection:** Automatic detection of Daily, Weekly, Monthly, Quarterly, Yearly
- **Excel Integration:** Full bidirectional Python ↔ Excel communication via xlwings

## 📞 Support

For issues or questions:
1. Check `docs/_old_docs/` for implementation notes
2. Review model configurations in `src/models/`
3. Inspect data processing in `data/merged/`

## 📄 License

Internal use only.

---

**Version:** 4.0
**Last Updated:** January 2025