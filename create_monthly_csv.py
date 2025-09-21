#!/usr/bin/env python3
"""
Create monthly CSV from Excel files for the nowcasting system
Based on the log.json configuration
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

def create_monthly_csv():
    """Create the monthly CSV file from Excel sheets"""
    
    print("🔄 Creating monthly CSV from Excel files...")
    
    # File paths
    y_vars_file = "data/SMF_Datasets_Y Vars.xlsx"
    x_vars_file = "data/SMF_Datasets_X_Vars.xlsx"
    output_file = "data/processed/indonesia_macro_monthly.csv"
    
    # Check if files exist
    if not os.path.exists(y_vars_file):
        print(f"❌ Y variables file not found: {y_vars_file}")
        return False
        
    if not os.path.exists(x_vars_file):
        print(f"❌ X variables file not found: {x_vars_file}")
        return False
    
    # Read sheet names to understand structure
    print("📊 Analyzing Excel file structure...")
    
    try:
        y_sheets = pd.ExcelFile(y_vars_file).sheet_names
        x_sheets = pd.ExcelFile(x_vars_file).sheet_names
        
        print(f"Y Variables sheets: {y_sheets}")
        print(f"X Variables sheets: {x_sheets}")
        
    except Exception as e:
        print(f"❌ Error reading Excel files: {e}")
        return False
    
    # Target variables mapping based on log.json
    target_sheets = {
        'cpi_yoy': 'CPI - Monthly',
        'gdp_yoy': 'GDP - Monthly', 
        'usd_idr': 'FX - Monthly',
        'policy_rate_7drr': 'Policy Rate - Monthly',
        'deposit_rate_1m': 'Deposit Rate 1M - Monthly',
        'deposit_rate_3m': 'Deposit Rate 3M - Monthly', 
        'deposit_rate_6m': 'Deposit Rate 6M - Monthly',
        'deposit_rate_12m': 'Deposit Rate 12M - Monthly'
    }
    
    # Exogenous variables mapping
    exog_sheets = {
        'jibor_avg': 'JIBOR - Monthly',
        'ipi': 'IPI - Monthly', 
        'pmi': 'PMI - Monthly',
        'money_supply': 'Money Supply - Monthly',
        'jci': 'Stock Index - Monthly'
    }
    
    # Start with a date range
    date_range = pd.date_range(start='1969-01-31', end='2025-07-31', freq='M')
    df_combined = pd.DataFrame({'date': date_range})
    
    print("📈 Processing Y variables (targets)...")
    
    # Process Y variables
    for var_name, sheet_name in target_sheets.items():
        try:
            # Try to find the sheet (handle potential name variations)
            actual_sheet = None
            for sheet in y_sheets:
                if sheet_name.lower() in sheet.lower() or any(word in sheet.lower() for word in sheet_name.lower().split()):
                    actual_sheet = sheet
                    break
            
            if actual_sheet:
                print(f"  ✅ Processing {var_name} from '{actual_sheet}'")
                df_sheet = pd.read_excel(y_vars_file, sheet_name=actual_sheet)
                
                # Clean and process the data
                df_processed = process_sheet_data(df_sheet, var_name)
                if df_processed is not None and not df_processed.empty:
                    df_combined = pd.merge(df_combined, df_processed, on='date', how='left')
                else:
                    print(f"  ⚠️  No data extracted for {var_name}")
            else:
                print(f"  ❌ Sheet not found for {var_name}: {sheet_name}")
                
        except Exception as e:
            print(f"  ❌ Error processing {var_name}: {e}")
    
    print("📊 Processing X variables (exogenous)...")
    
    # Process X variables
    for var_name, sheet_name in exog_sheets.items():
        try:
            # Try to find the sheet
            actual_sheet = None
            for sheet in x_sheets:
                if sheet_name.lower() in sheet.lower() or any(word in sheet.lower() for word in sheet_name.lower().split()):
                    actual_sheet = sheet
                    break
            
            if actual_sheet:
                print(f"  ✅ Processing {var_name} from '{actual_sheet}'")
                df_sheet = pd.read_excel(x_vars_file, sheet_name=actual_sheet)
                
                # Clean and process the data
                df_processed = process_sheet_data(df_sheet, var_name)
                if df_processed is not None and not df_processed.empty:
                    df_combined = pd.merge(df_combined, df_processed, on='date', how='left')
                else:
                    print(f"  ⚠️  No data extracted for {var_name}")
            else:
                print(f"  ❌ Sheet not found for {var_name}: {sheet_name}")
                
        except Exception as e:
            print(f"  ❌ Error processing {var_name}: {e}")
    
    # Handle USD/IDR separately if it's in X variables
    if 'usd_idr' not in df_combined.columns:
        try:
            fx_sheet = None
            for sheet in x_sheets:
                if 'fx' in sheet.lower() or 'usd' in sheet.lower():
                    fx_sheet = sheet
                    break
            
            if fx_sheet:
                print(f"  ✅ Processing USD/IDR from '{fx_sheet}'")
                df_sheet = pd.read_excel(x_vars_file, sheet_name=fx_sheet)
                df_processed = process_sheet_data(df_sheet, 'usd_idr')
                if df_processed is not None and not df_processed.empty:
                    df_combined = pd.merge(df_combined, df_processed, on='date', how='left')
        except Exception as e:
            print(f"  ❌ Error processing USD/IDR: {e}")
    
    # Clean up the final dataset
    print("🧹 Cleaning final dataset...")
    
    # Remove rows where all values are NaN (except date)
    df_combined = df_combined.dropna(how='all', subset=[col for col in df_combined.columns if col != 'date'])
    
    # Format date column
    df_combined['date'] = pd.to_datetime(df_combined['date']).dt.strftime('%Y-%m-%d')
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save to CSV
    df_combined.to_csv(output_file, index=False)
    
    print(f"✅ Monthly CSV created successfully!")
    print(f"📁 File: {output_file}")
    print(f"📊 Shape: {df_combined.shape}")
    print(f"📅 Date range: {df_combined['date'].min()} to {df_combined['date'].max()}")
    print(f"📈 Variables: {list(df_combined.columns)}")
    
    return True

def process_sheet_data(df, var_name):
    """Process individual sheet data to extract time series"""
    
    if df.empty:
        return None
    
    # Try to identify date and value columns
    date_col = None
    value_col = None
    
    # Look for date column
    for col in df.columns:
        col_str = str(col).lower()
        if any(word in col_str for word in ['date', 'time', 'period', 'month', 'year']):
            # Check if this column contains date-like data
            sample_values = df[col].dropna().head()
            if not sample_values.empty:
                try:
                    pd.to_datetime(sample_values.iloc[0])
                    date_col = col
                    break
                except:
                    continue
    
    # If no obvious date column, try first column
    if date_col is None and len(df.columns) > 0:
        try:
            sample_values = df.iloc[:, 0].dropna().head()
            if not sample_values.empty:
                pd.to_datetime(sample_values.iloc[0])
                date_col = df.columns[0]
        except:
            pass
    
    # Look for value column
    for col in df.columns:
        if col != date_col:
            col_str = str(col).lower()
            # Skip columns that look like metadata
            if not any(word in col_str for word in ['note', 'source', 'desc', 'comment']):
                # Check if column has numeric data
                if pd.api.types.is_numeric_dtype(df[col]) or df[col].dtype == 'object':
                    try:
                        # Try to convert to numeric
                        test_series = pd.to_numeric(df[col], errors='coerce')
                        if not test_series.dropna().empty:
                            value_col = col
                            break
                    except:
                        continue
    
    # If we couldn't find proper columns, try a different approach
    if date_col is None or value_col is None:
        print(f"    ⚠️  Could not identify date/value columns for {var_name}")
        print(f"    📋 Available columns: {list(df.columns)}")
        
        # Fallback: assume first two columns are date and value
        if len(df.columns) >= 2:
            date_col = df.columns[0]
            value_col = df.columns[1]
            print(f"    🔄 Using fallback: date='{date_col}', value='{value_col}'")
        else:
            return None
    
    try:
        # Extract and clean the data
        df_clean = df[[date_col, value_col]].copy()
        df_clean.columns = ['date', var_name]
        
        # Convert date column
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Convert value column to numeric
        df_clean[var_name] = pd.to_numeric(df_clean[var_name], errors='coerce')
        
        # Remove rows with invalid dates or all NaN values
        df_clean = df_clean.dropna(subset=['date'])
        
        # Ensure monthly frequency (end of month)
        df_clean['date'] = df_clean['date'].dt.to_period('M').dt.end_time
        
        # Remove duplicates, keeping the last value for each month
        df_clean = df_clean.drop_duplicates(subset=['date'], keep='last')
        
        # Sort by date
        df_clean = df_clean.sort_values('date')
        
        print(f"    📊 Extracted {len(df_clean)} records for {var_name}")
        return df_clean
        
    except Exception as e:
        print(f"    ❌ Error processing data for {var_name}: {e}")
        return None

if __name__ == "__main__":
    success = create_monthly_csv()
    if success:
        print("\n🎉 CSV creation completed successfully!")
    else:
        print("\n❌ CSV creation failed!")
