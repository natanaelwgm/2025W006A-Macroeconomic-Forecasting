"""
Merge SMF X and Y Variables by Frequency
Creates one consolidated dataset per frequency: Monthly, Quarterly, Weekly, Yearly
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# File paths
Y_FILE = "SMF_Datasets_Y Vars.xlsx"
X_FILE = "SMF_Datasets_X_Vars.xlsx"
OUTPUT_DIR = Path("merged")

# Create output directory
OUTPUT_DIR.mkdir(exist_ok=True)

# Frequency mappings
FREQUENCIES = {
    'Monthly': 'M',
    'Quarterly': 'Q',
    'Weekly': 'W',
    'Yearly': 'Y',
    'Daily': 'D'
}


def extract_variable_data(file_path, sheet_name):
    """
    Extract time series data from a sheet.
    Dates start at row 29 (0-indexed), column 0 is date, column 1 is value.
    """
    try:
        # Read from row 29 onwards (where actual data starts)
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, skiprows=29)
        
        if df.empty or len(df.columns) < 2:
            print(f"  ⚠️  {sheet_name}: No data found")
            return None
        
        # Extract date and value columns
        df_clean = pd.DataFrame({
            'date': df.iloc[:, 0],
            'value': df.iloc[:, 1]
        })
        
        # Remove rows with NaN in either column
        df_clean = df_clean.dropna()
        
        # Convert date to datetime
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Remove rows where date conversion failed
        df_clean = df_clean.dropna(subset=['date'])
        
        # Convert value to numeric
        df_clean['value'] = pd.to_numeric(df_clean['value'], errors='coerce')
        
        # Remove rows with NaN values
        df_clean = df_clean.dropna()
        
        if len(df_clean) == 0:
            print(f"  ⚠️  {sheet_name}: No valid data after cleaning")
            return None
        
        # Get clean variable name (remove frequency suffix)
        var_name = sheet_name
        for freq in FREQUENCIES.keys():
            if f" - {freq}" in var_name:
                var_name = var_name.replace(f" - {freq}", "").strip()
                break
        
        # Rename value column to variable name
        df_clean = df_clean.rename(columns={'value': var_name})
        
        print(f"  ✓ {sheet_name}: {len(df_clean)} observations ({df_clean['date'].min().date()} to {df_clean['date'].max().date()})")
        
        return df_clean
        
    except Exception as e:
        print(f"  ✗ Error reading {sheet_name}: {e}")
        return None


def merge_datasets_by_frequency(frequency):
    """
    Merge all Y and X variables for a given frequency.
    """
    print("\n" + "=" * 80)
    print(f"PROCESSING {frequency.upper()} DATA")
    print("=" * 80)
    
    # Load Excel files
    xl_y = pd.ExcelFile(Y_FILE)
    xl_x = pd.ExcelFile(X_FILE)
    
    # Find sheets matching this frequency
    y_sheets = [s for s in xl_y.sheet_names if f" - {frequency}" in s]
    x_sheets = [s for s in xl_x.sheet_names if f" - {frequency}" in s]
    
    print(f"\nFound {len(y_sheets)} Y variables and {len(x_sheets)} X variables")
    
    # Start with empty dataframe
    merged_df = None
    variables_added = []
    
    # Process Y variables
    print(f"\n📊 Processing Y Variables ({len(y_sheets)} sheets):")
    for sheet in y_sheets:
        df = extract_variable_data(Y_FILE, sheet)
        if df is not None:
            var_name = [col for col in df.columns if col != 'date'][0]
            if merged_df is None:
                merged_df = df
                variables_added.append(var_name)
            else:
                # Merge on date
                merged_df = pd.merge(merged_df, df, on='date', how='outer')
                variables_added.append(var_name)
    
    # Process X variables
    print(f"\n📊 Processing X Variables ({len(x_sheets)} sheets):")
    for sheet in x_sheets:
        df = extract_variable_data(X_FILE, sheet)
        if df is not None:
            var_name = [col for col in df.columns if col != 'date'][0]
            if merged_df is None:
                merged_df = df
                variables_added.append(var_name)
            else:
                # Merge on date
                merged_df = pd.merge(merged_df, df, on='date', how='outer')
                variables_added.append(var_name)
    
    if merged_df is None or len(merged_df) == 0:
        print(f"\n⚠️  No data to merge for {frequency}")
        return
    
    # Sort by date
    merged_df = merged_df.sort_values('date').reset_index(drop=True)
    
    # Summary
    print(f"\n{'=' * 80}")
    print(f"MERGED {frequency.upper()} DATASET SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total variables: {len(variables_added)}")
    print(f"Date range: {merged_df['date'].min().date()} to {merged_df['date'].max().date()}")
    print(f"Total observations: {len(merged_df)}")
    print(f"\nVariables included:")
    for i, var in enumerate(variables_added, 1):
        non_null = merged_df[var].notna().sum()
        print(f"  {i:2d}. {var:40s} ({non_null:4d} non-null values)")
    
    # Save to CSV
    output_file = OUTPUT_DIR / f"smf_{frequency.lower()}_data.csv"
    merged_df.to_csv(output_file, index=False)
    print(f"\n✅ Saved to: {output_file}")
    print(f"   Shape: {merged_df.shape}")
    
    # Save summary statistics
    stats_file = OUTPUT_DIR / f"smf_{frequency.lower()}_summary.txt"
    with open(stats_file, 'w') as f:
        f.write(f"SMF {frequency} Dataset Summary\n")
        f.write(f"{'=' * 80}\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Variables: {len(variables_added)}\n")
        f.write(f"Date Range: {merged_df['date'].min().date()} to {merged_df['date'].max().date()}\n")
        f.write(f"Total Observations: {len(merged_df)}\n\n")
        f.write("Variables:\n")
        for i, var in enumerate(variables_added, 1):
            non_null = merged_df[var].notna().sum()
            pct = (non_null / len(merged_df)) * 100
            f.write(f"  {i:2d}. {var:40s} {non_null:4d} obs ({pct:5.1f}%)\n")
        
        f.write(f"\n{'=' * 80}\n")
        f.write("Descriptive Statistics:\n")
        f.write(f"{'=' * 80}\n\n")
        f.write(merged_df.describe().to_string())
    
    print(f"✅ Saved summary to: {stats_file}")
    
    return merged_df


def main():
    """Main function to process all frequencies"""
    print("=" * 80)
    print("SMF DATASET MERGER")
    print("Merging X and Y Variables by Frequency")
    print("=" * 80)
    
    # Check if files exist
    if not Path(Y_FILE).exists():
        print(f"❌ Error: {Y_FILE} not found!")
        return
    
    if not Path(X_FILE).exists():
        print(f"❌ Error: {X_FILE} not found!")
        return
    
    print(f"✓ Found {Y_FILE}")
    print(f"✓ Found {X_FILE}")
    
    # Process each frequency
    results = {}
    for frequency in ['Monthly', 'Quarterly', 'Weekly', 'Yearly']:
        try:
            df = merge_datasets_by_frequency(frequency)
            if df is not None:
                results[frequency] = df
        except Exception as e:
            print(f"\n❌ Error processing {frequency}: {e}")
            import traceback
            traceback.print_exc()
    
    # Final summary
    print("\n" + "=" * 80)
    print("COMPLETE SUMMARY")
    print("=" * 80)
    print(f"\nProcessed {len(results)} frequency datasets:")
    for freq, df in results.items():
        print(f"  • {freq:12s}: {df.shape[1]-1:3d} variables × {df.shape[0]:5d} observations")
    
    print(f"\n✅ All datasets saved to: {OUTPUT_DIR}/")
    print("\nFiles created:")
    for f in sorted(OUTPUT_DIR.glob("*")):
        print(f"  • {f.name}")


if __name__ == "__main__":
    main()



