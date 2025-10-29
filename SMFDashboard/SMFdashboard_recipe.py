import xlwings as xw
import numpy as np
import pandas as pd
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import warnings
warnings.filterwarnings('ignore')

# Add src to path for custom model library
SRC_DIR = Path(__file__).parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# Import model registry
from core.registry import discover_plugins
from core.base import BaseModel

# Discover all available models
MODEL_REGISTRY = discover_plugins('models')
print(f"✅ Loaded {len(MODEL_REGISTRY)} custom models: {list(MODEL_REGISTRY.keys())}")

# Recipe system paths
RECIPE_DIR = Path("/Users/schalkeanindya/Downloads/2025W006A-Macroeconomic-Forecasting-717308800511ac4d480202e2cce3cee4167c7384/recipes")
DATA_DIR = Path("/Users/schalkeanindya/Downloads/2025W006A-Macroeconomic-Forecasting-717308800511ac4d480202e2cce3cee4167c7384/data/processed")


# Model name mapping (Dashboard names -> Registry names)
MODEL_NAME_MAP = {
    'Naive': 'Naive',
    'SeasonalNaive': 'SeasonalNaive',
    'Drift': 'Drift',  # If not in registry, will be handled gracefully
    'Linear': 'Linear',
    'StandardizedLinear': 'StandardizedLinear',
    'Ridge': 'Ridge',
    'StandardizedRidge': 'StandardizedRidge',
    'Lasso': 'Lasso',
    'ElasticNet': 'ElasticNet',
    'ElasticNetGrid': 'ElasticNetGrid',
    'Huber': 'Huber',
    'PLS1': 'PLS1',
    'AR1': 'AR1',
    'ARp': 'ARp',
    'TVP': 'TVP',  # May not be available
    'BVAR': 'BVAR',
    'RandomForest': 'RandomForest',
    'ExtraTrees': 'ExtraTrees',
    'GradientBoosting': 'GradientBoosting',
    'StochasticGB': 'StochasticGB',
    'DecisionTree': 'Tree',
    'DFM': 'DFM',
    'DFM2': 'DFM2',
    'GARCH': 'GARCH',
    'NeuroGARCH': 'NeuroGARCH',  # May not be available
    'DNS': 'DNS',  # May not be available
    'MIDAS': 'MIDAS',  # May not be available
    'LSTM': 'LSTM',
    'ARIMA': 'ARIMA',  # May not be available
    'XGBoost': 'XGBoost',
    'Bagging': 'Bagging',
}


def create_model(model_name: str, params: dict = None) -> BaseModel:
    """
    Create a model instance from the registry
    
    Args:
        model_name: Model name from dashboard (e.g., 'Linear', 'RandomForest')
        params: Optional model parameters
    
    Returns:
        BaseModel instance or None if model not available
    """
    # Map dashboard name to registry name
    registry_name = MODEL_NAME_MAP.get(model_name, model_name)
    
    # Get model from registry
    if registry_name not in MODEL_REGISTRY:
        print(f"⚠️  Model '{model_name}' (registry: '{registry_name}') not available in MODEL_REGISTRY")
        print(f"   Available models: {sorted(MODEL_REGISTRY.keys())}")
        return None
    
    try:
        create_fn, spec = MODEL_REGISTRY[registry_name]
        
        # Create model with parameters
        model = create_fn(params or {})
        
        return model
    except Exception as e:
        print(f"⚠️  Error creating model '{model_name}': {e}")
        return None


def generate_dummy_recipe_data():
    """Generate dummy data matching recipe variable names"""
    wb = xw.Book.caller()
    data_view = wb.sheets['Data_View']
    dash = wb.sheets['Dashboard']
    
    data_view.clear()
    dash.range('B33').value = "⏳ Generating dummy data matching recipe format..."
    
    # Generate time series (same as real data: 2005-2025)
    np.random.seed(42)
    periods = 246  # ~20 years of monthly data
    start_date = datetime(2005, 1, 31)
    dates = pd.date_range(start=start_date, periods=periods, freq='M')
    
    # Generate variables matching recipe names
    trend = np.linspace(100, 145, periods)
    seasonal = 10 * np.sin(np.linspace(0, 20*np.pi, periods))
    
    # 1. CPI (Consumer Price Index) - base 100
    cpi = trend + seasonal + np.random.normal(0, 3, periods)
    
    # 2. Real GDP Growth (%) - 4-6% range
    gdp_growth = 5 + 0.5*np.sin(np.linspace(0, 15*np.pi, periods)) + np.random.normal(0, 0.8, periods)
    
    # 3. BI7DRR (Bank Indonesia rate) - 3-7%
    bi7drr = 5 + 1.5*np.sin(np.linspace(0, 12*np.pi, periods)) + np.random.normal(0, 0.3, periods)
    
    # 4-7. Deposit Rates (slightly higher than BI7DRR)
    deposit_1m = bi7drr + 0.5 + np.random.normal(0, 0.2, periods)
    deposit_3m = bi7drr + 0.8 + np.random.normal(0, 0.2, periods)
    deposit_6m = bi7drr + 1.0 + np.random.normal(0, 0.2, periods)
    deposit_12m = bi7drr + 1.2 + np.random.normal(0, 0.2, periods)
    
    # 8. Government Bond Yield 10 Year - 6-9%
    govt_bond_10yr = bi7drr + 2 + np.random.normal(0, 0.4, periods)
    
    # 9. JISDOR Exchange Rate - 13000-16000 IDR/USD
    jisdor = 14500 + 1000*np.sin(np.linspace(0, 18*np.pi, periods)) + np.random.normal(0, 200, periods)
    
    # 10. FX (USD/IDR) - similar to JISDOR
    fx = jisdor + np.random.normal(0, 50, periods)
    
    # Create DataFrame with exact recipe column names
    df = pd.DataFrame({
        'date': dates,
        'CPI': cpi,
        'Real GDP Growth': gdp_growth,
        'BI7DRR': bi7drr,
        'Deposit Rate 1M': deposit_1m,
        'Deposit Rate 3M': deposit_3m,
        'Deposit Rate 6M': deposit_6m,
        'Deposit Rate 12M': deposit_12m,
        'Govt Bond Yield 10 Yr': govt_bond_10yr,
        'JISDOR Exchange Rate': jisdor,
        'FX': fx
    })
    
    # Write to Data_View sheet
    data_view.range('A1').value = "📊 DUMMY DATA - For Testing"
    data_view.range('A1').font.bold = True
    data_view.range('A1').font.size = 14
    data_view.range('A1').color = (255, 200, 100)
    
    data_view.range('A3').value = df
    data_view.range('A3:G3').font.bold = True
    data_view.range('A3:G3').color = (70, 130, 180)
    data_view.range('A3:G3').font.color = (255, 255, 255)
    
    try:
        data_view.range('A3').expand().columns.autofit()
    except:
        pass
    
    # Summary
    data_view.range('M1').value = "📋 Data Summary"
    data_view.range('M1').font.bold = True
    data_view.range('M2').value = [
        ['Records:', len(df)],
        ['Variables:', 10],
        ['Start:', str(df['date'].min())[:10]],
        ['End:', str(df['date'].max())[:10]],
        ['', ''],
        ['Variables (Recipe Format):', ''],
        ['• CPI', ''],
        ['• Real GDP Growth', ''],
        ['• BI7DRR', ''],
        ['• Deposit Rate 1M', ''],
        ['• Deposit Rate 3M', ''],
        ['• Deposit Rate 6M', ''],
        ['• Deposit Rate 12M', ''],
        ['• Govt Bond Yield 10 Yr', ''],
        ['• JISDOR Exchange Rate', ''],
        ['• FX', '']
    ]
    
    dash.range('B33').value = f"✅ Generated {periods} months × 10 variables (recipe format)"
    data_view.activate()
    
    return f"✅ Generated dummy data matching recipes"


def setup_recipe_dashboard():
    """Initialize the recipe-based dashboard structure"""
    wb = xw.Book.caller()
    
    # Get existing sheet names
    existing_sheets = [s.name for s in wb.sheets]
    
    # Create or get sheets (added Forecast_Results back for forecasts)
    sheet_names = ['Dashboard', 'Recipe_Config', 'Data_View', 
                   'Backcast_Results', 'Forecast_Results', 'Model_Rankings']
    for name in sheet_names:
        if name not in existing_sheets:
            wb.sheets.add(name, after=wb.sheets[-1])
    
    # Setup Dashboard - Main Control Panel
    dash = wb.sheets['Dashboard']
    dash.clear()
    dash.range('A1').value = "🎯 SMF RECIPE-BASED FORECASTING DASHBOARD"
    dash.range('A1').font.size = 20
    dash.range('A1').font.bold = True
    dash.range('A1:P1').merge()
    dash.range('A1').api.HorizontalAlignment = -4108  # Center
    dash.range('A1').color = (70, 130, 180)
    dash.range('A1').font.color = (255, 255, 255)
    
    # ========== LEFT SIDE: BEGINNER SECTION ==========
    
    # Dashboard Description Panel (Left)
    dash.range('A3').value = "📋 DASHBOARD OVERVIEW"
    dash.range('A3').font.bold = True
    dash.range('A3').font.size = 14
    dash.range('A3:J3').merge()
    dash.range('A3').color = (220, 220, 220)

    dash.range('A4').value = "This dashboard lets you configure, validate, and compare forecasting models using recipe-based settings."
    dash.range('A4:J4').merge()
    dash.range('A4').font.size = 11
    dash.range('A4').wrap_text = True
    
    dash.range('A6').value = "💡 Tip: Go to Recipe_Config to name & save recipes"
    dash.range('A6').font.italic = True
    dash.range('A6').font.size = 9
    dash.range('A6:J6').merge()
    dash.range('A6').color = (255, 255, 230)
    
    # ========== HORIZONTAL LAYOUT: Quick Settings + Best Models Side by Side ==========
    
    # FORECAST QUICK SETTINGS Panel (Left columns A-E)
    dash.range('A8').value = "⚡ FORECAST QUICK SETTINGS"
    dash.range('A8').font.bold = True
    dash.range('A8').font.size = 12
    dash.range('A8:E8').merge()
    dash.range('A8').color = (100, 200, 100)  # Green for beginner section
    dash.range('A8').font.color = (255, 255, 255)
    
    dash.range('A9').value = [
        ['Parameter', 'Value'],
        ['Top N Models', 3],
        ['Forecast Horizons', '1,3,6,12'],
        ['Max Forecast Periods', 12]
    ]
    dash.range('A9:B12').columns.autofit()
    dash.range('A9:B9').font.bold = True
    dash.range('A9:B9').color = (200, 255, 200)
    
    # Make values editable
    dash.range('B10:B12').color = (255, 255, 200)
    
    # 🏆 SHOW BEST MODELS FOR Panel (shifted left to start at column D, span D-I)
    dash.range('D8').value = "🏆 SHOW BEST MODELS FOR"
    dash.range('D8').font.bold = True
    dash.range('D8').font.size = 12
    dash.range('D8:I8').merge()
    dash.range('D8').color = (100, 200, 100)
    dash.range('D8').font.color = (255, 255, 255)
    
    # Variables and Frequencies side by side
    # Variables now in columns D-E (starting row 9)
    dash.range('D9').value = "Variables"
    dash.range('D9').font.bold = True
    dash.range('D9:E9').merge()
    dash.range('D9').color = (200, 255, 200)
    
    # Variables checklist header
    dash.range('D10').value = [['✓', 'Variable']]
    dash.range('D10:E10').font.bold = True
    dash.range('D10:E10').color = (230, 255, 230)
    
    # Pre-populated economic variables
    variables = [
        'Real GDP Growth', 'BI7DRR', 'Deposit Rate 1M',
        'Deposit Rate 3M', 'Deposit Rate 6M', 'Deposit Rate 12M',
        'CPI', 'JISDOR Exchange Rate', 'Informal Employment'
    ]
    
    # Populate variable checkboxes (columns D-E)
    for i, var in enumerate(variables):
        row = 11 + i
        # Checkbox column (unchecked by default)
        dash.range(f'D{row}').value = '✗'
        dash.range(f'D{row}').api.HorizontalAlignment = -4108  # Center
        dash.range(f'D{row}').font.bold = True
        dash.range(f'D{row}').color = (255, 200, 200)
        
        # Add data validation for checkbox (✓ or ✗)
        try:
            dash.range(f'D{row}').api.Validation.Delete()
            dash.range(f'D{row}').api.Validation.Add(
                Type=3,  # xlValidateList
                AlertStyle=1,
                Formula1='✓,✗'
            )
        except:
            pass
        
        # Variable name column
        dash.range(f'E{row}').value = var
        dash.range(f'E{row}').color = (255, 255, 240)
    
    # Frequencies now in columns F-G (starting row 9)
    dash.range('F9').value = "Frequencies"
    dash.range('F9').font.bold = True
    dash.range('F9:G9').merge()
    dash.range('F9').color = (200, 255, 200)
    
    # Frequencies checklist header
    dash.range('F10').value = [['✓', 'Frequency']]
    dash.range('F10:G10').font.bold = True
    dash.range('F10:G10').color = (230, 255, 230)
    
    # Unique frequencies
    frequencies = ['monthly', 'quarterly', 'semesterly', 'yearly', 'weekly']
    
    # Populate frequency checkboxes (columns F-G)
    for i, freq in enumerate(frequencies):
        row = 11 + i
        # Checkbox column (monthly checked, others unchecked)
        if i == 0:  # monthly
            dash.range(f'F{row}').value = '✓'
            dash.range(f'F{row}').color = (200, 255, 200)
        else:
            dash.range(f'F{row}').value = '✗'
            dash.range(f'F{row}').color = (255, 200, 200)
        
        dash.range(f'F{row}').api.HorizontalAlignment = -4108  # Center
        dash.range(f'F{row}').font.bold = True
        
        # Add data validation for checkbox (✓ or ✗)
        try:
            dash.range(f'F{row}').api.Validation.Delete()
            dash.range(f'F{row}').api.Validation.Add(
                Type=3,  # xlValidateList
                AlertStyle=1,
                Formula1='✓,✗'
            )
        except:
            pass
        
        # Frequency name column
        dash.range(f'G{row}').value = freq
        dash.range(f'G{row}').color = (255, 255, 240)
    
    # Quick Actions for Beginners (row 22)
    dash.range('A22').value = "🚀 QUICK ACTIONS FOR BEGINNERS"
    dash.range('A22').font.bold = True
    dash.range('A22').font.size = 12
    dash.range('A22:K22').merge()
    dash.range('A22').color = (220, 220, 220)
    
    beginner_steps = [
        ['1', 'Set Quick Settings', 'Adjust Top N, Horizons, Max Periods (left)'],
        ['2', 'Choose Variables', 'Check variables you want to forecast (columns F-G)'],
        ['3', 'Choose Frequency', 'Check frequencies (columns H-I)'],
        ['4', 'Show Best Models', 'View which models perform best'],
        ['5', 'Run Forecast', 'Generate future predictions'],
        ['6', 'Refresh Charts', 'View visualizations'],
        ['7', 'Clear Results', 'Start over with new settings']
    ]
    
    dash.range('A23').value = beginner_steps
    dash.range('A23:C23').font.bold = True
    dash.range('A23:C23').color = (230, 230, 230)
    dash.range('A23:C29').columns.autofit()
    
    # ========== POWER USER / CUSTOM BACKCAST SECTION (Right Side) ==========
    
    # Custom Backcast header (shifted left: columns K-N, starting row 8)
    dash.range('K8').value = "⚙️ POWER USER / CUSTOM BACKCAST"
    dash.range('K8').font.bold = True
    dash.range('K8').font.size = 12
    dash.range('K8:N8').merge()
    dash.range('K8').color = (200, 100, 100)  # Red/orange for power user
    dash.range('K8').font.color = (255, 255, 255)
    
    # Action buttons and instructions (compact)
    dash.range('K9').value = "Actions:"
    dash.range('K9').font.bold = True
    dash.range('K9').font.size = 11
    
    action_buttons = [
        ['•', 'Configure Models'],
        ['•', 'Run Backcast'],
        ['•', 'View Rankings'],
        ['•', 'Run Forecast'],
        ['•', 'Refresh Charts'],
        ['•', 'Clear Results']
    ]
    
    dash.range('K10').value = action_buttons
    dash.range('K10').columns.autofit()
    
    # Note for power users
    dash.range('K17').value = "💡 For advanced customization, go to Recipe_Config"
    dash.range('K17').font.italic = True
    dash.range('K17').font.size = 9
    dash.range('K17:N17').merge()
    dash.range('K17').color = (255, 240, 200)
    
    # Data Path Input (row 31)
    dash.range('A31').value = "📂 Data Path:"
    dash.range('A31').font.bold = True
    default_data_path = "/Users/schalkeanindya/SMFdashboard/data/merged/smf_monthly_data.csv"
    dash.range('B31').value = default_data_path
    dash.range('B31').color = (255, 255, 200)
    dash.range('B31').font.size = 9
    dash.range('B31:K31').merge()
    
    # Status Bar (row 33)
    dash.range('A33').value = "Status:"
    dash.range('A33').font.bold = True
    dash.range('B33').value = "Ready - Generate data to start"
    dash.range('B33').font.italic = True
    dash.range('B33:K33').merge()
    
    # Visualization Area (row 35)
    dash.range('A35').value = "📊 VISUALIZATIONS"
    dash.range('A35').font.size = 16
    dash.range('A35').font.bold = True
    dash.range('A35').color = (70, 130, 180)
    dash.range('A35').font.color = (255, 255, 255)
    dash.range('A35:P35').merge()
    dash.range('A35').api.HorizontalAlignment = -4108
    
    # Setup Recipe Config Sheet
    setup_recipe_config_sheet(wb)
    
    wb.sheets['Dashboard'].activate()
    xw.apps.active.activate(steal_focus=True)
    return "✅ Recipe dashboard initialized"


def setup_recipe_config_sheet(wb):
    """Setup the Recipe Configuration sheet with model checklist"""
    config = wb.sheets['Recipe_Config']
    config.clear()
    
    config.range('A1').value = "⚙️ MODEL SELECTION & CONFIGURATION"
    config.range('A1').font.size = 16
    config.range('A1').font.bold = True
    config.range('A1:H1').merge()
    config.range('A1').color = (70, 130, 180)
    config.range('A1').font.color = (255, 255, 255)
    config.range('A1').api.HorizontalAlignment = -4108
    
    config.range('A2').value = "✓ Check models to enable | Edit hyperparameters | Defaults provided"
    config.range('A2').font.italic = True
    config.range('A2:H2').merge()
    config.range('A2').color = (255, 255, 230)
    
    # Recipe Naming & Data Path Section (NEW - moved from Dashboard)
    config.range('A3').value = "💾 RECIPE NAME & DATA PATH"
    config.range('A3').font.bold = True
    config.range('A3').font.size = 12
    config.range('A3:D3').merge()
    config.range('A3').color = (255, 200, 100)
    
    config.range('A4').value = "Recipe Name:"
    config.range('A4').font.bold = True
    config.range('B4').value = "my_custom_recipe"
    config.range('B4').color = (255, 255, 200)
    config.range('B4:D4').merge()
    config.range('B4').font.size = 11
    
    config.range('E4').value = "➜ Click 'Save Recipe' button after naming"
    config.range('E4').font.italic = True
    config.range('E4:H4').merge()
    config.range('E4').font.size = 9
    config.range('E4').color = (255, 255, 230)
    
    config.range('A5').value = "Data Path: (set in Dashboard B31)"
    config.range('A5').font.bold = True
    config.range('A5').font.italic = True
    config.range('B5').value = "=Dashboard!B31"
    config.range('B5').color = (200, 255, 200)
    config.range('B5:H5').merge()
    config.range('B5').font.size = 9
    
    # Add quick data select helper
    config.range('A6').value = "💡 Available datasets:"
    config.range('A6').font.italic = True
    config.range('A6').font.size = 9
    datasets_info = "Daily (6 vars) | Weekly (40 vars) | Monthly (43 vars) | Quarterly (44 vars) | Semesterly (44 vars) | Yearly (44 vars)"
    config.range('B6').value = datasets_info
    config.range('B6:H6').merge()
    config.range('B6').font.size = 8
    config.range('B6').font.italic = True
    config.range('B6').color = (240, 248, 255)
    
    # Models Checklist Section
    config.range('A8').value = "☑️ SELECT MODELS TO TEST"
    config.range('A8').font.bold = True
    config.range('A8').font.size = 14
    config.range('A8:C8').merge()
    config.range('A8').color = (220, 220, 220)
    
    config.range('A9').value = [
        ['✓', 'Model Name', 'Description']
    ]
    config.range('A9:C9').font.bold = True
    config.range('A9:C9').color = (200, 200, 255)
    
    # All available models with descriptions (from both repos)
    models_list = [
        # === Basic Forecasting Models (Fast, Good Baselines) ===
        [True, 'Naive', 'Naive Forecast - Last value baseline'],
        [True, 'SeasonalNaive', 'Seasonal Naive - Last season baseline'],
        [False, 'Drift', 'Drift Model - Linear trend'],
        [True, 'MovingAverage', 'Moving Average - Smoothing'],
        [True, 'ExponentialSmoothing', 'Exponential Smoothing - Weighted average'],
        
        # === Linear Models (Fast, Interpretable) ===
        [True, 'Linear', 'Linear Regression - Simple trend'],
        [True, 'StandardizedLinear', 'Linear with normalization'],
        [True, 'Ridge', 'Ridge Regression - L2 regularization'],
        [True, 'StandardizedRidge', 'Ridge with normalization'],
        [True, 'Lasso', 'Lasso Regression - L1 feature selection'],
        [True, 'ElasticNet', 'ElasticNet - Ridge + Lasso combined'],
        [True, 'ElasticNetGrid', 'ElasticNet with grid search'],
        [False, 'Huber', 'Huber - Robust to outliers'],
        [False, 'PLS1', 'Partial Least Squares - Factor extraction'],
        [False, 'QuantileRegression', 'Quantile Regression - Robust estimates'],
        
        # === Time Series Models (Designed for TS) ===
        [True, 'AR1', 'Autoregressive (1) - Simple AR'],
        [True, 'ARp', 'Autoregressive (p) - Multiple lags'],
        [True, 'ARIMA', 'ARIMA - Full time series model'],
        [False, 'SARIMAX', 'SARIMAX - Seasonal ARIMA with exog'],
        [False, 'TVP', 'Time-Varying Parameters - Adaptive'],
        [False, 'BVAR', 'Bayesian VAR - Multivariate shrinkage'],
        [False, 'VAR', 'Vector Autoregression - Multivariate'],
        
        # === Tree-Based Models (Good for non-linearity) ===
        [True, 'DecisionTree', 'Decision Tree - Single tree'],
        [True, 'RandomForest', 'Random Forest - Ensemble of trees'],
        [True, 'ExtraTrees', 'Extra Trees - Randomized splits'],
        [True, 'GradientBoosting', 'Gradient Boosting - Sequential trees'],
        [True, 'StochasticGB', 'Stochastic GB - With subsampling'],
        [True, 'XGBoost', 'XGBoost - Advanced gradient boosting'],
        [True, 'LightGBM', 'LightGBM - Fast gradient boosting'],
        [True, 'CatBoost', 'CatBoost - Categorical boosting'],
        [True, 'Bagging', 'Bagging - Bootstrap aggregating'],
        
        # === Advanced ML Models ===
        [False, 'KNN', 'K-Nearest Neighbors - Instance-based'],
        [False, 'SVR', 'Support Vector Regression - Kernel method'],
        [False, 'NeuralNetwork', 'Neural Network - MLP regressor'],
        
        # === Factor & Dimensionality Reduction ===
        [False, 'DFM', 'Dynamic Factor Model - Extract common factors'],
        [False, 'DFM2', 'Dynamic Factor Model v2 - Enhanced'],
        [False, 'PCA', 'PCA Regression - Principal components'],
        
        # === Financial Models (For rates/volatility) ===
        [False, 'GARCH', 'GARCH - Volatility clustering'],
        [False, 'NeuroGARCH', 'Neural GARCH - ML + volatility'],
        [False, 'DNS', 'Dynamic Nelson-Siegel - Yield curves'],
        [False, 'MIDAS', 'MIDAS - Mixed frequency data'],
        
        # === Deep Learning (Slow, requires more data) ===
        [False, 'LSTM', 'LSTM - Neural network for sequences'],
        [False, 'GRU', 'GRU - Gated Recurrent Unit'],
        [False, 'Transformer', 'Transformer - Attention mechanism']
    ]
    
    for i, (checked, model, desc) in enumerate(models_list, 10):
        # Use ✓ and ✗ instead of TRUE/FALSE for better visual clarity
        config.range(f'A{i}').value = '✓' if checked else '✗'
        config.range(f'B{i}').value = model
        config.range(f'C{i}').value = desc
        config.range(f'A{i}').color = (200, 255, 200) if checked else (255, 200, 200)  # Green for checked, red for unchecked
        config.range(f'A{i}').api.HorizontalAlignment = -4108  # Center
        
        # Add data validation for easier toggle (dropdown with ✓ and ✗)
        try:
            config.range(f'A{i}').api.Validation.Delete()
            config.range(f'A{i}').api.Validation.Add(
                Type=3,  # xlValidateList
                AlertStyle=1,  # xlValidAlertStop
                Formula1='✓,✗'
            )
        except:
            pass  # Skip if validation fails
    
    last_model_row = 10 + len(models_list) - 1
    
    # Hyperparameters Section - MOVED DOWN to row 65+ to avoid overlap with targets/exog
    hyperparam_start = 65
    
    config.range(f'E{hyperparam_start}').value = "🔧 HYPERPARAMETERS (Default Settings)"
    config.range(f'E{hyperparam_start}').font.bold = True
    config.range(f'E{hyperparam_start}').font.size = 14
    config.range(f'E{hyperparam_start}:H{hyperparam_start}').merge()
    config.range(f'E{hyperparam_start}').color = (220, 220, 220)
    
    config.range(f'E{hyperparam_start+1}').value = [
        ['Model', 'Parameter', 'Value', 'Description']
    ]
    config.range(f'E{hyperparam_start+1}:H{hyperparam_start+1}').font.bold = True
    config.range(f'E{hyperparam_start+1}:H{hyperparam_start+1}').color = (200, 200, 255)
    
    # Default hyperparameters for ALL 25+ models in MODEL_REGISTRY
    hyperparams = [
        # === Tree-Based Models ===
        ['RandomForest', 'n_estimators', 100, 'Number of trees'],
        ['RandomForest', 'max_depth', 10, 'Max tree depth'],
        ['RandomForest', 'min_samples_split', 2, 'Min samples to split'],
        ['', '', '', ''],
        ['ExtraTrees', 'n_estimators', 100, 'Number of trees'],
        ['ExtraTrees', 'max_depth', 10, 'Max tree depth'],
        ['', '', '', ''],
        ['XGBoost', 'n_estimators', 100, 'Number of boosting rounds'],
        ['XGBoost', 'learning_rate', 0.1, 'Step size shrinkage'],
        ['XGBoost', 'max_depth', 6, 'Max tree depth'],
        ['', '', '', ''],
        ['GradientBoosting', 'n_estimators', 100, 'Number of boosting stages'],
        ['GradientBoosting', 'learning_rate', 0.1, 'Learning rate'],
        ['GradientBoosting', 'max_depth', 3, 'Max depth'],
        ['', '', '', ''],
        ['StochasticGB', 'n_estimators', 100, 'Number of boosting stages'],
        ['StochasticGB', 'learning_rate', 0.1, 'Learning rate'],
        ['StochasticGB', 'subsample', 0.8, 'Fraction of samples per tree'],
        ['', '', '', ''],
        ['LightGBM', 'n_estimators', 100, 'Number of trees'],
        ['LightGBM', 'learning_rate', 0.1, 'Learning rate'],
        ['LightGBM', 'num_leaves', 31, 'Max leaves per tree'],
        ['', '', '', ''],
        ['CatBoost', 'iterations', 100, 'Number of trees'],
        ['CatBoost', 'learning_rate', 0.1, 'Learning rate'],
        ['CatBoost', 'depth', 6, 'Tree depth'],
        ['', '', '', ''],
        ['DecisionTree', 'max_depth', 5, 'Max tree depth'],
        ['DecisionTree', 'min_samples_split', 2, 'Min samples to split'],
        ['', '', '', ''],
        ['Bagging', 'n_estimators', 10, 'Number of base estimators'],
        ['Bagging', 'max_samples', 1.0, 'Fraction of samples'],
        ['', '', '', ''],
        
        # === Linear Models ===
        ['Ridge', 'alpha', 1.0, 'Regularization strength'],
        ['', '', '', ''],
        ['StandardizedRidge', 'alpha', 1.0, 'Regularization strength'],
        ['', '', '', ''],
        ['Lasso', 'alpha', 1.0, 'L1 regularization'],
        ['', '', '', ''],
        ['ElasticNet', 'alpha', 1.0, 'Regularization strength'],
        ['ElasticNet', 'l1_ratio', 0.5, 'L1 vs L2 ratio (0-1)'],
        ['', '', '', ''],
        ['ElasticNetGrid', 'alpha_min', 0.01, 'Min alpha for grid'],
        ['ElasticNetGrid', 'alpha_max', 10.0, 'Max alpha for grid'],
        ['ElasticNetGrid', 'n_alphas', 10, 'Number of alphas to try'],
        ['', '', '', ''],
        ['Huber', 'epsilon', 1.35, 'Outlier threshold'],
        ['Huber', 'alpha', 0.0001, 'Regularization'],
        ['', '', '', ''],
        ['PLS1', 'n_components', 2, 'Number of components'],
        ['', '', '', ''],
        
        # === Time Series Models ===
        ['AR1', 'None', 'N/A', 'No parameters (AR1 fixed)'],
        ['', '', '', ''],
        ['ARp', 'p', 4, 'Number of AR lags'],
        ['', '', '', ''],
        ['ARIMA', 'order_p', 1, 'AR order'],
        ['ARIMA', 'order_d', 1, 'Differencing order'],
        ['ARIMA', 'order_q', 1, 'MA order'],
        ['', '', '', ''],
        ['SARIMAX', 'order_p', 1, 'AR order'],
        ['SARIMAX', 'order_d', 1, 'Differencing'],
        ['SARIMAX', 'order_q', 1, 'MA order'],
        ['SARIMAX', 'seasonal_period', 12, 'Seasonal period'],
        ['', '', '', ''],
        ['BVAR', 'lags', 4, 'Number of lags'],
        ['BVAR', 'lambda_prior', 0.2, 'Shrinkage parameter'],
        ['', '', '', ''],
        ['VAR', 'maxlags', 4, 'Maximum lags'],
        ['', '', '', ''],
        
        # === Factor Models ===
        ['DFM', 'n_factors', 3, 'Number of latent factors'],
        ['DFM', 'factor_order', 1, 'AR order of factors'],
        ['', '', '', ''],
        ['DFM2', 'n_factors', 3, 'Number of factors'],
        ['', '', '', ''],
        ['PCA', 'n_components', 5, 'Number of PCA components'],
        ['', '', '', ''],
        
        # === Financial Models ===
        ['GARCH', 'p', 1, 'GARCH lag order'],
        ['GARCH', 'q', 1, 'ARCH lag order'],
        ['', '', '', ''],
        ['NeuroGARCH', 'hidden_units', 10, 'Neural network hidden units'],
        ['', '', '', ''],
        ['DNS', 'tau', 10.0, 'Decay factor'],
        ['', '', '', ''],
        ['MIDAS', 'horizon', 1, 'Forecast horizon'],
        ['', '', '', ''],
        
        # === Deep Learning ===
        ['LSTM', 'hidden_size', 50, 'LSTM hidden units'],
        ['LSTM', 'num_layers', 2, 'Number of LSTM layers'],
        ['LSTM', 'epochs', 50, 'Training epochs'],
        ['', '', '', ''],
        ['GRU', 'hidden_size', 50, 'GRU hidden units'],
        ['GRU', 'num_layers', 2, 'Number of layers'],
        ['', '', '', ''],
        ['Transformer', 'n_heads', 4, 'Attention heads'],
        ['Transformer', 'd_model', 64, 'Model dimension'],
        ['', '', '', ''],
        ['NeuralNetwork', 'hidden_layer_sizes', '(50,25)', 'Hidden layer sizes'],
        ['NeuralNetwork', 'activation', 'relu', 'Activation function'],
        ['', '', '', ''],
        
        # === Other Models ===
        ['KNN', 'n_neighbors', 5, 'Number of neighbors'],
        ['KNN', 'weights', 'uniform', 'Weight function'],
        ['', '', '', ''],
        ['SVR', 'kernel', 'rbf', 'Kernel type (linear/rbf/poly)'],
        ['SVR', 'C', 1.0, 'Regularization parameter'],
        ['SVR', 'epsilon', 0.1, 'Epsilon in loss function'],
        ['', '', '', ''],
        ['QuantileRegression', 'quantile', 0.5, 'Quantile to estimate (0-1)'],
        ['QuantileRegression', 'alpha', 1.0, 'Regularization'],
        ['', '', '', ''],
        
        # === Naive Models (no parameters) ===
        ['Naive', 'None', 'N/A', 'No parameters'],
        ['', '', '', ''],
        ['SeasonalNaive', 'season', 12, 'Seasonal period'],
        ['', '', '', ''],
        ['Drift', 'None', 'N/A', 'No parameters'],
        ['', '', '', ''],
        ['MovingAverage', 'window', 3, 'Window size'],
        ['', '', '', ''],
        ['ExponentialSmoothing', 'alpha', 0.3, 'Smoothing parameter (0-1)'],
    ]
    
    for i, (model, param, value, desc) in enumerate(hyperparams, hyperparam_start+2):
        config.range(f'E{i}').value = model
        config.range(f'F{i}').value = param
        config.range(f'G{i}').value = value
        config.range(f'H{i}').value = desc
        if value != '':  # Only highlight non-empty values
            config.range(f'G{i}').color = (255, 255, 200)  # Editable
    
    # Forecast Settings - LEFT SIDE (A-C) after models
    # Models end at row 52 (10 + 44 - 1), so start forecast settings at row 54
    forecast_start_row = 54
    
    config.range(f'A{forecast_start_row}').value = "📅 FORECAST SETTINGS & DATA FREQUENCY"
    config.range(f'A{forecast_start_row}').font.bold = True
    config.range(f'A{forecast_start_row}').font.size = 14
    config.range(f'A{forecast_start_row}:C{forecast_start_row}').merge()
    config.range(f'A{forecast_start_row}').color = (220, 220, 220)
    
    config.range(f'A{forecast_start_row+1}').value = [
        ['Setting', 'Value', 'Description'],
        ['Data Frequency', 'Monthly', 'Monthly/Quarterly/Semesterly/Yearly'],
        ['Horizons (comma-separated)', '1,3,6,12', 'Forecast periods ahead'],
        ['Train Start Date', '2005-01-01', 'Training period start (YYYY-MM-DD)'],
        ['Train End Date', '2019-12-31', 'Training period end (YYYY-MM-DD)'],
        ['Test Start Date', '2020-01-01', 'Testing/backcast start (YYYY-MM-DD)'],
        ['Test End Date', '2024-12-31', 'Testing/backcast end (YYYY-MM-DD)'],
        ['Date Column', 'date', 'Column name for dates']
    ]
    config.range(f'A{forecast_start_row+1}:C{forecast_start_row+1}').font.bold = True
    config.range(f'A{forecast_start_row+1}:C{forecast_start_row+1}').color = (200, 200, 255)
    config.range(f'B{forecast_start_row+2}:B{forecast_start_row+8}').color = (255, 255, 200)  # All editable
    
    # Target Variables Selection - RIGHT SIDE (E-G), starts at row 8
    config.range('E8').value = "🎯 TARGET/OUTCOME VARIABLES"
    config.range('E8').font.bold = True
    config.range('E8').font.size = 14
    config.range('E8:G8').merge()
    config.range('E8').color = (100, 200, 150)
    
    config.range('E9').value = [
        ['✓', 'Variable Name', 'Horizons']
    ]
    config.range('E9:G9').font.bold = True
    config.range('E9:G9').color = (200, 255, 200)
    
    config.range('E10').value = "→ Load data first, variables will populate here"
    config.range('E10:G10').merge()
    config.range('E10').font.italic = True
    config.range('E10').color = (255, 255, 230)
    
    # Exogenous Variables Selection - FAR RIGHT (I-K), starts at row 8
    config.range('I8').value = "📊 EXOGENOUS/FEATURE VARIABLES"
    config.range('I8').font.bold = True
    config.range('I8').font.size = 14
    config.range('I8:K8').merge()
    config.range('I8').color = (255, 200, 100)
    
    config.range('I9').value = [
        ['✓', 'Variable Name', 'Lags (comma)']
    ]
    config.range('I9:K9').font.bold = True
    config.range('I9:K9').color = (255, 230, 200)
    
    config.range('I10').value = "→ Load data first, variables will populate here"
    config.range('I10:K10').merge()
    config.range('I10').font.italic = True
    config.range('I10').color = (255, 255, 230)
    
    # Auto-fit columns
    config.range('A:K').columns.autofit()
    
    # Template grids section - moved down after forecast settings (which now ends ~row 62)
    template_start_row = 64
    
    config.range(f'A{template_start_row}').value = [
        ['Model', 'Parameter', 'Values (comma-separated)']
    ]
    config.range(f'A{template_start_row}:C{template_start_row}').font.bold = True
    config.range(f'A{template_start_row}:C{template_start_row}').color = (200, 200, 255)
    
    # Default hyperparameters for grid search
    default_hypers = [
        ['RandomForest', 'n_estimators', '50, 100, 200'],
        ['RandomForest', 'max_depth', '5, 10, 15'],
        ['XGBoost', 'n_estimators', '50, 100, 200'],
        ['XGBoost', 'learning_rate', '0.01, 0.1, 0.2'],
        ['ARIMA', 'p', '0, 1, 2, 3'],
        ['ARIMA', 'd', '0, 1, 2'],
        ['ARIMA', 'q', '0, 1, 2']
    ]
    config.range(f'A{template_start_row+1}').value = default_hypers
    config.range(f'C{template_start_row+1}:C{template_start_row+7}').color = (255, 255, 200)
    
    config.range('A:C').columns.autofit()
    config.range('E:F').columns.autofit()


def get_frequency_template(frequency):
    """Get default template based on frequency"""
    templates = {
        'Monthly': {
            'code': 'M',
            'horizons': [1, 3, 6, 12, 24],
            'test_periods': 12,
            'description': 'Monthly data - 1-24 month forecasts'
        },
        'Quarterly': {
            'code': 'Q',
            'horizons': [1, 2, 4, 8],
            'test_periods': 4,
            'description': 'Quarterly data - 1-8 quarter forecasts'
        },
        'Semesterly': {
            'code': 'S',
            'horizons': [1, 2, 3, 4],
            'test_periods': 2,
            'description': 'Semesterly data - 1-4 semester forecasts'
        },
        'Yearly': {
            'code': 'Y',
            'horizons': [1, 2, 3, 5, 10],
            'test_periods': 3,
            'description': 'Yearly data - 1-10 year forecasts'
        }
    }
    return templates.get(frequency, templates['Monthly'])


def apply_frequency_template():
    """Apply frequency template to configuration"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    config_sheet = wb.sheets['Recipe_Config']
    
    # Get selected frequency
    frequency = dash.range('B4').value
    if not frequency or frequency not in ['Monthly', 'Quarterly', 'Semesterly', 'Yearly']:
        frequency = 'Monthly'
    
    template = get_frequency_template(frequency)
    
    # Update settings in Recipe_Config (row 57 in new layout)
    horizons_str = ','.join(map(str, template['horizons']))
    config_sheet.range('B57').value = horizons_str
    # Note: Train/test dates (rows 58-61) are now set manually by user
    
    dash.range('B33').value = f"✅ Applied {frequency} template: {template['description']}"
    config_sheet.activate()
    
    return f"✅ Template applied: {frequency}"


def get_selected_models():
    """Get list of selected models from Recipe_Config"""
    wb = xw.Book.caller()
    config = wb.sheets['Recipe_Config']
    
    selected_models = []
    # Read checkboxes from rows 10-53 (where models are listed) - 44 models total
    for i in range(10, 54):
        checked = config.range(f'A{i}').value
        model_name = config.range(f'B{i}').value
        
        # Handle both ✓/✗ and TRUE/FALSE formats
        is_checked = False
        if checked:
            if isinstance(checked, str):
                is_checked = checked in ['✓', 'TRUE', 'True', 'true', 'YES', 'Yes', 'yes']
            elif isinstance(checked, bool):
                is_checked = checked
        
        if is_checked and model_name:
            selected_models.append(model_name)
    
    return selected_models


def get_selected_targets():
    """Get list of selected target variables from Recipe_Config (columns E-G)"""
    wb = xw.Book.caller()
    config = wb.sheets['Recipe_Config']
    
    selected_targets = []
    # Read checkboxes from columns E-G starting at row 10
    for i in range(10, 60):  # Check up to 50 variables
        checked = config.range(f'E{i}').value
        var_name = config.range(f'F{i}').value
        horizons_str = config.range(f'G{i}').value
        
        # Handle both ✓/✗ and TRUE/FALSE formats
        is_checked = False
        if checked:
            if isinstance(checked, str):
                is_checked = checked in ['✓', 'TRUE', 'True', 'true', 'YES', 'Yes', 'yes']
            elif isinstance(checked, bool):
                is_checked = checked
        
        if is_checked and var_name:
            try:
                horizons = [int(h.strip()) for h in str(horizons_str).split(',') if h.strip()]
            except:
                horizons = [1, 3, 6, 12]
            
            selected_targets.append({
                'name': var_name,
                'horizons': horizons
            })
    
    return selected_targets


def get_selected_exog():
    """Get list of selected exogenous variables from Recipe_Config (columns I-K)"""
    wb = xw.Book.caller()
    config = wb.sheets['Recipe_Config']
    
    selected_exog = []
    # Read checkboxes from columns I-K starting at row 10
    for i in range(10, 60):  # Check up to 50 variables
        checked = config.range(f'I{i}').value
        var_name = config.range(f'J{i}').value
        lags_str = config.range(f'K{i}').value
        
        # Handle both ✓/✗ and TRUE/FALSE formats
        is_checked = False
        if checked:
            if isinstance(checked, str):
                is_checked = checked in ['✓', 'TRUE', 'True', 'true', 'YES', 'Yes', 'yes']
            elif isinstance(checked, bool):
                is_checked = checked
        
        if is_checked and var_name:
            try:
                lags = [int(lag.strip()) for lag in str(lags_str).split(',') if lag.strip()]
            except:
                lags = [0, 1]
            
            selected_exog.append({
                'name': var_name,
                'lags': lags
            })
    
    return selected_exog


def get_hyperparameters():
    """Get hyperparameters from Recipe_Config (now at rows 67+)"""
    wb = xw.Book.caller()
    config = wb.sheets['Recipe_Config']
    
    hyperparams = {}
    # Read from rows 67-110 where hyperparameters are now located (moved down to avoid overlap)
    for i in range(67, 111):
        model = config.range(f'E{i}').value
        param = config.range(f'F{i}').value
        value = config.range(f'G{i}').value
        
        if model and param and value:
            if model not in hyperparams:
                hyperparams[model] = {}
            hyperparams[model][param] = value
    
    return hyperparams


def load_data_from_recipe():
    """Load data specified in the recipe"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    config_sheet = wb.sheets['Recipe_Config']
    data_view = wb.sheets['Data_View']
    
    # Get data path from Dashboard
    data_path_raw = dash.range('B28').value
    if not data_path_raw:
        dash.range('B33').value = "⚠️ No data path set. Enter path in Dashboard B28"
        return "⚠️ No data path"
    
    # Try to resolve path
    data_path = None
    if os.path.exists(data_path_raw):
        data_path = data_path_raw
    else:
        # Try relative to DATA_DIR
        potential_path = DATA_DIR / Path(data_path_raw).name
        if potential_path.exists():
            data_path = potential_path
    
    if not data_path or not os.path.exists(data_path):
        dash.range('B33').value = f"⚠️ Data file not found: {Path(data_path_raw).name}"
        return "⚠️ Data not found"
    
    # Load CSV
    try:
        df = pd.read_csv(data_path)
        df = df.head(1000)  # Limit for Excel
    except Exception as e:
        dash.range('B33').value = f"⚠️ Error loading data: {str(e)[:50]}"
        return f"⚠️ Error: {e}"
    
    # Write to Data_View sheet
    data_view.clear()
    data_view.range('A1').value = f"📊 DATA: {Path(data_path).name}"
    data_view.range('A1').font.bold = True
    data_view.range('A1').font.size = 14
    
    data_view.range('A3').value = df
    data_view.range('A3').expand('right').font.bold = True
    data_view.range('A3').expand('right').color = (70, 130, 180)
    data_view.range('A3').expand('right').font.color = (255, 255, 255)
    
    try:
        data_view.range('A3').expand().columns.autofit()
    except:
        pass
    
    # Summary
    data_view.range('A1').value = f"📊 DATA: {Path(data_path).name} ({len(df)} rows × {len(df.columns)} cols)"
    
    # Populate target variables in Recipe_Config
    config_sheet = wb.sheets['Recipe_Config']
    
    # Detect date column
    date_col = None
    for col in df.columns:
        if 'date' in str(col).lower() or 'time' in str(col).lower():
            date_col = col
            break
    if date_col is None:
        date_col = df.columns[0]
    
    # Get numeric columns (potential targets)
    numeric_cols = [col for col in df.columns if col != date_col and pd.api.types.is_numeric_dtype(df[col])]
    
    # Auto-detect frequency from dates
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        time_diff = df[date_col].diff().median()
        if time_diff <= pd.Timedelta(days=7):
            freq = 'Daily'
            default_horizons = '1,7,14,30'
        elif time_diff <= pd.Timedelta(days=10):
            freq = 'Weekly'
            default_horizons = '1,4,12,24'
        elif time_diff <= pd.Timedelta(days=40):
            freq = 'Monthly'
            default_horizons = '1,3,6,12'
        elif time_diff <= pd.Timedelta(days=120):
            freq = 'Quarterly'
            default_horizons = '1,2,4,8'
        elif time_diff <= pd.Timedelta(days=210):
            freq = 'Semesterly'
            default_horizons = '1,2,3,4'
        else:
            freq = 'Yearly'
            default_horizons = '1,2,3,5'
        
        # Update frequency in config (row 56 in new layout)
        config_sheet.range('B56').value = freq
    except:
        default_horizons = '1,3,6,12'
    
    # Clear and populate TARGET variables in columns E-G (starting at row 10)
    target_start_row = 10
    config_sheet.range(f'E{target_start_row}:G{target_start_row+50}').clear_contents()
    
    # Populate target variables
    for i, var_name in enumerate(numeric_cols[:50], 0):  # Up to 50 variables
        config_sheet.range(f'E{target_start_row+i}').value = '✓'  # Checked by default (use ✓ instead of TRUE)
        config_sheet.range(f'F{target_start_row+i}').value = var_name
        config_sheet.range(f'G{target_start_row+i}').value = default_horizons
        config_sheet.range(f'E{target_start_row+i}').color = (200, 255, 200)  # Green for checked
        config_sheet.range(f'E{target_start_row+i}').api.HorizontalAlignment = -4108  # Center
        config_sheet.range(f'G{target_start_row+i}').color = (255, 255, 200)  # Editable
        
        # Add data validation for easier toggle
        try:
            config_sheet.range(f'E{target_start_row+i}').api.Validation.Delete()
            config_sheet.range(f'E{target_start_row+i}').api.Validation.Add(
                Type=3, AlertStyle=1, Formula1='✓,✗'
            )
        except:
            pass
    
    # Populate EXOGENOUS variables in columns I-K (starting at row 10)
    exog_start_row = 10
    config_sheet.range(f'I{exog_start_row}:K{exog_start_row+50}').clear_contents()
    
    default_lags = '0,1'  # Default: current and 1 lag
    
    # Populate exog variables (same list, but unchecked by default)
    for i, var_name in enumerate(numeric_cols[:50], 0):
        config_sheet.range(f'I{exog_start_row+i}').value = '✗'  # Unchecked by default (use ✗ instead of FALSE)
        config_sheet.range(f'J{exog_start_row+i}').value = var_name
        config_sheet.range(f'K{exog_start_row+i}').value = default_lags
        config_sheet.range(f'I{exog_start_row+i}').color = (255, 200, 200)  # Red for unchecked
        config_sheet.range(f'I{exog_start_row+i}').api.HorizontalAlignment = -4108  # Center
        config_sheet.range(f'K{exog_start_row+i}').color = (255, 255, 200)  # Editable
        
        # Add data validation for easier toggle
        try:
            config_sheet.range(f'I{exog_start_row+i}').api.Validation.Delete()
            config_sheet.range(f'I{exog_start_row+i}').api.Validation.Add(
                Type=3, AlertStyle=1, Formula1='✓,✗'
            )
        except:
            pass
    
    dash.range('B33').value = f"✅ Loaded: {len(df)} rows × {len(numeric_cols)} variables | Frequency: {freq}"
    data_view.activate()
    
    return f"✅ Loaded {len(df)} rows"


def run_forecast_with_precomputed_models():
    """
    CORRECTED LOGIC:
    1. Reads top N models from Backcast_Results sheet (generated by backtest)
    2. Re-trains ONLY these top models on full historical data
    3. Generates proper multi-step autoregressive forecast using trained models
    """
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    data_view = wb.sheets['Data_View']
    backcast_sheet = wb.sheets['Backcast_Results']
    
    dash.range('B33').value = "⏳ Forecasting with top models from backcast..."
    
    # Get Top N from settings
    top_n = int(dash.range('B10').value or 3)
    max_forecast_periods = int(dash.range('B12').value or 12)
    
    # Get forecast horizons from settings (B11)
    forecast_horizons_str = dash.range('B11').value or '1,3,6,12'
    try:
        forecast_horizons = [int(h.strip()) for h in str(forecast_horizons_str).split(',')]
    except:
        forecast_horizons = [1, 3, 6, 12]
    
    # Get selected variables (rows 11-20) from columns D/E
    selected_vars = []
    for row in range(11, 21):
        checkbox = dash.range(f'D{row}').value
        if checkbox == '✓':
            var_name = dash.range(f'E{row}').value
            if var_name:
                selected_vars.append(var_name)
    
    # Get selected frequencies (rows 11-16) from columns F/G
    selected_freqs = []
    for row in range(11, 17):
        checkbox = dash.range(f'F{row}').value
        if checkbox == '✓':
            freq = dash.range(f'G{row}').value
            if freq:
                selected_freqs.append(freq)
    
    if not selected_vars or not selected_freqs:
        dash.range('B33').value = "⚠️ Please select variables and frequencies first"
        return "⚠️ No selection"
    
    # Load data
    try:
        df = data_view.range('A3').options(pd.DataFrame, header=1, index=False, expand='table').value
        if df is None or df.empty:
            dash.range('B33').value = "⚠️ No data in Data_View. Load data first."
            return "⚠️ No data"
    except Exception as e:
        dash.range('B33').value = f"⚠️ Could not load data: {str(e)[:50]}"
        return "⚠️ Data load error"
    
    # Assume first column is date
    date_col = df.columns[0]
    if date_col:
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        except:
            pass
    
    # Create Forecast_Results sheet
    if 'Forecast_Results' in [s.name for s in wb.sheets]:
        forecast_sheet = wb.sheets['Forecast_Results']
        forecast_sheet.clear()
    else:
        forecast_sheet = wb.sheets.add('Forecast_Results')
    
    forecast_sheet.range('A1').value = f"📈 FORECASTS FROM TOP {top_n} BACKTEST MODELS"
    forecast_sheet.range('A1').font.bold = True
    forecast_sheet.range('A1').font.size = 14
    forecast_sheet.range('A1').color = (70, 130, 180)
    forecast_sheet.range('A1').font.color = (255, 255, 255)
    
    current_row = 3
    
    # Load top models from FINAL_EXCEL_REPORTS (precomputed results)
    all_top_models = {}  # { 'variable_name': ['Model1', 'Model2'], ... }
    
    # Map frequency to Excel file
    freq_to_file = {
        'monthly': 'forecasting_results_Monthly_detailed.xlsx',
        'quarterly': 'forecasting_results_Quarterly_detailed.xlsx',
        'yearly': 'forecasting_results_Yearly_detailed.xlsx',
        'semesterly': 'forecasting_results_Semesterly_detailed.xlsx',
    }
    
    try:
        for freq in selected_freqs:
            excel_file = freq_to_file.get(str(freq).lower())
            if not excel_file:
                continue
            
            file_path = os.path.join('/Users/schalkeanindya/SMFdashboard/FINAL_EXCEL_REPORTS', excel_file)
            if not os.path.exists(file_path):
                continue
            
            df_excel = pd.read_excel(file_path)
            
            # Find variable and RMSE columns
            var_col = None
            for col in ['Variable', 'variable', 'target', 'Target', 'Y Variable']:
                if col in df_excel.columns:
                    var_col = col
                    break
            
            rmse_col = None
            for col in ['RMSE', 'rmse', 'RMSE@H=1', 'test_rmse']:
                if col in df_excel.columns:
                    rmse_col = col
                    break
            
            if not var_col or not rmse_col:
                continue
            
            # For each selected variable, get top N models
            for var in selected_vars:
                var_data = df_excel[df_excel[var_col].astype(str) == str(var)]
                if len(var_data) == 0:
                    continue
                
                var_data_sorted = var_data.sort_values(rmse_col).head(top_n)
                
                for idx, row in var_data_sorted.iterrows():
                    model_name = ''
                    for col_name in ['Model', 'model_name', 'Model Type', 'plugin', 'Plugin', 'model', 'Member', 'member']:
                        if col_name in df_excel.columns:
                            val = row.get(col_name)
                            if val is not None:
                                model_name = str(val).strip()
                                if model_name and model_name != 'nan' and model_name.lower() != 'none':
                                    break
                    
                    if not model_name:
                        for col in df_excel.columns:
                            if 'id' in col.lower() or 'member' in col.lower() or 'variant' in col.lower():
                                val = row.get(col)
                                if val is not None:
                                    id_str = str(val).strip()
                                    if '-' in id_str:
                                        model_name = id_str.split('-')[0]
                                    else:
                                        model_name = id_str
                                    if model_name:
                                        break
                    
                    if model_name and var not in all_top_models:
                        all_top_models[var] = []
                    if model_name and model_name not in all_top_models[var]:
                        all_top_models[var].append(model_name)
    
    except Exception as e:
        dash.range('B33').value = f"⚠️ Could not load precomputed models. Error: {e}"
        import traceback
        traceback.print_exc()
        return "⚠️ Failed to load models"
    
    if not all_top_models:
        dash.range('B33').value = "⚠️ No models found in precomputed results for selected variables."
        return "⚠️ No models found"
    
    # Debug: Show what we found
    debug_msg = f"Found models for: {list(all_top_models.keys())[:3]}..."
    dash.range('B33').value = debug_msg
    
    # For each variable, train its top models and forecast
    results_written = False
    for target_col in selected_vars:
        # Debug variable matching
        in_all_top = target_col in all_top_models
        in_df = target_col in df.columns
        
        if not in_all_top:
            forecast_sheet.range(f'A{current_row}').value = f"⚠️ {target_col}: Not in precomputed results"
            current_row += 2
            continue
        if not in_df:
            forecast_sheet.range(f'A{current_row}').value = f"⚠️ {target_col}: Not in Data_View (available: {', '.join(df.columns[:3])}...)"
            current_row += 2
            continue
        
        top_model_names = all_top_models[target_col]
        if not top_model_names:
            continue
        
        try:
            # Prepare data for full history
            y_full = df[target_col].dropna().values
            if len(y_full) < 12:
                forecast_sheet.range(f'A{current_row}').value = f"⚠️ {target_col}: Not enough data (need ≥12 observations)"
                current_row += 2
                continue
            
            lags = [1, 3, 6, 12]
            X_all, y_all_target, _ = build_lagged_features(y_full, lags=lags, horizon=1)
            
            if len(X_all) == 0:
                forecast_sheet.range(f'A{current_row}').value = f"⚠️ {target_col}: Could not build features"
                current_row += 2
                continue
            
            # Train models and generate forecasts
            forecasts = {}
            for model_name in top_model_names:
                try:
                    model = create_model(model_name)
                    if model is None:
                        continue
                    
                    # Train on full history
                    model.fit(X_all.tolist(), y_all_target.tolist())
                    
                    # Autoregressive forecasting loop
                    history = list(y_full)
                    predictions = []
                    for period in range(max_forecast_periods):
                        # Build features using LAST values from history
                        features_for_pred = []
                        for lag in lags:
                            if len(history) >= lag:
                                features_for_pred.append(history[-lag])
                            else:
                                # Fallback to original data
                                if len(y_full) >= lag:
                                    features_for_pred.append(y_full[-lag])
                                else:
                                    features_for_pred.append(y_full[0])  # Use first value as fallback
                        
                        # Make prediction
                        try:
                            next_pred = model.predict_row(features_for_pred)
                        except:
                            # If predict_row fails, use simple average
                            next_pred = np.mean(history[-3:]) if len(history) >= 3 else history[-1]
                        
                        predictions.append(next_pred)
                        history.append(next_pred)
                    
                    forecasts[model_name] = predictions
                except Exception as e:
                    print(f"Error forecasting with {model_name} for {target_col}: {e}")
                    import traceback
                    traceback.print_exc()
            
            if not forecasts:
                continue
            
            # Write to Excel with detailed information
            # Variable header
            forecast_sheet.range(f'A{current_row}').value = f"📊 {target_col}"
            forecast_sheet.range(f'A{current_row}').font.bold = True
            forecast_sheet.range(f'A{current_row}').font.size = 12
            forecast_sheet.range(f'A{current_row}').color = (220, 240, 255)
            current_row += 1
            
            # Model specifications info
            forecast_sheet.range(f'A{current_row}').value = f"🔧 Models Used: {', '.join(forecasts.keys())}"
            forecast_sheet.range(f'A{current_row}').font.italic = True
            forecast_sheet.range(f'A{current_row}').font.size = 9
            current_row += 1
            
            # Training info
            forecast_sheet.range(f'A{current_row}').value = f"📈 Training: {len(y_full)} observations, Lags: {lags}, Horizons: {forecast_horizons}"
            forecast_sheet.range(f'A{current_row}').font.italic = True
            forecast_sheet.range(f'A{current_row}').font.size = 9
            current_row += 1
            current_row += 1  # Extra space
            
            # Create forecast table with horizons
            for horizon in forecast_horizons:
                forecast_sheet.range(f'A{current_row}').value = f"🎯 Horizon {horizon} Periods Ahead"
                forecast_sheet.range(f'A{current_row}').font.bold = True
                forecast_sheet.range(f'A{current_row}').color = (240, 248, 255)
                current_row += 1
                
                # Headers
                headers = ['Period'] + list(forecasts.keys())
                forecast_sheet.range(f'A{current_row}').value = [headers]
                forecast_sheet.range(f'A{current_row}').expand('right').font.bold = True
                forecast_sheet.range(f'A{current_row}').expand('right').color = (200, 220, 255)
                current_row += 1
                
                # Forecast values for this horizon
                for i in range(max_forecast_periods):
                    row_data = [f"t+{i+1}"]
                    row_data.extend([forecasts[model][i] for model in forecasts.keys()])
                    forecast_sheet.range(f'A{current_row}').value = row_data
                    current_row += 1
                
                # Add average for this horizon, using comma as decimal separator
                forecast_sheet.range(f'A{current_row}').value = f"📊 Average (h={horizon}):"
                for model in forecasts.keys():
                    avg_val = np.mean([forecasts[model][h-1] for h in forecast_horizons if h <= max_forecast_periods])
                    # Format with comma as decimal, 4 digits
                    avg_val_str = f"{avg_val:.4f}".replace('.', ',')
                    forecast_sheet.range(f'{chr(65+list(forecasts.keys()).index(model)+1)}{current_row}').value = avg_val_str
                forecast_sheet.range(f'A{current_row}').expand('right').font.italic = True
                current_row += 2

            current_row += 2
            results_written = True  # ✅ Mark that we wrote results
        
        except Exception as e:
            print(f"Error generating forecast for {target_col}: {e}")
            forecast_sheet.range(f'A{current_row}').value = f"⚠️ Error for {target_col}: {str(e)[:50]}"
            current_row += 2
            results_written = True
    
    if not results_written:
        forecast_sheet.range('A1').value = "⚠️ NO FORECASTS GENERATED"
        forecast_sheet.range('A2').value = f"Selected vars: {selected_vars}"
        forecast_sheet.range('A3').value = f"Models found: {list(all_top_models.keys())}"
        forecast_sheet.range('A4').value = f"Data columns: {list(df.columns)[:5]}"
        dash.range('B33').value = "⚠️ Check variable names - no forecasts generated"
        return "⚠️ No forecasts"
    
    forecast_sheet.activate()
    dash.range('B33').value = "✅ Forecasts generated using top models from backcast!"
    
    return "✅ Forecast complete"


def run_recipe_forecast():
    """
    Run forecast using top N models from backcast results
    Trains on ALL available data and generates future predictions
    """
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    data_view = wb.sheets['Data_View']
    config_sheet = wb.sheets['Recipe_Config']
    backcast_sheet = wb.sheets['Backcast_Results']
    
    # Create or get forecast sheet
    if 'Forecast_Results' in [s.name for s in wb.sheets]:
        forecast_sheet = wb.sheets['Forecast_Results']
        forecast_sheet.clear()  # Clear old results
    else:
        forecast_sheet = wb.sheets.add('Forecast_Results', after=backcast_sheet)
    
    dash.range('B33').value = "⏳ Generating forecasts with best models..."
    
    # Get settings from Quick Settings (rows 9-12)
    top_n = int(dash.range('B10').value or 3)
    
    # Get data
    try:
        df = data_view.range('A3').options(pd.DataFrame, header=1, index=False, expand='table').value
        if df is None or len(df) == 0:
            dash.range('B33').value = "⚠️ No data loaded. Load Data first!"
            return "⚠️ No data"
    except:
        dash.range('B33').value = "⚠️ No data loaded. Load Data first!"
        return "⚠️ No data"
    
    # Get selected targets
    selected_targets = get_selected_targets()
    if len(selected_targets) == 0:
        dash.range('B33').value = "⚠️ No target variables selected!"
        return "⚠️ No targets"
    
    # Detect date column
    date_col_name = config_sheet.range('B62').value or 'date'
    date_col = None
    for col in df.columns:
        if date_col_name.lower() in str(col).lower() or 'date' in str(col).lower():
            date_col = col
            break
    if date_col is None:
        date_col = df.columns[0]
    
    # Convert dates
    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except:
        dash.range('B33').value = f"⚠️ Could not parse date column"
        return "⚠️ Date error"
    
    # Get horizons from Dashboard (quick settings)
    forecast_horizons_str = dash.range('B11').value or '1,3,6,12'
    try:
        forecast_horizons = [int(h.strip()) for h in str(forecast_horizons_str).split(',')]
    except:
        forecast_horizons = [1, 3, 6, 12]
    
    max_forecast_periods = int(dash.range('B12').value or 12)
    
    # Setup forecast sheet
    forecast_sheet.clear()
    forecast_sheet.range('A1').value = f"📈 FORECAST RESULTS - Top {top_n} Models per Variable"
    forecast_sheet.range('A1').font.bold = True
    forecast_sheet.range('A1').font.size = 14
    forecast_sheet.range('A1').color = (70, 130, 180)
    forecast_sheet.range('A1').font.color = (255, 255, 255)
    
    forecast_sheet.range('A2').value = f"Forecast Horizons: {','.join(map(str, forecast_horizons))}"
    forecast_sheet.range('A2').font.italic = True
    
    current_row = 4
    
    # Get date frequency for forecast dates
    date_diff = df[date_col].diff().median()
    if date_diff <= pd.Timedelta(days=7):
        freq = 'D'
    elif date_diff <= pd.Timedelta(days=10):
        freq = 'W'
    elif date_diff <= pd.Timedelta(days=40):
        freq = 'MS'  # Month start
    elif date_diff <= pd.Timedelta(days=120):
        freq = 'QS'  # Quarter start
    else:
        freq = 'YS'  # Year start
    
    # Generate forecasts for each target
    for target_info in selected_targets:
        target_col = target_info['name']
        
        if target_col not in df.columns:
            continue
        
        try:
            # Get full data (train + test)
            y_full = df[target_col].dropna().values
            dates_full = pd.to_datetime(df[date_col]).values
            
            if len(y_full) < 12:
                continue
            
            # Build lagged features for FULL dataset
            lags = [1, 3, 6, 12]
            max_lag = max(lags)
            
            X_all = []
            y_all_target = []
            valid_indices = []
            
            for i in range(max_lag, len(y_full)):
                features = [y_full[i - lag] for lag in lags]
                X_all.append(features)
                y_all_target.append(y_full[i])
                valid_indices.append(i)
            
            if len(X_all) == 0:
                continue
            
            # Train models on ALL data with proper lagged features
            model_predictions_by_h = {}  # {horizon: {model_name: predictions}}
            
            for horizon in forecast_horizons:  # Process all horizons
                model_predictions_by_h[horizon] = {}
                
                # Use top N models (try the most popular ones)
                models_to_train = ['Linear', 'Ridge', 'RandomForest', 'Naive', 'SeasonalNaive'][:top_n]
                
                for model_name in models_to_train:
                    try:
                        # Train on full data with lagged features
                        model = create_model(model_name)
                        if model is None:
                            continue
                        
                        # Train on all available history
                        model.fit(X_all, y_all_target)
                        
                        # Generate multi-step forecast up to max_periods
                        forecast = []
                        current_history = list(y_full[-12:])  # Keep last 12 values
                        
                        for step in range(min(horizon, max_forecast_periods)):
                            # Build features from current history
                            features = []
                            if len(current_history) >= max_lag:
                                features = [current_history[-lag] for lag in lags]
                            else:
                                # Fallback: pad with last value
                                features = [current_history[-1]] * len(lags)
                            
                            # Predict next value
                            next_val = model.predict_row(features)
                            forecast.append(next_val)
                            
                            # Update history
                            current_history.append(next_val)
                            if len(current_history) > 12:
                                current_history = current_history[-12:]
                        
                        model_predictions_by_h[horizon][model_name] = np.array(forecast)
                        
                    except Exception as e:
                        print(f"Forecast error for {model_name} h={horizon}: {e}")
                        continue
            
            # Write results to sheet
            if any(model_predictions_by_h.values()):
                # Get last date for reference
                last_date = dates_full[-1]
                
                forecast_sheet.range(f'A{current_row}').value = f"📊 {target_col}"
                forecast_sheet.range(f'A{current_row}').font.bold = True
                forecast_sheet.range(f'A{current_row}').font.size = 12
                forecast_sheet.range(f'A{current_row}').color = (220, 220, 220)
                
                current_row += 1
                forecast_sheet.range(f'A{current_row}').value = f"📅 Last observed date: {pd.Timestamp(last_date).strftime('%Y-%m-%d')}"
                forecast_sheet.range(f'A{current_row}').font.italic = True
                forecast_sheet.range(f'A{current_row}').color = (255, 255, 230)
                
                current_row += 1
                
                # Get forecast dates for display - show all periods!
                forecast_dates_list = []
                for horizon in sorted(model_predictions_by_h.keys()):
                    # Generate forecast dates
                    try:
                        forecast_dates = pd.date_range(start=last_date, periods=horizon+1, freq=freq)[1:]
                        forecast_dates_str = [d.strftime('%Y-%m-%d') for d in forecast_dates]
                        forecast_dates_list.append(forecast_dates_str)  # Show ALL periods!
                    except:
                        forecast_dates_list.append([f'Step {i+1}' for i in range(horizon)])
                
                # Headers with actual dates - show ALL periods for the largest horizon
                max_forecast_periods_display = max(len(dates) for dates in forecast_dates_list) if forecast_dates_list else 12
                headers = ['Horizon', 'Model'] + [f'Period {i+1}' for i in range(max_forecast_periods_display)]
                forecast_sheet.range(f'A{current_row}').value = [headers]
                forecast_sheet.range(f'A{current_row}:H{current_row}').font.bold = True
                forecast_sheet.range(f'A{current_row}:H{current_row}').color = (200, 200, 255)
                
                current_row += 1
                
                # Write forecasts for each horizon and model
                for idx, horizon in enumerate(sorted(model_predictions_by_h.keys())):
                    # Add date info row for this horizon
                    forecast_sheet.range(f'A{current_row}').value = [f'H={horizon} Periods']
                    forecast_sheet.range(f'A{current_row}').font.italic = True
                    forecast_sheet.range(f'A{current_row}:B{current_row}').merge()
                    current_row += 1
                    
                    # Add date row
                    dates_row = ['', f'Dates'] + forecast_dates_list[idx][:max_forecast_periods_display]
                    forecast_sheet.range(f'A{current_row}').value = dates_row
                    forecast_sheet.range(f'A{current_row}').font.size = 9
                    forecast_sheet.range(f'A{current_row}').font.italic = True
                    current_row += 1
                    
                    for model_name, forecast_vals in model_predictions_by_h[horizon].items():
                        # Pad forecast_vals to max_forecast_periods_display
                        padded_forecast = list(forecast_vals[:max_forecast_periods_display])
                        while len(padded_forecast) < max_forecast_periods_display:
                            padded_forecast.append('')
                        row_data = [horizon, model_name] + padded_forecast
                        forecast_sheet.range(f'A{current_row}').value = row_data
                        current_row += 1
                    
                    current_row += 1  # Extra space between horizons
                
                current_row += 2  # Space between variables
            
        except Exception as e:
            print(f"Error generating forecast for {target_col}: {e}")
            continue
    
    # Auto-fit columns
    try:
        forecast_sheet.range('A:G').columns.autofit()
    except:
        pass
    
    forecast_sheet.activate()
    dash.range('B33').value = f"✅ Forecast complete: {len(selected_targets)} variables × Top {top_n} models"
    
    return "✅ Forecast complete"


def save_custom_recipe():
    """Save current configuration as a new recipe JSON"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    config_sheet = wb.sheets['Recipe_Config']
    
    # Get recipe name from Recipe_Config (NEW LOCATION!)
    recipe_name = config_sheet.range('B4').value
    if not recipe_name:
        dash.range('B33').value = "⚠️ Enter recipe name in Recipe_Config cell B4"
        config_sheet.activate()
        config_sheet.range('B4').select()
        return "⚠️ No recipe name"
    
    # Get frequency from Dashboard
    frequency = dash.range('B4').value or 'Monthly'
    freq_template = get_frequency_template(frequency)
    
    # Get selected models
    selected_models = get_selected_models()
    if not selected_models:
        dash.range('B33').value = "⚠️ No models selected in Recipe_Config"
        return "⚠️ No models"
    
    # Get hyperparameters
    hyperparams = get_hyperparameters()
    
    # Get forecast settings (row 57 in new layout)
    horizons_str = config_sheet.range('B57').value or '1,3,6,12'
    try:
        horizons = [int(h.strip()) for h in str(horizons_str).split(',')]
    except:
        horizons = freq_template['horizons']
    
    # Get train/test dates from Recipe_Config (rows 58-62)
    train_start = str(config_sheet.range('B58').value or '2005-01-01')
    train_end = str(config_sheet.range('B59').value or '2019-12-31')
    test_start = str(config_sheet.range('B60').value or '2020-01-01')
    test_end = str(config_sheet.range('B61').value or '2024-12-31')
    date_col = str(config_sheet.range('B62').value or 'date')
    
    # Get data path from Dashboard
    data_path = str(dash.range('B31').value or '')
    
    # Build recipe dict in REPO format (like your other repos)
    recipe = {
        "run_name": recipe_name,
        "frequency": freq_template['code'],
        "strategy": "frozen",
        "train": {
            "start": train_start,
            "end": train_end
        },
        "test": {
            "start": test_start,
            "end": test_end
        },
        "data": {
            "path": data_path,
            "date_col": date_col
        },
        "models_filter": selected_models,  # Changed from selected_models
        "horizons": horizons,
        "model_configs": hyperparams,  # Changed from hyperparameters
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to custom recipes folder
    custom_recipe_dir = Path("/Users/schalkeanindya/SMFdashboard/custom_recipes")
    custom_recipe_dir.mkdir(exist_ok=True)
    
    save_path = custom_recipe_dir / f"{recipe_name}.json"
    
    try:
        with open(save_path, 'w') as f:
            json.dump(recipe, f, indent=2)
        
        dash.range('B33').value = f"✅ Recipe saved: {save_path.name}"
        return f"✅ Saved: {save_path.name}"
    except Exception as e:
        dash.range('B33').value = f"⚠️ Error saving: {str(e)[:50]}"
        return f"⚠️ Error: {e}"


# Button handlers
def btn_setup_recipe():
    """Button: Setup Recipe Dashboard"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    dash.range('B33').value = "⏳ Setting up recipe dashboard..."
    msg = setup_recipe_dashboard()
    dash.range('B33').value = msg
    return msg


def btn_generate_dummy_data():
    """Button: Generate Dummy Data"""
    wb = xw.Book.caller()
    msg = generate_dummy_recipe_data()
    return msg


def btn_apply_template():
    """Button: Apply Frequency Template"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    dash.range('B33').value = "⏳ Applying template..."
    msg = apply_frequency_template()
    return msg


def btn_load_data():
    """Button: Load Data"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    dash.range('B33').value = "⏳ Loading data..."
    msg = load_data_from_recipe()
    return msg


def btn_save_recipe():
    """Button: Save Recipe"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    dash.range('B33').value = "⏳ Saving recipe..."
    msg = save_custom_recipe()
    return msg


def btn_view_recipe():
    """Button: View Recipe Configuration"""
    wb = xw.Book.caller()
    wb.sheets['Recipe_Config'].activate()
    return "✅ Showing recipe configuration"


def run_recipe_backcast():
    """Run backcast validation for recipe models - WITH ACTUAL VS PREDICTED - using date-based splits"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    backcast_sheet = wb.sheets['Backcast_Results']
    data_view = wb.sheets['Data_View']
    config_sheet = wb.sheets['Recipe_Config']
    
    dash.range('B33').value = "⏳ Running backcast validation..."
    
    # Get data
    try:
        df = data_view.range('A3').options(pd.DataFrame, header=1, index=False, expand='table').value
        if df is None or len(df) == 0:
            dash.range('B33').value = "⚠️ No data loaded. Load Data first!"
            return "⚠️ No data"
    except:
        dash.range('B33').value = "⚠️ No data loaded. Load Data first!"
        return "⚠️ No data"
    
    # Get settings from config
    top_n = int(dash.range('B10').value or 3)
    
    # Read train/test dates from Recipe_Config (rows 58-62 in new layout)
    train_start = config_sheet.range('B58').value or '2005-01-01'
    train_end = config_sheet.range('B59').value or '2019-12-31'
    test_start = config_sheet.range('B60').value or '2020-01-01'
    test_end = config_sheet.range('B61').value or '2024-12-31'
    date_col_name = config_sheet.range('B62').value or 'date'
    
    # Get selected models from config
    selected_models = get_selected_models()
    if len(selected_models) == 0:
        dash.range('B33').value = "⚠️ No models selected. Check models in Recipe_Config!"
        return "⚠️ No models selected"
    
    # Get selected target variables
    selected_targets = get_selected_targets()
    if len(selected_targets) == 0:
        dash.range('B33').value = "⚠️ No target variables selected. Check targets in Recipe_Config!"
        return "⚠️ No targets selected"
    
    # Detect date column
    date_col = None
    for col in df.columns:
        if date_col_name.lower() in str(col).lower() or 'date' in str(col).lower():
            date_col = col
            break
    
    if date_col is None:
        date_col = df.columns[0]  # Fallback to first column
    
    # Convert date column to datetime
    try:
        df[date_col] = pd.to_datetime(df[date_col])
    except:
        dash.range('B33').value = f"⚠️ Could not parse date column: {date_col}"
        return "⚠️ Date parse error"
    
    # Run backcast
    backcast_sheet.clear()
    backcast_sheet.range('A1').value = f"🔍 BACKCAST VALIDATION - Top {top_n} Models per Variable (Date-based split)"
    backcast_sheet.range('A1').font.bold = True
    backcast_sheet.range('A1').font.size = 14
    backcast_sheet.range('A1').color = (70, 130, 180)
    backcast_sheet.range('A1').font.color = (255, 255, 255)
    
    backcast_sheet.range('A2').value = f"Train: {train_start} to {train_end} | Test: {test_start} to {test_end}"
    backcast_sheet.range('A2').font.italic = True
    
    current_row = 4
    
    # Filter data by train/test dates
    try:
        train_start_dt = pd.to_datetime(train_start)
        train_end_dt = pd.to_datetime(train_end)
        test_start_dt = pd.to_datetime(test_start)
        test_end_dt = pd.to_datetime(test_end)
    except:
        dash.range('B33').value = "⚠️ Invalid date format. Use YYYY-MM-DD"
        return "⚠️ Date format error"
    
    # Train actual models on each SELECTED target variable
    for target_info in selected_targets:
        target_col = target_info['name']
        
        # Check if target exists in data
        if target_col not in df.columns:
            continue
        
        try:
            # Split by dates
            train_mask = (df[date_col] >= train_start_dt) & (df[date_col] <= train_end_dt)
            test_mask = (df[date_col] >= test_start_dt) & (df[date_col] <= test_end_dt)
            
            df_train = df[train_mask].copy()
            df_test = df[test_mask].copy()
            
            if len(df_train) < 12 or len(df_test) < 1:  # Need minimum data
                continue
                
            y_train = df_train[target_col].dropna().values
            y_test = df_test[target_col].dropna().values
            dates_test = df_test[date_col].iloc[:len(y_test)]
            
            if len(y_train) < 12 or len(y_test) < 1:
                continue
            
            # Format dates properly
            dates_test_formatted = []
            for d in dates_test:
                try:
                    ts = pd.Timestamp(d)
                    dates_test_formatted.append(ts.date())
                except:
                    dates_test_formatted.append(str(d)[:10] if d else '')
            
            # Prepare features (simple lagged features for backcast)
            lags = [1, 3, 6, 12]  # Standard lags
            X_train = []
            y_train_lagged = []
            
            # Build lagged features for training
            max_lag = max(lags)
            for i in range(max_lag, len(y_train)):
                features = [y_train[i - lag] for lag in lags]
                X_train.append(features)
                y_train_lagged.append(y_train[i])
            
            # Build test features
            X_test = []
            # Use full y_train for building test features
            y_full_train = y_train.copy()
            for i in range(len(y_test)):
                # For each test point, use the most recent training values
                # This simulates a rolling forecast scenario
                features = []
                for lag in lags:
                    idx = len(y_full_train) - lag + i
                    if idx >= 0 and idx < len(y_full_train):
                        features.append(y_full_train[idx])
                    else:
                        features.append(y_full_train[-1])  # Fallback
                X_test.append(features)
            
            y_train_lagged = np.array(y_train_lagged)
            
            # Train models using CUSTOM MODEL LIBRARY
            models_predictions = {}
            
            for model_name in selected_models:  # Train all selected models
                try:
                    # Create model from registry
                    model = create_model(model_name)
                    if model is None:
                        continue  # Model not available
                    
                    # Fit model with lagged features
                    model.fit(X_train, y_train_lagged.tolist())
                    
                    # Predict on test set
                    pred = [model.predict_row(x) for x in X_test]
                    models_predictions[model_name] = np.array(pred)
                    
                except Exception as e:
                    print(f"Error training {model_name}: {e}")
                    import traceback
                    traceback.print_exc()
                    continue
        except Exception as e:
            print(f"Error processing {target_col}: {e}")
            continue
        
        # Calculate metrics and rank
        if len(models_predictions) == 0:
            continue  # Skip if no models trained successfully
        
        model_scores = []
        for model_name, pred in models_predictions.items():
            try:
                rmse = np.sqrt(np.mean((y_test - pred) ** 2))
                mae = np.mean(np.abs(y_test - pred))
                r2 = 1 - (np.sum((y_test - pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2))
                model_scores.append((model_name, rmse, mae, r2, pred))
            except:
                continue
        
        if len(model_scores) == 0:
            continue  # Skip if no valid scores
        
        # Sort by RMSE
        model_scores.sort(key=lambda x: x[1])
        
        # Write variable header
        backcast_sheet.range(f'A{current_row}').value = f"📊 {target_col}"
        backcast_sheet.range(f'A{current_row}').font.bold = True
        backcast_sheet.range(f'A{current_row}').font.size = 12
        backcast_sheet.range(f'A{current_row}').color = (220, 220, 220)
        
        # Performance metrics table
        backcast_sheet.range(f'A{current_row+1}').value = [
            ['Rank', 'Model', 'RMSE', 'MAE', 'R²']
        ]
        backcast_sheet.range(f'A{current_row+1}:E{current_row+1}').font.bold = True
        backcast_sheet.range(f'A{current_row+1}:E{current_row+1}').color = (200, 200, 255)
        
        # Top N models
        for i, (name, rmse, mae, r2, _) in enumerate(model_scores[:top_n], 1):
            backcast_sheet.range(f'A{current_row+1+i}').value = [i, name, rmse, mae, r2]
            if i == 1:  # Highlight best
                backcast_sheet.range(f'A{current_row+1+i}:E{current_row+1+i}').color = (200, 250, 200)
        
        # Actual vs Predicted table
        backcast_sheet.range(f'G{current_row+1}').value = "Actual vs Predicted (Top 3):"
        backcast_sheet.range(f'G{current_row+1}').font.bold = True
        
        headers = ['Date', 'Actual']
        for i in range(min(3, top_n)):
            headers.append(model_scores[i][0])
        
        backcast_sheet.range(f'G{current_row+2}').value = [headers]
        backcast_sheet.range(f'G{current_row+2}').expand('right').font.bold = True
        backcast_sheet.range(f'G{current_row+2}').expand('right').color = (200, 200, 255)
        
        # Write actual vs predicted values
        for j in range(len(y_test)):
            row_data = [dates_test_formatted[j], y_test[j]]
            for i in range(min(3, top_n)):
                row_data.append(model_scores[i][4][j])  # predicted value
            backcast_sheet.range(f'G{current_row+3+j}').value = row_data
        
        current_row += len(y_test) + 7
    
    # Column widths
    try:
        backcast_sheet.range('A:E').columns.autofit()
        backcast_sheet.range('G:M').columns.autofit()
    except:
        pass
    
    backcast_sheet.activate()
    dash.range('B33').value = f"✅ Backcast: {len(selected_targets)} variables × Top {top_n} models | Date-based split"
    
    return f"✅ Backcast complete"


def view_model_rankings():
    """Show consolidated model rankings across all variables"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    
    # Create or get Rankings sheet
    if 'Model_Rankings' not in [sheet.name for sheet in wb.sheets]:
        rankings_sheet = wb.sheets.add('Model_Rankings', after=dash)
    else:
        rankings_sheet = wb.sheets['Model_Rankings']
    
    rankings_sheet.clear()
    dash.range('B33').value = "⏳ Generating model rankings..."
    
    # Check if backcast has been run
    try:
        backcast_sheet = wb.sheets['Backcast_Results']
        # Try to read some data to verify backcast was run
        test_data = backcast_sheet.range('A1').value
        if not test_data:
            dash.range('B33').value = "⚠️ Run Backcast first to see rankings"
            rankings_sheet.activate()
            rankings_sheet.range('A1').value = "⚠️ Please run Backcast first to generate rankings"
            return "⚠️ No backcast data"
    except:
        dash.range('B33').value = "⚠️ Run Backcast first to see rankings"
        rankings_sheet.activate()
        rankings_sheet.range('A1').value = "⚠️ Please run Backcast first to generate rankings"
        return "⚠️ No backcast data"
    
    # Header
    rankings_sheet.range('A1').value = "🏆 MODEL RANKINGS - Summary Across All Variables"
    rankings_sheet.range('A1').font.bold = True
    rankings_sheet.range('A1').font.size = 14
    rankings_sheet.range('A1:F1').merge()
    rankings_sheet.range('A1').color = (70, 130, 180)
    rankings_sheet.range('A1').font.color = (255, 255, 255)
    rankings_sheet.range('A1').api.HorizontalAlignment = -4108
    
    rankings_sheet.range('A2').value = "Average performance across all variables (lower RMSE is better)"
    rankings_sheet.range('A2').font.italic = True
    rankings_sheet.range('A2:F2').merge()
    
    # Get data from Data_View to find variables
    data_view = wb.sheets['Data_View']
    try:
        df = data_view.range('A3').options(pd.DataFrame, header=1, index=False, expand='table').value
        if df is None:
            raise ValueError("No data")
        date_col = df.columns[0]
        numeric_cols = [col for col in df.columns if col != date_col]
    except:
        rankings_sheet.range('A4').value = "⚠️ No data found. Generate or load data first."
        rankings_sheet.activate()
        return "⚠️ No data"
    
    # Parse backcast results to extract model performance
    model_performances = {}  # {model_name: [rmse_list]}
    
    # Read from Backcast_Results sheet
    # Format: Variable header (A4), then metrics header (A5), then data rows (A6+)
    current_row = 4
    max_rows = 1000  # Safety limit
    
    while current_row < max_rows:
        try:
            # Look for variable header (📊 prefix or bold text)
            cell_val = backcast_sheet.range(f'A{current_row}').value
            
            # Check if this is a variable header (has 📊 or is bold/variable name)
            if not cell_val or (not '📊' in str(cell_val) and backcast_sheet.range(f'A{current_row}').font.bold == False):
                current_row += 1
                continue
            
            # Found variable header - next row is metrics header
            current_row += 1
            
            # Skip if not Rank/Model/RMSE header
            header_val = backcast_sheet.range(f'A{current_row}').value
            if 'Rank' not in str(header_val):
                current_row += 1
                continue
            
            # Now we're at the data rows - read model performance
            current_row += 1
            for i in range(10):  # Read up to 10 models
                rank_cell = backcast_sheet.range(f'A{current_row + i}').value
                
                # Stop if we hit next section or empty row
                if rank_cell is None:
                    break
                
                # Check if we've moved to next variable (📊 header)
                next_var_check = backcast_sheet.range(f'A{current_row + i + 1}').value
                if next_var_check and '📊' in str(next_var_check):
                    break
                
                try:
                    model_name = backcast_sheet.range(f'B{current_row + i}').value
                    rmse_val = backcast_sheet.range(f'C{current_row + i}').value
                    
                    if model_name and rmse_val is not None:
                        rmse = float(rmse_val)
                        if model_name not in model_performances:
                            model_performances[model_name] = []
                        model_performances[model_name].append(rmse)
                except:
                    continue
            
            # Move to next section (find next variable or end)
            current_row += 15  # Skip to likely next variable
            if current_row > 500:  # Safety check
                break
                
        except Exception as e:
            print(f"Error parsing row {current_row}: {e}")
            current_row += 1
            if current_row > 500:
                break
    
    if not model_performances:
        rankings_sheet.range('A4').value = "⚠️ Could not parse backcast results"
        rankings_sheet.activate()
        return "⚠️ Parse error"
    
    # Calculate average performance
    model_summary = []
    for model_name, rmse_list in model_performances.items():
        if len(rmse_list) == 0:
            continue  # Skip models with no valid RMSE values
        avg_rmse = np.mean(rmse_list)
        min_rmse = np.min(rmse_list)
        max_rmse = np.max(rmse_list)
        count = len(rmse_list)
        model_summary.append((model_name, avg_rmse, min_rmse, max_rmse, count))
    
    # Check if we have any valid models
    if len(model_summary) == 0:
        rankings_sheet.range('A4').value = "⚠️ No valid model performances found"
        rankings_sheet.activate()
        dash.range('B33').value = "⚠️ No valid rankings"
        return "⚠️ No valid data"
    
    # Sort by average RMSE
    model_summary.sort(key=lambda x: x[1])
    
    # Write summary table
    rankings_sheet.range('A4').value = [
        ['Rank', 'Model', 'Avg RMSE', 'Min RMSE', 'Max RMSE', 'Variables Tested']
    ]
    rankings_sheet.range('A4:F4').font.bold = True
    rankings_sheet.range('A4:F4').color = (200, 200, 255)
    
    for i, (model_name, avg_rmse, min_rmse, max_rmse, count) in enumerate(model_summary, 1):
        rankings_sheet.range(f'A{4+i}').value = [i, model_name, avg_rmse, min_rmse, max_rmse, count]
        
        # Highlight top 3
        if i == 1:
            rankings_sheet.range(f'A{4+i}:F{4+i}').color = (200, 250, 200)  # Green
        elif i == 2:
            rankings_sheet.range(f'A{4+i}:F{4+i}').color = (220, 250, 220)  # Light green
        elif i == 3:
            rankings_sheet.range(f'A{4+i}:F{4+i}').color = (240, 250, 240)  # Very light green
    
    # Format numbers
    try:
        rankings_sheet.range(f'C5:E{4+len(model_summary)}').number_format = '0.00'
    except:
        pass
    
    # Auto-fit columns
    try:
        rankings_sheet.range('A:F').columns.autofit()
    except:
        pass
    
    # Add note
    rankings_sheet.range(f'A{6+len(model_summary)}').value = "💡 Tip: Lower RMSE indicates better performance"
    rankings_sheet.range(f'A{6+len(model_summary)}').font.italic = True
    rankings_sheet.range(f'A{6+len(model_summary)}:F{6+len(model_summary)}').merge()
    rankings_sheet.range(f'A{6+len(model_summary)}').color = (255, 255, 230)
    
    rankings_sheet.activate()
    dash.range('B33').value = f"✅ Rankings: {len(model_summary)} models ranked by average RMSE"
    
    return f"✅ Rankings generated"


def build_lagged_features(y, lags=[1, 3, 6, 12], horizon=1):
    """
    Build proper lagged features for time series forecasting (like the other repo)
    Returns X (features at t), y_target (values at t+horizon), valid_indices
    
    Features at time i predict target at i+horizon
    """
    n = len(y)
    max_lag = max(lags) if lags else 0
    
    X = []
    y_target = []
    valid_indices = []
    
    for i in range(n):
        # Need: features at time i, target at time i+horizon
        target_idx = i + horizon
        
        # Skip if we don't have all lags or target not available
        if i < max_lag or target_idx >= n:
            continue
        
        # Check if target is valid (not NaN)
        if np.isnan(y[target_idx]):
            continue
        
        # Build feature row from lags
        features = []
        valid = True
        for lag in sorted(lags):
            lag_idx = i - lag
            if lag_idx < 0 or np.isnan(y[lag_idx]):
                valid = False
                break
            features.append(y[lag_idx])
        
        if not valid or len(features) == 0:
            continue
        
        X.append(features)
        y_target.append(y[target_idx])
        valid_indices.append(i)  # Origin time (when we make the forecast)
    
    return np.array(X), np.array(y_target), valid_indices


def refresh_recipe_charts():
    """Create forecast + backcast charts for EVERY variable (using PROPER time series features + horizons)"""
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    data_view = wb.sheets['Data_View']
    config_sheet = wb.sheets['Recipe_Config']
    
    # Clear old charts first
    try:
        for pic in list(dash.pictures):
            if pic.name.startswith('Chart_'):
                pic.delete()
    except:
        pass
    
    top_n = int(dash.range('B10').value or 3)
    dash.range('B33').value = f"⏳ Creating charts with PROPER time series features (like other repo)..."
    
    # Get data
    try:
        df = data_view.range('A3').options(pd.DataFrame, header=1, index=False, expand='table').value
        if df is None or len(df) == 0:
            dash.range('B33').value = "⚠️ No data loaded. Load Data first!"
            return "⚠️ No data"
    except:
        dash.range('B33').value = "⚠️ No data loaded. Load Data first!"
        return "⚠️ No data"
    
    # Get selected targets and models
    selected_targets = get_selected_targets()
    selected_models = get_selected_models()
    
    if len(selected_targets) == 0:
        dash.range('B33').value = "⚠️ No target variables selected!"
        return "⚠️ No targets"
    
    if len(selected_models) == 0:
        dash.range('B33').value = "⚠️ No models selected!"
        return "⚠️ No models"
    
    # Get train/test dates
    train_start = config_sheet.range('B58').value or '2005-01-01'
    train_end = config_sheet.range('B59').value or '2019-12-31'
    test_start = config_sheet.range('B60').value or '2020-01-01'
    test_end = config_sheet.range('B61').value or '2024-12-31'
    date_col_name = config_sheet.range('B62').value or 'date'
    # forecast_horizon removed - only backcast validation
    
    # Detect date column
    date_col = None
    for col in df.columns:
        if date_col_name.lower() in str(col).lower() or 'date' in str(col).lower():
            date_col = col
            break
    if date_col is None:
        date_col = df.columns[0]
    
    # Prepare dates
    df[date_col] = pd.to_datetime(df[date_col])
    
    # Parse train/test dates
    try:
        train_start_dt = pd.to_datetime(train_start)
        train_end_dt = pd.to_datetime(train_end)
        test_start_dt = pd.to_datetime(test_start)
        test_end_dt = pd.to_datetime(test_end)
    except:
        dash.range('B33').value = "⚠️ Invalid date format in config"
        return "⚠️ Date error"
    
    # Create charts for each SELECTED variable
    # Dynamic spacing: closer together when fewer charts, more spread when many
    num_charts = len(selected_targets)
    if num_charts <= 3:
        chart_spacing = 18  # Compact spacing for 1-3 charts
    elif num_charts <= 6:
        chart_spacing = 22  # Medium spacing for 4-6 charts
    elif num_charts <= 10:
        chart_spacing = 26  # Normal spacing for 7-10 charts
    else:
        chart_spacing = 30  # More spacing for many charts
    
    row_position = 30  # Starting position
    
    dash.range('B33').value = f"⏳ Creating {num_charts} charts with dynamic spacing..."
    
    for var_idx, target_info in enumerate(selected_targets):
        target_col = target_info['name']
        
        # Check if target exists in data
        if target_col not in df.columns:
            continue
        
        try:
            # Split data by dates
            train_mask = (df[date_col] >= train_start_dt) & (df[date_col] <= train_end_dt)
            test_mask = (df[date_col] >= test_start_dt) & (df[date_col] <= test_end_dt)
            
            df_train = df[train_mask].copy()
            df_test = df[test_mask].copy()
            
            if len(df_train) < 12 or len(df_test) < 1:
                continue
            
            # Build PROPER lagged features for backcast (h=1 for simplicity in charts)
            # Use target column's horizons from config
            lags = [1, 3, 6, 12]  # Standard lags like other repo
            horizon = target_info.get('horizons', [1])[0] if target_info.get('horizons') else 1
            
            # Get full series
            y_full = df[target_col].values
            all_dates = pd.to_datetime(df[date_col])
            
            # Build features for entire dataset
            X_full, y_full_target, valid_idx = build_lagged_features(y_full, lags=lags, horizon=horizon)
            
            if len(X_full) == 0 or len(y_full_target) == 0:
                continue
            
            # Split into train/test based on dates
            dates_full = all_dates.iloc[valid_idx].values
            train_mask = (dates_full >= pd.Timestamp(train_start)) & (dates_full <= pd.Timestamp(train_end))
            test_mask = (dates_full >= pd.Timestamp(test_start)) & (dates_full <= pd.Timestamp(test_end))
            
            X_train = X_full[train_mask]
            y_train = y_full_target[train_mask]
            X_test = X_full[test_mask]
            y_test = y_full_target[test_mask]
            dates_test = dates_full[test_mask]
            
            if len(X_train) < 12 or len(X_test) < 1:
                continue
            
            # Generate backcast predictions using CUSTOM MODEL LIBRARY
            backcast_preds = {}
            
            for model_name in selected_models:  # Train all selected models
                try:
                    # Create model from registry
                    model = create_model(model_name)
                    if model is None:
                        continue  # Model not available
                    
                    # Fit model with lagged features
                    model.fit(X_train.tolist(), y_train.tolist())
                    
                    # Predict on test set
                    pred = [model.predict_row(x) for x in X_test.tolist()]
                    backcast_preds[model_name] = np.array(pred)
                    
                except Exception as e:
                    print(f"Chart - Error training {model_name}: {e}")
                    continue
            
            # Calculate RMSE and get top N
            if len(backcast_preds) == 0:
                continue  # Skip if no models trained
            
            model_scores = []
            for model_name, pred in backcast_preds.items():
                try:
                    rmse = np.sqrt(np.mean((y_test - pred) ** 2))
                    model_scores.append((model_name, rmse, pred))
                except:
                    continue
            
            if len(model_scores) == 0:
                continue
            
            model_scores.sort(key=lambda x: x[1])
            
            # FORECAST REMOVED - Only backcast validation charts now
            
            # Create TWO-PANEL chart: Backcast + Forecast
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))
            
            # LEFT: Backcast Validation
            ax1.plot(dates_test, y_test, 'o-', linewidth=3, 
                    markersize=6, label='Actual', color='black', alpha=0.8, zorder=10)
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#96CEB4']
            for i, (name, rmse, pred) in enumerate(model_scores[:top_n]):
                ax1.plot(dates_test, pred, 's--', linewidth=2, 
                        markersize=4, label=f'{name} (RMSE:{rmse:.2f})', 
                        color=colors[i % len(colors)], alpha=0.7)
            
            ax1.set_xlabel('Date', fontsize=10, fontweight='bold')
            ax1.set_ylabel(target_col, fontsize=10, fontweight='bold')
            ax1.set_title(f'🔍 Backcast: {target_col[:40]}', 
                         fontsize=11, fontweight='bold', pad=10)
            ax1.legend(loc='best', frameon=True, shadow=True, fontsize=8)
            ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            
            # Better date formatting for backcast
            import matplotlib.dates as mdates
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
            
            # RIGHT: Generate Forecast INLINE (not from sheet)
            forecast_values = {}
            forecast_dates = []
            
            try:
                # Use the SAME logic as run_recipe_forecast
                y_full = df[target_col].dropna().values
                
                if len(y_full) >= 12:
                    # Build lagged features for full dataset
                    lags = [1, 3, 6, 12]
                    max_lag = max(lags)
                    
                    X_all = []
                    y_all_target = []
                    
                    for i in range(max_lag, len(y_full)):
                        features = [y_full[i - lag] for lag in lags]
                        X_all.append(features)
                        y_all_target.append(y_full[i])
                    
                    # Get forecast settings from Dashboard
                    horizons_str = dash.range('B11').value or '1,3,6,12'
                    try:
                        forecast_horizons = [int(h.strip()) for h in str(horizons_str).split(',')]
                    except:
                        forecast_horizons = [1, 3, 6, 12]
                    
                    max_periods = int(dash.range('B12').value or 12)
                    
                    # Train top N models and generate forecasts
                    models_to_train = ['Linear', 'Ridge', 'RandomForest', 'Naive', 'SeasonalNaive'][:top_n]
                    
                    for model_name in models_to_train:
                        try:
                            model = create_model(model_name)
                            if model is None:
                                continue
                            
                            # Train on all data
                            model.fit(X_all, y_all_target)
                            
                            # Generate multi-step forecast
                            forecast = []
                            current_history = list(y_full[-12:])
                            
                            for step in range(min(max_periods, max(forecast_horizons))):
                                features = []
                                if len(current_history) >= max_lag:
                                    features = [current_history[-lag] for lag in lags]
                                else:
                                    features = [current_history[-1]] * len(lags)
                                
                                next_val = model.predict_row(features)
                                forecast.append(next_val)
                                current_history.append(next_val)
                                if len(current_history) > 12:
                                    current_history = current_history[-12:]
                            
                            forecast_values[model_name] = np.array(forecast)
                        except:
                            continue
                    
                    # Generate forecast dates
                    last_date = dates_full[-1]
                    date_diff = df[date_col].diff().median()
                    if date_diff <= pd.Timedelta(days=7):
                        freq = 'D'
                    elif date_diff <= pd.Timedelta(days=10):
                        freq = 'W'
                    elif date_diff <= pd.Timedelta(days=40):
                        freq = 'MS'
                    elif date_diff <= pd.Timedelta(days=120):
                        freq = 'QS'
                    else:
                        freq = 'YS'
                    
                    try:
                        forecast_dates = pd.date_range(start=last_date, periods=max_periods+1, freq=freq)[1:]
                    except:
                        # Fallback: simple date progression
                        from datetime import timedelta
                        forecast_dates = []
                        for i in range(max_periods):
                            forecast_dates.append(last_date + timedelta(days=30*i))
            except Exception as e:
                print(f"Error generating forecast chart: {e}")
                forecast_values = {}
            
            if forecast_values and len(forecast_dates) > 0:
                # Plot historical data
                hist_limit = min(24, len(df))
                hist_dates = df[date_col].iloc[-hist_limit:].values
                hist_values = df[target_col].iloc[-hist_limit:].values
                
                ax2.plot(hist_dates, hist_values, 
                        'o-', linewidth=2.5, markersize=4, label='Historical', 
                        color='black', alpha=0.8, zorder=10)
                
                # Add vertical line at forecast start
                last_date = hist_dates[-1] if len(hist_dates) > 0 else pd.Timestamp.now()
                ax2.axvline(x=last_date, color='red', linestyle=':', 
                           linewidth=2, alpha=0.6, label='Forecast Start')
                
                # Plot forecasts
                for i, (model_name, forecast_vals) in enumerate(list(forecast_values.items())[:top_n]):
                    # Only plot available forecast periods
                    num_forecast_periods = min(len(forecast_vals), len(forecast_dates))
                    if num_forecast_periods > 0:
                        ax2.plot(forecast_dates[:num_forecast_periods], forecast_vals[:num_forecast_periods], 
                                's--', linewidth=2, markersize=4, 
                                label=f'{model_name} Forecast', 
                                color=colors[i % len(colors)], alpha=0.7)
            else:
                # No forecast data yet - show placeholder
                ax2.text(0.5, 0.5, 'Run Forecast\nto see predictions', 
                        ha='center', va='center', fontsize=12, color='gray',
                        transform=ax2.transAxes)
            
            ax2.set_xlabel('Date', fontsize=10, fontweight='bold')
            ax2.set_ylabel(target_col, fontsize=10, fontweight='bold')
            ax2.set_title(f'📈 Forecast: {target_col[:40]}', 
                         fontsize=11, fontweight='bold', pad=10)
            ax2.legend(loc='best', frameon=True, shadow=True, fontsize=8)
            ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax2.xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
            
            plt.tight_layout()
            
            # Place on dashboard with better error handling
            try:
                chart_name = f'Chart_{target_col.replace(" ", "_").replace("/", "_")}'
                
                # Remove old chart if exists
                for pic in list(dash.pictures):
                    try:
                        if pic.name == chart_name:
                            pic.delete()
                    except:
                        continue
                
                # Add new chart (two panels: backcast + forecast)
                dash.pictures.add(fig, 
                                 name=chart_name,
                                 left=dash.range(f'A{row_position}').left,
                                 top=dash.range(f'A{row_position}').top,
                                 width=900,  # Wider for two panels
                                 height=280)  # Good height for visibility
                
                dash.range('B33').value = f"⏳ Created chart {var_idx+1}/{len(selected_targets)}: {target_col}"
                
            except Exception as e:
                print(f"Error placing chart for {target_col}: {e}")
                dash.range('B33').value = f"⚠️ Chart error: {target_col} - {str(e)[:30]}"
            finally:
                plt.close(fig)
            
            row_position += chart_spacing  # Dynamic spacing based on number of charts
            
        except Exception as e:
            print(f"Error creating chart for {target_col}: {e}")
            dash.range('B33').value = f"⚠️ Error: {target_col} - {str(e)[:50]}"
            continue
    
    dash.activate()
    dash.range('B33').value = f"✅ Created {len(selected_targets)} charts (backcast + forecast) | Top {top_n} models"
    
    return f"✅ Charts created"


def load_precomputed_model_list(variable, frequency, top_n=3):
    """
    Load top N precomputed models for a variable from detailed Excel files.
    Returns list of dicts with model info: {model_name, rmse, mae, config}
    """
    freq_to_file = {
        'monthly': 'forecasting_results_Monthly_detailed.xlsx',
        'quarterly': 'forecasting_results_Quarterly_detailed.xlsx',
        'yearly': 'forecasting_results_Yearly_detailed.xlsx',
        'semesterly': 'forecasting_results_Semesterly_detailed.xlsx',
    }
    
    excel_file = freq_to_file.get(str(frequency).lower())
    if not excel_file:
        return []
    
    file_path = os.path.join('/Users/schalkeanindya/SMFdashboard/FINAL_EXCEL_REPORTS', excel_file)
    if not os.path.exists(file_path):
        return []
    
    try:
        import pandas as pd
        df = pd.read_excel(file_path)
        
        # Find variable name column
        var_col = None
        for col in ['Variable', 'variable', 'target', 'Target', 'Y Variable']:
            if col in df.columns:
                var_col = col
                break
        if not var_col:
            return []
        
        # Find RMSE column
        rmse_col = None
        for col in ['RMSE', 'rmse', 'RMSE@H=1', 'test_rmse']:
            if col in df.columns:
                rmse_col = col
                break
        if not rmse_col:
            return []
        
        # Filter for variable
        var_data = df[df[var_col].astype(str) == str(variable)]
        if len(var_data) == 0:
            return []
        
        # Sort by RMSE and get top N
        var_data_sorted = var_data.sort_values(rmse_col).head(top_n)
        
        # Debug: print columns to see what we're working with
        print(f"DEBUG - Columns: {df.columns.tolist()}")
        print(f"DEBUG - First row: {var_data_sorted.iloc[0]}")
        
        # Build result list
        models = []
        for idx, row in var_data_sorted.iterrows():
            # Try multiple possible model name columns
            model_name = ''
            
            # First, try common model column names
            for col_name in ['Model', 'model_name', 'Model Type', 'plugin', 'Plugin', 'model', 'Member', 'member']:
                if col_name in df.columns:
                    val = row.get(col_name)
                    if val is not None:
                        model_name = str(val).strip()
                        if model_name and model_name != 'nan' and model_name.lower() != 'none':
                            break
            
            # If no model name found, try to extract from ID/Member column
            if not model_name:
                # Look for columns with ID or member information
                for col in df.columns:
                    if 'id' in col.lower() or 'member' in col.lower() or 'variant' in col.lower():
                        val = row.get(col)
                        if val is not None:
                            # Try to extract model type from ID (e.g., "XGBoost-1459..." -> "XGBoost")
                            id_str = str(val).strip()
                            if '-' in id_str:
                                model_name = id_str.split('-')[0]
                            else:
                                model_name = id_str
                            if model_name:
                                break
            
            # Last resort: use indices as fallback but try to get ANY info
            if not model_name:
                # Print what we have to debug
                print(f"DEBUG - Row data: {row.to_dict()}")
                model_name = f"Model_{idx}"  # Fallback
            
            model_info = {
                'model_name': model_name or f'Unknown_{idx}',
                'rmse': float(row.get(rmse_col, 0)),
                'mae': float(row.get('MAE', 0)) if 'MAE' in df.columns else 0.0,
                'r2': float(row.get('R²', 0)) if 'R²' in df.columns else (float(row.get('R2', 0)) if 'R2' in df.columns else 0.0),
            }
            models.append(model_info)
        
        return models
    except Exception as e:
        print(f"Error loading precomputed models: {e}")
        return []


def show_precomputed_best_models():
    """Show best models from precomputed Excel files based on user selection"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    
    # Get selected variables (columns D-E, rows 11-20)
    selected_vars = []
    for row in range(11, 21):
        checkbox = dash.range(f'D{row}').value
        if checkbox == '✓':
            var_name = dash.range(f'E{row}').value
            if var_name:
                selected_vars.append(var_name)
    
    # Get selected frequencies (columns F-G, rows 11-16)
    selected_freqs = []
    for row in range(11, 17):
        checkbox = dash.range(f'F{row}').value
        if checkbox == '✓':
            freq = dash.range(f'G{row}').value
            if freq:
                selected_freqs.append(freq)
    
    if not selected_vars or not selected_freqs:
        dash.range('B33').value = "⚠️ Please select variables and frequencies first"
        return "⚠️ No selection"
    
    dash.range('B33').value = "⏳ Loading precomputed results..."
    
    # Create or get Results sheet
    if 'Precomputed_Results' not in [s.name for s in wb.sheets]:
        results_sheet = wb.sheets.add('Precomputed_Results', after=dash)
    else:
        results_sheet = wb.sheets['Precomputed_Results']
    
    results_sheet.clear()
    
    # Frequency to file mapping
    freq_to_file = {
        'monthly': 'forecasting_results_Monthly_detailed.xlsx',
        'quarterly': 'forecasting_results_Quarterly_detailed.xlsx',
        'yearly': 'forecasting_results_Yearly_detailed.xlsx',
        'semesterly': 'forecasting_results_Semesterly_detailed.xlsx',
        'weekly': None  # No weekly detailed file yet
    }
    
    current_row = 1
    results_sheet.range('A1').value = "🏆 PRE-COMPUTED BEST MODELS"
    results_sheet.range('A1').font.bold = True
    results_sheet.range('A1').font.size = 14
    results_sheet.range('A1:F1').merge()
    results_sheet.range('A1').color = (70, 130, 180)
    results_sheet.range('A1').font.color = (255, 255, 255)
    current_row = 3
    
    for freq in selected_freqs:
        excel_file = freq_to_file.get(freq.lower())
        if not excel_file:
            continue
            
        file_path = os.path.join('/Users/schalkeanindya/SMFdashboard/FINAL_EXCEL_REPORTS', excel_file)
        if not os.path.exists(file_path):
            results_sheet.range(f'A{current_row}').value = f"⚠️ {freq.capitalize()} results file not found"
            current_row += 2
            continue
        
        # Read Excel file
        try:
            import pandas as pd
            df = pd.read_excel(file_path)
            
            # Display frequency header
            results_sheet.range(f'A{current_row}').value = f"📊 {freq.upper()} FREQUENCY"
            results_sheet.range(f'A{current_row}').font.bold = True
            results_sheet.range(f'A{current_row}').font.size = 12
            results_sheet.range(f'A{current_row}').color = (220, 220, 220)
            current_row += 1
            
            # Get available columns
            available_columns = df.columns.tolist()
            
            # Find variable name column (try common names)
            var_col = None
            for col in ['Variable', 'variable', 'target', 'Target', 'Y Variable']:
                if col in available_columns:
                    var_col = col
                    break
            
            # For each selected variable, find best models
            for var in selected_vars:
                # Filter data for this variable
                var_data = df[df[var_col] == var] if var_col else df[df.iloc[:, 0] == var]
                
                if len(var_data) == 0:
                    continue
                
                # Find RMSE column
                rmse_col = None
                for col in ['RMSE', 'rmse', 'RMSE@H=1', 'test_rmse']:
                    if col in available_columns:
                        rmse_col = col
                        break
                
                if not rmse_col:
                    continue
                
                # Sort by RMSE (lower is better)
                var_data_sorted = var_data.sort_values(rmse_col)
                
                # Display top 5 models for this variable
                results_sheet.range(f'A{current_row}').value = f"🏆 {var}"
                results_sheet.range(f'A{current_row}').font.bold = True
                results_sheet.range(f'A{current_row}').color = (220, 240, 255)
                current_row += 1
                
                # Header row
                headers = ['Rank', 'Model']
                if 'Strategy' in available_columns:
                    headers.append('Strategy')
                headers.extend([rmse_col, 'MAE', 'R²'])
                
                results_sheet.range(f'A{current_row}').value = [headers]
                results_sheet.range(f'A{current_row}').expand('right').font.bold = True
                results_sheet.range(f'A{current_row}').expand('right').color = (200, 220, 255)
                current_row += 1
                
                # Top 5 models
                for rank, (idx, row) in enumerate(var_data_sorted.head(5).iterrows(), 1):
                    row_data = [rank]
                    if 'Model' in available_columns:
                        row_data.append(row.get('Model', ''))
                    elif 'model_name' in available_columns:
                        row_data.append(row.get('model_name', ''))
                    else:
                        row_data.append(row.iloc[1] if len(row) > 1 else '')
                    
                    if 'Strategy' in available_columns:
                        row_data.append(row.get('Strategy', ''))
                    
                    row_data.append(row.get(rmse_col, ''))
                    row_data.append(row.get('MAE', ''))
                    row_data.append(row.get('R²', ''))
                    
                    results_sheet.range(f'A{current_row}').value = [row_data]
                    
                    # Highlight best model
                    if rank == 1:
                        results_sheet.range(f'A{current_row}').expand('right').color = (200, 255, 200)
                    
                    current_row += 1
                
                current_row += 1  # Space between variables
            
            current_row += 1  # Space between frequencies
            
        except Exception as e:
            results_sheet.range(f'A{current_row}').value = f"⚠️ Error reading {freq} file: {str(e)[:50]}"
            current_row += 2
            continue
    
    results_sheet.activate()
    dash.range('B33').value = f"✅ Loaded precomputed results for {len(selected_vars)} variables × {len(selected_freqs)} frequencies"
    
    return "✅ Results displayed"


def btn_show_best_models():
    """Button: Show Best Models from Precomputed Results"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = show_precomputed_best_models()
    return msg


def show_precomputed_backcast_results():
    """Populate Backcast_Results with precomputed detailed results based on user selections."""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    
    # Ensure Backcast_Results sheet exists
    if 'Backcast_Results' not in [s.name for s in wb.sheets]:
        backcast_sheet = wb.sheets.add('Backcast_Results', after=dash)
    else:
        backcast_sheet = wb.sheets['Backcast_Results']
    backcast_sheet.clear()
    
    # Read selections from Dashboard (updated columns)
    selected_vars = []
    for row in range(11, 21):
        if dash.range(f'D{row}').value == '✓':
            var_name = dash.range(f'E{row}').value
            if var_name:
                selected_vars.append(var_name)
    
    selected_freqs = []
    for row in range(11, 17):
        if dash.range(f'F{row}').value == '✓':
            freq = dash.range(f'G{row}').value
            if freq:
                selected_freqs.append(freq)
    
    if not selected_vars or not selected_freqs:
        dash.range('B33').value = "⚠️ Please select variables and frequencies first"
        return "⚠️ No selection"
    
    dash.range('B33').value = "⏳ Loading precomputed detailed results into Backcast_Results..."
    
    # Frequency mapping
    freq_to_file = {
        'monthly': 'forecasting_results_Monthly_detailed.xlsx',
        'quarterly': 'forecasting_results_Quarterly_detailed.xlsx',
        'yearly': 'forecasting_results_Yearly_detailed.xlsx',
        'semesterly': 'forecasting_results_Semesterly_detailed.xlsx',
        'weekly': None,
    }
    base_dir = '/Users/schalkeanindya/SMFdashboard/FINAL_EXCEL_REPORTS'
    
    # Header
    backcast_sheet.range('A1').value = "📘 PRECOMPUTED BACKCAST RESULTS"
    backcast_sheet.range('A1').font.bold = True
    backcast_sheet.range('A1').font.size = 14
    backcast_sheet.range('A1:H1').merge()
    backcast_sheet.range('A1').color = (70, 130, 180)
    backcast_sheet.range('A1').font.color = (255, 255, 255)
    current_row = 3
    
    import pandas as pd
    
    for freq in selected_freqs:
        freq_row = 3  # Track row for this frequency
        excel_file = freq_to_file.get(str(freq).lower())
        if not excel_file:
            continue
        file_path = os.path.join(base_dir, excel_file)
        if not os.path.exists(file_path):
            backcast_sheet.range(f'A{current_row}').value = f"⚠️ {freq} detailed file not found"
            current_row += 2
            continue
        
        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            backcast_sheet.range(f'A{current_row}').value = f"⚠️ Error reading {excel_file}: {str(e)[:80]}"
            current_row += 2
            continue
        
        # Try to detect columns
        cols = df.columns.tolist()
        var_col = None
        for c in ['Variable', 'variable', 'Target', 'target', 'Y Variable']:
            if c in cols:
                var_col = c
                break
        rmse_col = None
        for c in ['RMSE', 'rmse', 'RMSE@H=1', 'test_rmse']:
            if c in cols:
                rmse_col = c
                break
        mae_col = 'MAE' if 'MAE' in cols else ('mae' if 'mae' in cols else None)
        r2_col = 'R²' if 'R²' in cols else ('R2' if 'R2' in cols else ('r2' if 'r2' in cols else None))
        
        # Try to find model column with multiple possible names
        model_col = None
        for c in ['Model', 'model_name', 'Model Type', 'plugin', 'Plugin', 'model', 'Member', 'member', 'Model_Name', 'Type']:
            if c in cols:
                model_col = c
                break
        
        strategy_col = 'Strategy' if 'Strategy' in cols else None
        
        # Debug: show what columns we found
        print(f"🔍 Detected columns: model_col={model_col}, rmse_col={rmse_col}, mae_col={mae_col}, r2_col={r2_col}")
        print(f"📋 All columns: {cols[:10]}...")
        
        # Frequency header
        backcast_sheet.range(f'A{current_row}').value = f"📊 {str(freq).upper()}"
        backcast_sheet.range(f'A{current_row}').font.bold = True
        backcast_sheet.range(f'A{current_row}').color = (220, 220, 220)
        current_row += 1
        
        # Store all variable data
        var_data_list = []
        
        for var_idx, var in enumerate(selected_vars):
            # Filter for variable
            if var_col:
                var_df = df[df[var_col].astype(str) == str(var)]
            else:
                var_df = df[df.iloc[:, 0].astype(str) == str(var)]
            if len(var_df) == 0:
                continue
            
            # Filter to show only rows where RMSE is NOT null
            if rmse_col and rmse_col in var_df.columns:
                var_df = var_df[var_df[rmse_col].notna()]
            
            if len(var_df) == 0:
                continue
            
            # Sort by RMSE if available
            if rmse_col and rmse_col in var_df.columns:
                var_df_sorted = var_df.sort_values(rmse_col)
            else:
                var_df_sorted = var_df.copy()
            
            var_data_list.append({
                'var': var,
                'var_idx': var_idx,
                'data': var_df_sorted,
                # A=65, M=77 (skip to M for second variable)
                'start_col': chr(65 + (var_idx * 12))  # Skip 12 columns for each variable
            })
        
        # First pass: show rankings side-by-side
        for var_info in var_data_list:
            var = var_info['var']
            var_idx = var_info['var_idx']
            var_df_sorted = var_info['data']
            var_start_col = var_info['start_col']
            
            # Use current_row to place horizontally (all variables start at same row)
            display_row = current_row
            
            # Section header (horizontal placement)
            backcast_sheet.range(f'{var_start_col}{display_row}').value = f"📊 {var}"
            backcast_sheet.range(f'{var_start_col}{display_row}').font.bold = True
            backcast_sheet.range(f'{var_start_col}{display_row}').font.size = 12
            backcast_sheet.range(f'{var_start_col}{display_row}').color = (240, 248, 255)
            display_row += 1
            
            # Group by model and get best RMSE for each unique model
            unique_models = {}
            for _, r in var_df_sorted.iterrows():
                # Extract model name with multiple fallbacks
                model_name = 'Unknown'
                if model_col:
                    model_name = str(r.get(model_col, 'Unknown')).strip()
                    if model_name == 'Unknown' or model_name == 'nan' or model_name == '':
                        model_name = 'Unknown'
                
                # If still unknown, try to extract from other columns
                if model_name == 'Unknown':
                    # Try Model_ID column (e.g., "Naive-955-v55-085910" -> "Naive")
                    for col in var_df_sorted.columns:
                        if 'id' in col.lower() or 'member' in col.lower():
                            id_val = r.get(col)
                            if pd.notna(id_val):
                                id_str = str(id_val).strip()
                                if '-' in id_str:
                                    model_name = id_str.split('-')[0]
                                    break
                
                rmse_val = r.get(rmse_col, None)
                if rmse_val is None or pd.isna(rmse_val):
                    continue
                
                # Keep the first (best) RMSE for each model
                if model_name not in unique_models:
                    unique_models[model_name] = r
            
            # Sort unique models by RMSE
            models_list = list(unique_models.items())
            if rmse_col:
                models_list.sort(key=lambda x: float(x[1].get(rmse_col, float('inf'))))
            
            # Summary (Top N = 5 unique models)
            headers = ['Rank', 'Model Name']
            if strategy_col: headers.append('Strategy')
            if rmse_col: headers.append(rmse_col)
            if mae_col: headers.append(mae_col)
            # R² removed (many missing)
            backcast_sheet.range(f'{var_start_col}{display_row}').value = [headers]
            backcast_sheet.range(f'{var_start_col}{display_row}').expand('right').font.bold = True
            backcast_sheet.range(f'{var_start_col}{display_row}').expand('right').color = (200, 220, 255)
            display_row += 1
            
            for rank, (model_name, r) in enumerate(models_list[:5], 1):
                row_vals = [rank, model_name]
                if strategy_col: row_vals.append(r.get(strategy_col, ''))
                if rmse_col: 
                    rmse_val = r.get(rmse_col, '')
                    row_vals.append(rmse_val if pd.notna(rmse_val) else '')
                if mae_col: 
                    mae_val = r.get(mae_col, '')
                    row_vals.append(mae_val if pd.notna(mae_val) else '')
                # R² removed
                
                backcast_sheet.range(f'{var_start_col}{display_row}').value = [row_vals]
                if rank == 1:
                    backcast_sheet.range(f'{var_start_col}{display_row}').expand('right').color = (200, 255, 200)
                display_row += 1
            
            # Track the maximum row used across all variables for next frequency section
            if display_row > freq_row:
                freq_row = display_row
        
        # After rankings, find max row and continue with detailed results below
        current_row = freq_row + 2
        
        # Second pass: show detailed results side-by-side
        for var_info in var_data_list:
            var = var_info['var']
            var_start_col = var_info['start_col']
            var_df_sorted = var_info['data']
            
            detailed_row = current_row
            backcast_sheet.range(f'{var_start_col}{detailed_row}').value = "📄 Detailed"
            backcast_sheet.range(f'{var_start_col}{detailed_row}').font.bold = True
            backcast_sheet.range(f'{var_start_col}{detailed_row}').font.italic = True
            detailed_row += 1
            
            try:
                # Show key columns: Model, Horizon, RMSE, MAE, Forecast, Actual
                key_cols = []
                if model_col: key_cols.append(model_col)
                if 'Horizon' in var_df_sorted.columns: key_cols.append('Horizon')
                if rmse_col: key_cols.append(rmse_col)
                if mae_col: key_cols.append(mae_col)
                
                # Add forecast and actual columns if they exist
                for col in var_df_sorted.columns:
                    if 'forecast' in col.lower() and col not in key_cols:
                        key_cols.append(col)
                    if 'actual' in col.lower() and col not in key_cols:
                        key_cols.append(col)
                
                if key_cols:
                    backcast_sheet.range(f'{var_start_col}{detailed_row}').value = [key_cols]
                    backcast_sheet.range(f'{var_start_col}{detailed_row}').expand('right').font.bold = True
                    backcast_sheet.range(f'{var_start_col}{detailed_row}').expand('right').color = (220, 230, 240)
                    detailed_row += 1
                    
                    # Show ALL rows (not limited)
                    for _, rr in var_df_sorted.iterrows():
                        row_data = []
                        for col in key_cols:
                            val = rr.get(col)
                            if pd.notna(val):
                                # Format numbers with comma as decimal separator
                                if isinstance(val, (int, float)):
                                    row_data.append(f"{val:.6f}".replace('.', ','))
                                else:
                                    row_data.append(str(val))
                            else:
                                row_data.append('')
                        backcast_sheet.range(f'{var_start_col}{detailed_row}').value = [row_data]
                        detailed_row += 1
                    
                    if detailed_row > freq_row:
                        freq_row = detailed_row
            except Exception as e:
                backcast_sheet.range(f'{var_start_col}{detailed_row}').value = f"⚠️ Error: {str(e)[:50]}"
                detailed_row += 1
                if detailed_row > freq_row:
                    freq_row = detailed_row
        
        # Advance to next frequency section
        current_row = freq_row + 3
    
    try:
        # Autofit all columns up to where variables are placed
        max_col_idx = 65 + (len(selected_vars) * 6)
        if max_col_idx > 90:  # More than Z
            cols = 'A:Z'
        else:
            cols = f'A:{chr(max_col_idx)}'
        backcast_sheet.range(cols).columns.autofit()
    except:
        pass
    
    backcast_sheet.activate()
    dash.range('B33').value = "✅ Precomputed detailed results shown in Backcast_Results"
    return "✅ Precomputed backcast displayed"


def btn_show_precomputed_backcast():
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = show_precomputed_backcast_results()
    return msg


def btn_recipe_backcast():
    """Button: Run Backcast with Recipe"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = run_recipe_backcast()
    return msg


def btn_refresh_charts():
    """Button: Refresh Charts"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = refresh_recipe_charts()
    return msg


def btn_view_rankings():
    """Button: View Model Rankings"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = view_model_rankings()
    return msg


def btn_recipe_forecast():
    """Button: Run Forecast with Top N Models"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = run_recipe_forecast()
    return msg


def btn_forecast_with_precomputed():
    """Button: Run Forecast with Precomputed Models (NO training)"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    msg = run_forecast_with_precomputed_models()
    return msg


def btn_clear_results():
    """Button: Clear All Results (Backcast, Forecast, Charts)"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    
    try:
        # Clear Backcast_Results sheet if it exists
        if 'Backcast_Results' in [s.name for s in wb.sheets]:
            backcast_sheet = wb.sheets['Backcast_Results']
            backcast_sheet.clear()
            backcast_sheet.range('A1').value = "Backcast results cleared - Run Backcast again to generate new results"
        
        # Clear Forecast_Results sheet if it exists
        if 'Forecast_Results' in [s.name for s in wb.sheets]:
            forecast_sheet = wb.sheets['Forecast_Results']
            forecast_sheet.clear()
            forecast_sheet.range('A1').value = "Forecast results cleared - Run Forecast again to generate new predictions"
        
        # Clear Model_Rankings sheet if it exists
        if 'Model_Rankings' in [s.name for s in wb.sheets]:
            rankings_sheet = wb.sheets['Model_Rankings']
            rankings_sheet.clear()
        
        # Clear all charts from Dashboard
        try:
            for pic in list(dash.pictures):
                if pic.name.startswith('Chart_'):
                    pic.delete()
        except:
            pass
        
        dash.range('B33').value = "✅ All results cleared! Ready to run new analysis."
        
        return "✅ Results cleared"
        
    except Exception as e:
        dash.range('B33').value = f"⚠️ Error clearing results: {str(e)[:50]}"
        return f"⚠️ Error: {str(e)[:50]}"


def main():
    """Main entry point"""
    setup_recipe_dashboard()


if __name__ == "__main__":
    xw.Book("SMFdashboard.xlsm").set_mock_caller()
    main()

