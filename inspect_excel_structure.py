#!/usr/bin/env python3
"""Inspect Excel file structure to understand column names"""

import pandas as pd
import sys

def inspect_excel(filename):
    """Read and display Excel file structure"""
    try:
        print(f"Reading: {filename}")
        df = pd.read_excel(filename)
        
        print(f"\n📊 Shape: {df.shape}")
        print(f"\n📋 Columns: {df.columns.tolist()}")
        print(f"\n📝 First 5 rows:")
        print(df.head().to_string())
        print(f"\n📊 Data types:")
        print(df.dtypes)
        
        # Check for Variable column
        if 'Variable' in df.columns or 'variable' in df.columns:
            var_col = 'Variable' if 'Variable' in df.columns else 'variable'
            unique_vars = df[var_col].unique()
            print(f"\n🔍 Unique variables: {unique_vars}")
        
        # Check for Model column
        model_cols = [col for col in df.columns if 'model' in col.lower()]
        print(f"\n🎯 Model-related columns: {model_cols}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    files = [
        '/Users/schalkeanindya/SMFdashboard/FINAL_EXCEL_REPORTS/forecasting_results_Monthly_detailed.xlsx',
        '/Users/schalkeanindya/SMFdashboard/FINAL_EXCEL_REPORTS/forecasting_results_Quarterly_detailed.xlsx',
    ]
    
    for f in files:
        inspect_excel(f)
        print("\n" + "="*80 + "\n")

