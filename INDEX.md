# SMF Dashboard - File Index 📑

## 🚀 Start Here - Navigation Guide

| File | Purpose | Audience | When to Use |
|------|---------|----------|-------------|
| **START_HERE.txt** | Decision tree for which file to open | All users | First file to read! |
| **QUICK_START.md** | 5-minute getting started | Beginners | Never used Python? |
| **GETTING_STARTED.md** | Project overview | Python users | Already have Python? |
| **README.md** | Complete technical docs | All users | Need full reference? |
| **PROJECT_SUMMARY.txt** | Quick overview | Stakeholders | Share with team |
| **SETUP_VBA.md** | Excel macros setup | All users | Setting up buttons |

## 📂 Project Organization

### Core Files
- `SMFdashboard_recipe.py` - Main Python application
- `SMFdashboard.xlsm` - Excel dashboard (create from scratch or template)
- `VBA_CODE_RECIPE_V2.txt` - VBA macros code
- `requirements.txt` - Python dependencies
- `PROJECT_STRUCTURE.txt` - Folder organization

### Data Files
- `data/merged/*.csv` - Pre-processed datasets (CSV)
- `data/merged/*.xlsx` - Pre-processed datasets (Excel)
- `data/merged/SMF_All_Frequencies.xlsx` - Master Excel file (all frequencies)

### Source Code
- `src/core/` - Core modules (BaseModel, registry, etc.)
- `src/models/` - 40+ model implementations
  - Linear, Ridge, Lasso
  - Random Forest, Gradient Boosting
  - LSTM, Neural Networks
  - ARIMA, GARCH, VAR, etc.

### Documentation
- `docs/_old_docs/` - Archive of old documentation
- `old_scripts/` - Utility scripts (not for end users)

### Configurations
- `custom_recipes/` - Saved recipe JSON files

## 📖 Documentation Guide

### For New Users
1. Read **QUICK_START.md** (5 min)
2. Follow setup in **SETUP_VBA.md**
3. Run Python script
4. Click "Load Data" → Select variables → Run

### For New Users/Stakeholders
1. Read **GETTING_STARTED.md** or **FOR_YOUR_BOSS.txt**
2. See "What It Does" section
3. View included data summary
4. See workflow overview

### For Technical Users
1. Read **README.md** (complete reference)
2. Check `src/models/` for model implementations
3. Review `src/core/` for architecture
4. Customize hyperparameters in Recipe_Config

## 🎯 Quick Reference

### Installation
```bash
pip install -r requirements.txt
```

### Run
```bash
python SMFdashboard_recipe.py
```

### Excel Setup
- Open `SMFdashboard.xlsm`
- Add VBA from `VBA_CODE_RECIPE_V2.txt`
- See **SETUP_VBA.md** for details

### Data Paths
Default data: `/Users/schalkeanindya/SMFdashboard/data/merged/smf_monthly_data.csv`

Or use:
- `smf_quarterly_data.csv`
- `smf_weekly_data.csv`
- `smf_yearly_data.csv`
- `smf_daily_data.csv`
- `smf_semesterly_data.csv`

## 📊 What's Included

### Models (45+)
- Linear, Ridge, Lasso, Elastic Net
- Random Forest, Extra Trees
- Gradient Boosting, Stochastic GB
- LSTM, Neural Networks
- ARIMA, AR1, ARp, SARIMAX
- GARCH, NeuroGARCH
- VAR, BVAR, TVP
- DFM, DFM2, DNS
- Naive, Seasonal Naive, Drift
- KNN, PLS1, PCA
- Quantile Regression

### Features
- Excel-based interface
- Model comparison
- Multi-horizon forecasting
- Backcast validation
- Visual charts
- Date-based train/test splits
- Custom hyperparameters

### Data
- 6 merged datasets (all frequencies)
- 500+ economic variables
- 50,000+ observations total
- Ready-to-use CSVs and Excel files

## 🔗 Related Files

### To Understand the Code
- `SMFdashboard_recipe.py` lines 1-100 → Setup functions
- `SMFdashboard_recipe.py` lines 700-900 → Backcast logic
- `SMFdashboard_recipe.py` lines 1000-1300 → Forecast logic
- `SMFdashboard_recipe.py` lines 1867-2200 → Chart generation

### To Customize Models
- `src/models/*/model.py` → Individual model implementations
- `src/core/base.py` → BaseModel interface
- `src/core/registry.py` → Model discovery

### To Add Data
- `data/merged/README.md` → Data structure guide
- `data/merge_datasets_v2.py` → Merging script

## 📝 File Descriptions

| File | Lines | Description |
|------|-------|-------------|
| `SMFdashboard_recipe.py` | ~2,300 | Main application code |
| `README.md` | ~600 | Full documentation |
| `QUICK_START.md` | ~100 | Getting started guide |
| `GETTING_STARTED.md` | ~200 | Executive overview |
| `SETUP_VBA.md` | ~100 | VBA setup instructions |
| `FOR_YOUR_BOSS.txt` | ~60 | Executive summary |

## 🎨 Dashboard Sheets

1. **Dashboard** - Main control center
2. **Recipe_Config** - Model/variable selection
3. **Data_View** - Data preview
4. **Backcast_Results** - Model performance
5. **Forecast_Results** - Future predictions

## ✅ Ready for Sharing

- ✅ Clean folder structure
- ✅ Comprehensive documentation
- ✅ Easy-to-follow guides
- ✅ Pre-loaded data
- ✅ Professional presentation
- ✅ Executive summary
- ✅ Technical details

---

**Start with:** QUICK_START.md (5 min)  
**Show to stakeholders:** GETTING_STARTED.md (2 min)  
**Full reference:** README.md (30 min)
