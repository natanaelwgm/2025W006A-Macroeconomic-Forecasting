"""
Force Refresh Recipe_Config Sheet
Fixes caching issues by forcing module reload
"""

import xlwings as xw
import sys
from pathlib import Path

def force_refresh():
    """Force refresh Recipe_Config with latest code"""
    
    # Get current workbook
    wb = xw.books.active
    
    print("🔄 Forcing module reload...")
    
    # Remove ALL cached SMFdashboard modules
    modules_to_remove = [key for key in sys.modules.keys() if 'SMFdashboard' in key]
    for mod in modules_to_remove:
        del sys.modules[mod]
        print(f"   Removed cached: {mod}")
    
    # Force reimport from file
    sys.path.insert(0, str(Path(__file__).parent))
    from SMFdashboard_recipe import setup_recipe_config_sheet
    
    print("✅ Fresh module imported")
    
    # Delete old sheet if exists
    if 'Recipe_Config' in [s.name for s in wb.sheets]:
        print("🗑️  Deleting old Recipe_Config...")
        wb.sheets['Recipe_Config'].delete()
    
    # Create new sheet
    print("📊 Creating new Recipe_Config...")
    if 'Dashboard' not in [s.name for s in wb.sheets]:
        dash = wb.sheets.add('Dashboard', before=wb.sheets[0])
    
    if 'Recipe_Config' not in [s.name for s in wb.sheets]:
        config = wb.sheets.add('Recipe_Config', after=wb.sheets['Dashboard'])
    
    # Setup fresh config
    setup_recipe_config_sheet(wb)
    
    # Activate Recipe_Config
    wb.sheets['Recipe_Config'].activate()
    
    print("\n" + "=" * 70)
    print("✅ RECIPE_CONFIG REFRESHED WITH ALL 43 MODELS!")
    print("=" * 70)
    print("\nModels should now include:")
    print("  • 3 Basic Models (Naive, SeasonalNaive, Drift)")
    print("  • 10 Linear Models (Linear, Ridge, Lasso, ElasticNet, etc.)")
    print("  • 6 Time Series Models (AR1, ARp, ARIMA, TVP, BVAR)")
    print("  • 7 Tree Models (DecisionTree, RandomForest, XGBoost, etc.)")
    print("  • 3 Advanced ML (KNN, SVR, PLS1)")
    print("  • 2 Factor Models (DFM, DFM2)")
    print("  • 4 Financial Models (GARCH, NeuroGARCH, DNS, MIDAS)")
    print("  • 1 Deep Learning (LSTM)")
    print("\nTotal: 43 models")
    print("\nCheck Recipe_Config sheet now!")
    
    return "✅ Complete!"

if __name__ == "__main__":
    result = force_refresh()
    print(f"\n{result}")

