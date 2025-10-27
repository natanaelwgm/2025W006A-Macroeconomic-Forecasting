# Getting Started with SMF Dashboard

## For Users 👥

This dashboard enables macroeconomic forecasting with 45+ machine learning models through an Excel interface.

### What It Does
- **Forecasts** future economic indicators (GDP, inflation, employment, etc.)
- **Validates** model performance on historical data (backcast)
- **Compares** multiple models side-by-side
- **Visualizes** results with interactive charts
- **Supports** multiple frequencies (daily, weekly, monthly, quarterly, yearly)

### Key Features
✅ Excel-based interface (no coding needed!)  
✅ 45+ forecasting models (Linear, Tree, Neural Networks, GARCH, etc.)  
✅ Automatic model comparison (shows best performers)  
✅ Date-based train/test splits  
✅ Multi-horizon forecasting (1, 3, 6, 12 periods ahead)  
✅ Pre-loaded datasets for quick start  

## Installation (Step-by-Step for Beginners)

### Step 1: Install Python

**If you don't have Python installed yet:**

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.x" (latest version)
   - Run the installer

2. **During Installation:**
   - ✅ CHECK "Add Python to PATH" (important!)
   - Click "Install Now"

3. **Verify Installation:**
   - Open Terminal (Mac) or Command Prompt (Windows)
   - Type: `python --version`
   - Should show: "Python 3.x.x"

### Step 2: Install Dependencies

1. **Open Terminal/Command Prompt**

2. **Navigate to project folder:**
   ```bash
   cd /Users/schalkeanindya/SMFdashboard
   ```
   
   (Windows users: Use `cd C:\Users\YourName\SMFdashboard`)

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Wait for installation to complete** (~2-3 minutes)

### Step 3: Open the Excel File

**Note:** The `SMFdashboard.xlsm` file is already created and configured!

Simply:
1. Open `SMFdashboard.xlsm` in Excel (it's in the project folder)
2. Enable macros when prompted
3. Dashboard is ready to use

### Step 4: Run the Dashboard

1. **Open Terminal/Command Prompt**
   - Navigate to project folder:
     ```bash
     cd /Users/schalkeanindya/SMFdashboard
     ```

2. **Run Python script:**
   ```bash
   python SMFdashboard_recipe.py
   ```

3. **Dashboard should open in Excel!** ✅

## Quick Demo (2 Minutes)

1. **Open Excel:** `SMFdashboard.xlsm`
2. **Click "Load Data":** Uses default monthly dataset
3. **Select 3 variables:** In Recipe_Config sheet
4. **Click "Run Backcast":** See model performance
5. **Click "Refresh Charts":** See visualizations

**Done!** You now have forecasts for 3 economic indicators.

## Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete technical documentation |
| `QUICK_START.md` | 5-minute getting started guide |
| `SETUP_VBA.md` | VBA macros setup instructions |
| `PROJECT_STRUCTURE.txt` | Folder organization overview |

## What You'll See

### Dashboard Sheet
- Quick settings panel
- Workflow buttons (Load, Backcast, Forecast, Charts)
- Status messages
- Interactive parameter controls

### Recipe_Config Sheet
- Model selection (✓/✗ checkboxes)
- Target variable selection
- Exogenous variable selection
- Hyperparameter settings
- Train/test date configuration

### Backcast_Results Sheet
- Model rankings by variable
- Performance metrics (RMSE, MAE, R²)
- Actual vs Predicted values

### Charts on Dashboard
- **Left panel:** Backcast validation (past)
- **Right panel:** Forecast predictions (future)
- Color-coded by model
- Shows top N performers

### Forecast_Results Sheet
- Future predictions by horizon
- Actual dates for each period
- Multi-horizon forecasts (1, 3, 6, 12 steps ahead)

## Customization Options

### Change Forecast Horizons
**Dashboard → Cell G7**
- Default: `1,3,6,12`
- Short-term: `1,3`
- Long-term: `6,12,24`

### Change Max Forecast Periods
**Dashboard → Cell G8**
- Default: `12`
- Short-term: `6`
- Long-term: `24`

### Select Different Models
**Recipe_Config → Columns A-C**
- Check ✓ to enable
- Uncheck ✗ to disable
- 44 models available

### Use Different Data
**Dashboard → Click "Load Data"**
- Enter path to your CSV
- Or use pre-loaded datasets in `data/merged/`

## Data Files Included

- `smf_monthly_data.csv` - 6,048 observations, 167 variables
- `smf_quarterly_data.csv` - 1,832 observations, 159 variables
- `smf_weekly_data.csv` - 1,728 observations, 123 variables
- `smf_yearly_data.csv` - 524 observations, 108 variables
- `smf_daily_data.csv` - 26,288 observations, 6 variables
- `smf_semesterly_data.csv` - 918 observations, aggregated

## Technical Details

- **Framework:** xlwings (Excel ↔ Python bridge)
- **Models:** Custom library with BaseModel interface
- **Forecasting:** Multi-step recursive prediction with lagged features
- **Validation:** Date-based train/test splits
- **Architecture:** Modular, extensible design

## Support & Troubleshooting

See `README.md` section "🐛 Troubleshooting" for:
- Connection errors
- Chart display issues
- Model training problems
- Python path configuration

## Next Steps

1. **Experiment:** Try different models and horizons
2. **Compare:** Use multiple frequencies (monthly vs quarterly)
3. **Extend:** Add your own models in `src/models/`
4. **Save:** Save custom recipes for reuse

---

**Ready to start forecasting?** Open `QUICK_START.md`! 🚀
