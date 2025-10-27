# Quick Start Guide 🚀

Get started with SMF Dashboard in 5 minutes!

## Prerequisites for First-Time Users

### Do you have Python installed?

**Check if Python is installed:**
1. Open Terminal (Mac) or Command Prompt (Windows)
2. Type: `python --version`
3. If you see "Python 3.x.x" → **You're good!** ✅
4. If you see "command not found" → **Install Python first!** (see below)

**If you need to install Python:**
1. Go to https://www.python.org/downloads/
2. Download the latest version
3. Run the installer
4. **IMPORTANT:** Check "Add Python to PATH" during installation
5. Restart Terminal/Command Prompt
6. Verify: `python --version`

### Install Python Packages

1. **Open Terminal/Command Prompt**

2. **Navigate to project folder:**
   ```bash
   cd /Users/schalkeanindya/SMFdashboard
   ```
   (Windows: `cd C:\Users\YourName\SMFdashboard`)

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Wait 2-3 minutes** for installation

### Excel File Setup

**Note:** The `SMFdashboard.xlsm` file is already created and configured!

All you need to do:
- Open `SMFdashboard.xlsm` in Excel
- Enable macros when prompted
- Dashboard is ready to use

## Step 1: Open Excel

1. Open `SMFdashboard.xlsm`
2. Enable macros when prompted
3. Click "Yes" to trust the workbook

## Step 2: Run Python

1. **Open Terminal/Command Prompt**

2. **Navigate to project folder:**
   ```bash
   cd /Users/schalkeanindya/SMFdashboard
   ```

3. **Run the dashboard:**
   ```bash
   python SMFdashboard_recipe.py
   ```

You should see:
```
✅ Loaded 25 custom models: [...]
✅ Dashboard setup complete!
```

4. **Excel should open automatically!** ✅

## Step 3: Load Data

In the Dashboard, click **"Load Data"** button.

**Option A:** Use pre-loaded data
- Keep default path: `/Users/schalkeanindya/SMFdashboard/data/merged/smf_monthly_data.csv`

**Option B:** Use your own data
- Enter path to your CSV file
- Make sure it has a date column

## Step 4: Configure

### In Dashboard (Quick Settings):
- **G5:** Top N Models = `3` (shows top 3 models)
- **G7:** Forecast Horizons = `1,3,6` (short-term forecasts)
- **G8:** Max Periods = `12` (how far ahead)

### In Recipe_Config:
1. **Select Target Variables** (Columns E-G)
   - Check ✓ next to 3-5 variables you want to forecast
   - Set horizon to `1` (1 period ahead)

2. **Select Models** (Columns A-C)
   - Check ✓ next to 5-10 models:
     - ✓ Linear
     - ✓ Ridge
     - ✓ RandomForest
     - ✓ Naive
     - ✓ SeasonalNaive

3. **Set Train/Test Dates** (B58-B62)
   - Training Start: `2005-01-01`
   - Training End: `2019-12-31`
   - Test Start: `2020-01-01`
   - Test End: `2024-12-31`

## Step 5: Run!

Click buttons in this order:

1. **"Run Backcast"** → Wait for completion
2. **"Refresh Charts"** → See visualizations
3. **"Run Forecast"** → See future predictions

## ✅ Success!

You should now see:
- **Backcast_Results sheet:** Model performance metrics
- **Dashboard:** Charts showing actual vs predicted + future forecasts
- **Forecast_Results sheet:** Detailed future predictions

---

## Need Help?

- **Charts don't show:** Make sure "Run Backcast" completed first
- **No models training:** Check if you selected models (✓ in Recipe_Config)
- **Wrong data:** Verify your CSV has a date column

## Next Steps

1. **Experiment with different models:** Try LSTM, GARCH, NeuralNetwork
2. **Adjust horizons:** Change G7 to "1,3,6,12,24" for longer forecasts
3. **Select more variables:** Add more ✓ in Recipe_Config
4. **Save recipe:** Click "Save Custom Recipe" in Recipe_Config to reuse settings

---

**That's it! You're ready to forecast.** 🎉
