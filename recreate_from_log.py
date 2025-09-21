#!/usr/bin/env python3
"""
Recreate CSV from Log JSON Blueprint

This script uses the indonesia_macro_monthly.log.json as a blueprint to 
recreate the working CSV that your boss originally used successfully.
"""

import pandas as pd
import json
import os
from datetime import datetime

def load_log_blueprint():
    """Load the log JSON that shows the working data structure."""
    with open('data/processed/indonesia_macro_monthly.log.json', 'r') as f:
        return json.load(f)

def extract_sheet_data(excel_file, sheet_name, variable_name):
    """
    Extract data from a specific Excel sheet, handling the messy structure.
    Returns a DataFrame with 'date' and variable_name columns.
    """
    print(f"  📊 Extracting {variable_name} from '{sheet_name}'...")
    
    try:
        # Read the sheet
        df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        print(f"    📋 Sheet shape: {df.shape}")
        
        # Find the data start row (look for first date-like entry)
        data_start_row = -1
        for i in range(min(50, df.shape[0])):  # Check first 50 rows
            try:
                # Try to parse first column as date
                test_date = pd.to_datetime(df.iloc[i, 0], errors='coerce')
                if pd.notna(test_date):
                    data_start_row = i
                    print(f"    📅 Data starts at row {data_start_row}")
                    break
            except:
                continue
        
        if data_start_row == -1:
            print(f"    ❌ Could not find data start for {variable_name}")
            return None
        
        # Extract data starting from the identified row
        df_data = df.iloc[data_start_row:].copy()
        
        # Use first two columns (date and value)
        if df_data.shape[1] < 2:
            print(f"    ❌ Not enough columns for {variable_name}")
            return None
        
        df_data = df_data.iloc[:, :2].copy()  # Keep only first 2 columns
        df_data.columns = ['date', variable_name]
        
        # Clean and convert date column
        df_data['date'] = pd.to_datetime(df_data['date'], errors='coerce')
        df_data = df_data.dropna(subset=['date'])
        
        # Convert to end-of-month dates for consistency
        df_data['date'] = df_data['date'].dt.to_period('M').dt.end_time
        
        # Convert value column to numeric
        df_data[variable_name] = pd.to_numeric(df_data[variable_name], errors='coerce')
        
        # Remove rows with NaN values
        df_data = df_data.dropna(subset=[variable_name])
        
        print(f"    ✅ Extracted {len(df_data)} records")
        print(f"    📅 Date range: {df_data['date'].min()} to {df_data['date'].max()}")
        
        return df_data.set_index('date')
        
    except Exception as e:
        print(f"    ❌ Error extracting {variable_name}: {e}")
        return None

def recreate_csv_from_log():
    """
    Recreate the CSV using the log JSON as a blueprint.
    """
    print("🔄 Recreating CSV from log JSON blueprint...")
    
    # Load the blueprint
    log_data = load_log_blueprint()
    print(f"📋 Blueprint loaded: {log_data['first_date']} to {log_data['last_date']}")
    
    # Create date range based on log info
    start_date = pd.to_datetime(log_data['first_date']).to_period('M').end_time
    end_date = pd.to_datetime(log_data['last_date']).to_period('M').end_time
    date_index = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # Initialize with date index
    combined_df = pd.DataFrame(index=date_index)
    combined_df.index.name = 'date'
    
    print(f"📅 Created date range: {len(date_index)} months")
    
    # Extract target variable (CPI)
    print("📈 Processing TARGET variable...")
    target_info = log_data['target']
    y_file = 'data/SMF_Datasets_Y Vars.xlsx'  # Use actual file name
    
    cpi_data = extract_sheet_data(y_file, target_info['sheet'], 'cpi_yoy')
    if cpi_data is not None:
        combined_df = combined_df.join(cpi_data, how='left')
    
    # Extract exogenous variables
    print("📊 Processing EXOGENOUS variables...")
    for exog_info in log_data['exog']:
        var_name = exog_info['name']  # e.g., 'x_jibor'
        clean_name = var_name.replace('x_', '')  # Remove 'x_' prefix for column name
        
        # Map to our file names
        x_file = 'data/SMF_Datasets_X_Vars.xlsx'  # Use actual file name
        
        var_data = extract_sheet_data(x_file, exog_info['sheet'], clean_name)
        if var_data is not None:
            combined_df = combined_df.join(var_data, how='left')
    
    # Reset index to make date a column
    combined_df = combined_df.reset_index()
    
    # Reorder columns to match expected structure
    expected_cols = ['date', 'cpi_yoy', 'jibor', 'ipi', 'pmi', 'm2', 'jci', 'usd_idr']
    available_cols = ['date'] + [col for col in expected_cols[1:] if col in combined_df.columns]
    combined_df = combined_df[available_cols]
    
    # Rename columns to match current naming convention
    column_mapping = {
        'jibor': 'jibor_avg',
        'm2': 'money_supply',
        'usd_idr': 'usd_idr'
    }
    combined_df = combined_df.rename(columns=column_mapping)
    
    # Save the recreated CSV
    output_file = 'data/processed/indonesia_macro_monthly_fixed.csv'
    combined_df.to_csv(output_file, index=False)
    
    print(f"✅ Recreated CSV saved to: {output_file}")
    print(f"📊 Final shape: {combined_df.shape}")
    print(f"📈 Columns: {combined_df.columns.tolist()}")
    
    # Show data quality summary
    print("\n📋 Data Quality Summary:")
    for col in combined_df.columns:
        if col != 'date':
            non_null = combined_df[col].notna().sum()
            total = len(combined_df)
            pct = (non_null/total)*100
            print(f"  {col}: {non_null}/{total} ({pct:.1f}%)")
    
    print("\n📋 Sample data (first 5 rows):")
    print(combined_df.head())
    
    print("\n📋 Sample data (last 5 rows):")
    print(combined_df.tail())
    
    return output_file

if __name__ == "__main__":
    try:
        output_file = recreate_csv_from_log()
        print(f"\n🎉 Success! Working CSV recreated at: {output_file}")
        print("\n📝 Next steps:")
        print("1. Review the data quality summary above")
        print("2. If USD/IDR data looks good, replace the broken CSV:")
        print(f"   cp {output_file} data/processed/indonesia_macro_monthly.csv")
        print("3. Re-run your model tests")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please check the Excel files and log JSON structure.")
