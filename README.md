# Indonesia Macroeconomic Forecasting Framework

A comprehensive forecasting framework for Indonesian macroeconomic indicators with both command-line Python tools and an interactive Excel dashboard.

## 📁 Repository Structure

This repository contains two main components:

### 1. Command-Line Forecasting System (Root Level)
- **Python Scripts:** `run.py`, `run_v2.py`, `run_multi_targets.py` - Scripts for batch forecasting
- **Reports:** `report_v3.py`, `report_multi_targets_v2.py` - Report generation scripts
- **Recipes:** Configuration files in `recipes/` for different forecast scenarios
- **Outputs:** Results stored in `outputs/` directory
- **Data:** Processed data in `data/processed/`

### 2. Excel Dashboard System (`SMFDashboard/` folder)
- **Interactive Excel Interface** - `SMFDashboard/SMFdashboard.xlsm`
- **Python Scripts** - `SMFDashboard/SMFdashboard_recipe.py`
- **Model Library** - 40+ forecasting models in `SMFDashboard/src/models/`
- **Data Files** - Pre-processed datasets in `SMFDashboard/data/merged/`
- **Custom Recipes** - Saved configurations in `SMFDashboard/custom_recipes/`

## 🚀 Quick Start

### Option A: Using the Excel Dashboard (Recommended for Interactive Use)

Navigate to the SMFDashboard folder:

```bash
cd SMFDashboard
```

Follow the instructions in `SMFDashboard/README.md` for Excel dashboard setup.

### Option B: Using Command-Line Tools

For batch processing and automated forecasting:

```bash
# Install dependencies
pip install -r requirements.txt

# Run single target forecast
python3 run_v2.py recipes/test_quick.json --all

# Run multi-target forecast
python3 run_multi_targets.py recipes/recipe_multi_all_valid_y.json --verbose
```

## 🎯 Features

- **45+ Forecasting Models:** Linear, Ridge, Lasso, RandomForest, GradientBoosting, XGBoost, LSTM, ARIMA, GARCH, and more
- **Multiple Frequencies:** Daily, Weekly, Monthly, Quarterly, Semesterly, Yearly
- **Interactive Dashboard:** Excel-based interface with real-time charts
- **Batch Processing:** Command-line tools for automated forecasts
- **Comprehensive Reporting:** Enhanced reports with visualizations

## 📊 Project Structure

```
.
├── SMFDashboard/              # Excel Dashboard System
│   ├── SMFdashboard.xlsm     # Main Excel file
│   ├── src/                   # Model implementations
│   ├── data/                  # Data files
│   ├── custom_recipes/        # Saved configurations
│   └── docs/                  # Documentation
├── recipes/                   # Command-line recipe configs
├── outputs/                   # Forecast results
├── data/processed/            # Processed data files
├── run_v2.py                  # Main forecast script
├── report_multi_targets_v2.py # Report generator
└── requirements.txt           # Python dependencies
```

## 📖 Documentation

- **Excel Dashboard Guide:** See `SMFDashboard/README.md`
- **Command-Line Guide:** See `README_INTERNAL.md`
- **Reports Index:** See `REPORTS_INDEX.md`

## 🔧 Requirements

See `requirements.txt` for Python package dependencies.

## 📝 License

Internal use only.
