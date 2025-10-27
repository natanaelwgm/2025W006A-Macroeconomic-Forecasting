"""
Merge SMF X and Y Variables by Frequency (V2)
- Includes Informal Employment data
- Creates Semesterly dataset by aggregating Quarterly
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

# Frequency mappings with truncated/misspelled variations
FREQUENCY_PATTERNS = {
    'Monthly': ['Monthly', 'Monthly1', 'Monthl', 'Month', '1 Month'],
    'Quarterly': ['Quarterly', 'Quarterly1', 'Quarterl', 'Quarter', 'Quarte', 'Quart'],
    'Weekly': ['Weekly', 'Weekly1', 'Weekly ', 'Weekl'],  # Note: 'Weekly ' has trailing space
    'Yearly': ['Yearly', 'Yearly1', 'Annual', 'Annua'],
    'Daily': ['Daily', 'Daily1']
}

# Reverse mapping for quick lookup
FREQUENCY_NORMALIZE = {}
for standard, variations in FREQUENCY_PATTERNS.items():
    for variation in variations:
        FREQUENCY_NORMALIZE[variation] = standard

FREQUENCIES = {
    'Monthly': 'M',
    'Quarterly': 'Q',
    'Weekly': 'W',
    'Yearly': 'Y',
    'Daily': 'D'
}

# Variable aggregation methods (for creating Semesterly from Quarterly)
# True = Average, False = Sum
AGGREGATION_METHOD = {
    # Interest rates, percentages -> Average
    'BI7DRR': True,
    'Deposit Rate': True,
    'CPI': True,
    'Unemployment': True,
    'Gov Bond': True,
    'Govt Bond': True,
    'Fed Funds': True,
    'JIBOR': True,
    'PMI': True,
    'Stock Index': True,
    'FX': True,  # Average of reserves
    'JISDOR': True,
    'Crude Oil Price': True,
    'Price Index': True,
    'Terms of Trade': True,
    
    # Flows, volumes -> Sum
    'GDP': False,
    'Cement': False,
    'FPI': False,
    'IPI': False,
    'Money Supply': False,
    'Motor Sales': False,
    'Retail': False,
    'CCI': False,
    'Exports': False,
    'Imports': False,
    'Loans': False,
    'Trade Bal': False,
    'Consumption': False,
    'Fiscal Balance': False,
    'Disposable Income': False,
    'GFCF': False,
    'Capital Goods': False,
    'Debt': False,
    'Capacity Utilization': True,
    'Tax Revenue': False,
    'Expenditure': False,
    'Informal Employment': False,  # Count -> Sum
}


def should_average(var_name):
    """Determine if variable should be averaged (True) or summed (False)"""
    for key, is_avg in AGGREGATION_METHOD.items():
        if key in var_name:
            return is_avg
    # Default: average for rates/indices, sum for flows
    return True  # Conservative default


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
        # Try all frequency variations
        for freq_list in FREQUENCY_PATTERNS.values():
            for freq in freq_list:
                if sheet_name.endswith(f" - {freq}"):
                    var_name = sheet_name.rsplit(f" - {freq}", 1)[0].strip()
                    break
            if var_name != sheet_name:  # Found a match
                break
        
        # Rename value column to variable name
        df_clean = df_clean.rename(columns={'value': var_name})
        
        print(f"  ✓ {sheet_name}: {len(df_clean)} observations ({df_clean['date'].min().date()} to {df_clean['date'].max().date()})")
        
        return df_clean
        
    except Exception as e:
        print(f"  ✗ Error reading {sheet_name}: {e}")
        return None


def extract_informal_employment(file_path, frequency):
    """
    Extract Informal Employment data with special filtering.
    Filter: sex.label = "Total" AND classif1.label = "Age (Aggregate bands): Total"
    Date column: "time" (column 5)
    Value column: "obs_value" (column 6)
    """
    try:
        sheet_name = f"Informal Employment - {frequency}"
        
        # Read with header row
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
        
        if df.empty:
            print(f"  ⚠️  {sheet_name}: No data found")
            return None
        
        # Filter for Total sex and Age (Aggregate bands): Total
        mask = (df['sex.label'] == 'Total') & (df['classif1.label'] == 'Age (Aggregate bands): Total')
        df_filtered = df[mask].copy()
        
        if len(df_filtered) == 0:
            print(f"  ⚠️  {sheet_name}: No data matching filters")
            return None
        
        # Extract time and obs_value columns
        df_clean = pd.DataFrame({
            'date': df_filtered['time'],
            'Informal Employment': df_filtered['obs_value']
        })
        
        # Remove rows with NaN
        df_clean = df_clean.dropna()
        
        # Convert time to datetime (it might be just year)
        if frequency == 'Annual':
            # For annual data, time is just year (2023)
            df_clean['date'] = pd.to_datetime(df_clean['date'].astype(str) + '-12-01')
        elif frequency == 'Quarterly':
            # For quarterly, need to parse properly
            df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Remove any rows where date conversion failed
        df_clean = df_clean.dropna(subset=['date'])
        
        # Convert value to numeric
        df_clean['Informal Employment'] = pd.to_numeric(df_clean['Informal Employment'], errors='coerce')
        df_clean = df_clean.dropna()
        
        if len(df_clean) == 0:
            print(f"  ⚠️  {sheet_name}: No valid data after cleaning")
            return None
        
        print(f"  ✓ {sheet_name}: {len(df_clean)} observations ({df_clean['date'].min().date()} to {df_clean['date'].max().date()})")
        
        return df_clean
        
    except Exception as e:
        print(f"  ✗ Error reading Informal Employment ({frequency}): {e}")
        import traceback
        traceback.print_exc()
        return None


def merge_datasets_by_frequency(frequency, include_informal=True):
    """
    Merge all Y and X variables for a given frequency.
    Handles truncated/misspelled frequency names.
    """
    print("\n" + "=" * 80)
    print(f"PROCESSING {frequency.upper()} DATA")
    print("=" * 80)
    
    # Load Excel files
    xl_y = pd.ExcelFile(Y_FILE)
    xl_x = pd.ExcelFile(X_FILE)
    
    # Get all variations of this frequency name
    freq_variations = FREQUENCY_PATTERNS.get(frequency, [frequency])
    
    # Find sheets matching any variation of this frequency
    y_sheets = []
    x_sheets = []
    
    for sheet in xl_y.sheet_names:
        if "Informal Employment" in sheet:
            continue
        # Check if sheet ends with any frequency variation
        for freq_var in freq_variations:
            if sheet.endswith(f" - {freq_var}"):
                y_sheets.append(sheet)
                break
    
    for sheet in xl_x.sheet_names:
        for freq_var in freq_variations:
            if sheet.endswith(f" - {freq_var}"):
                x_sheets.append(sheet)
                break
    
    print(f"\nFound {len(y_sheets)} Y variables and {len(x_sheets)} X variables")
    print(f"(Searching for: {', '.join(freq_variations)})")
    
    # Show truncated sheets if any
    truncated_y = [s for s in y_sheets if not s.endswith(f" - {frequency}")]
    truncated_x = [s for s in x_sheets if not s.endswith(f" - {frequency}")]
    
    if truncated_y or truncated_x:
        print(f"\n🔧 Found {len(truncated_y) + len(truncated_x)} sheets with truncated/variant names:")
        for sheet in truncated_y + truncated_x:
            freq_suffix = sheet.rsplit(' - ', 1)[-1]
            print(f"  • {sheet} ('{freq_suffix}' → {frequency})")
    
    # Start with empty dataframe
    merged_df = None
    variables_added = []
    
    # Process Y variables
    print(f"\n📊 Processing Y Variables ({len(y_sheets)} sheets):")
    for sheet in y_sheets:
        df = extract_variable_data(Y_FILE, sheet)
        if df is not None:
            var_name = [col for col in df.columns if col != 'date'][0]
            
            # Handle duplicate variable names
            original_var = var_name
            suffix = 1
            while var_name in variables_added:
                var_name = f"{original_var}_{suffix}"
                suffix += 1
            
            if var_name != original_var:
                df = df.rename(columns={original_var: var_name})
                print(f"    → Renamed duplicate '{original_var}' to '{var_name}'")
            
            if merged_df is None:
                merged_df = df
                variables_added.append(var_name)
            else:
                merged_df = pd.merge(merged_df, df, on='date', how='outer')
                variables_added.append(var_name)
    
    # Add Informal Employment if available and requested
    if include_informal:
        print(f"\n📊 Processing Informal Employment:")
        informal_freq = 'Annual' if frequency == 'Yearly' else frequency
        df_informal = extract_informal_employment(Y_FILE, informal_freq)
        if df_informal is not None:
            if merged_df is None:
                merged_df = df_informal
                variables_added.append('Informal Employment')
            else:
                merged_df = pd.merge(merged_df, df_informal, on='date', how='outer')
                variables_added.append('Informal Employment')
    
    # Process X variables
    print(f"\n📊 Processing X Variables ({len(x_sheets)} sheets):")
    for sheet in x_sheets:
        df = extract_variable_data(X_FILE, sheet)
        if df is not None:
            var_name = [col for col in df.columns if col != 'date'][0]
            
            # Handle duplicate variable names
            original_var = var_name
            suffix = 1
            while var_name in variables_added:
                var_name = f"{original_var}_{suffix}"
                suffix += 1
            
            if var_name != original_var:
                df = df.rename(columns={original_var: var_name})
                print(f"    → Renamed duplicate '{original_var}' to '{var_name}'")
            
            if merged_df is None:
                merged_df = df
                variables_added.append(var_name)
            else:
                merged_df = pd.merge(merged_df, df, on='date', how='outer')
                variables_added.append(var_name)
    
    if merged_df is None or len(merged_df) == 0:
        print(f"\n⚠️  No data to merge for {frequency}")
        return None
    
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


def create_semesterly_from_quarterly(quarterly_df):
    """
    Create Semesterly (half-yearly) dataset by aggregating Quarterly data.
    Uses average for rates/indices, sum for flows.
    """
    print("\n" + "=" * 80)
    print("CREATING SEMESTERLY DATA FROM QUARTERLY")
    print("=" * 80)
    
    if quarterly_df is None or len(quarterly_df) == 0:
        print("⚠️  No quarterly data available")
        return None
    
    # Create semester period (1=H1, 2=H2)
    df = quarterly_df.copy()
    df['year'] = df['date'].dt.year
    df['quarter'] = df['date'].dt.quarter
    df['semester'] = df['quarter'].apply(lambda q: 1 if q <= 2 else 2)
    
    # For each variable, determine aggregation method
    agg_dict = {}
    variables = [col for col in df.columns if col not in ['date', 'year', 'quarter', 'semester']]
    
    print("\nAggregation methods:")
    for var in variables:
        if should_average(var):
            agg_dict[var] = 'mean'
            method = "AVG"
        else:
            agg_dict[var] = 'sum'
            method = "SUM"
        print(f"  • {var:40s} → {method}")
    
    # Group by year and semester
    semesterly = df.groupby(['year', 'semester']).agg(agg_dict).reset_index()
    
    # Create date column (use end of semester)
    semesterly['date'] = pd.to_datetime(
        semesterly.apply(
            lambda row: f"{int(row['year'])}-{6 if row['semester'] == 1 else 12}-30",
            axis=1
        )
    )
    
    # Drop temporary columns
    semesterly = semesterly.drop(columns=['year', 'semester'])
    
    # Reorder columns (date first)
    cols = ['date'] + [col for col in semesterly.columns if col != 'date']
    semesterly = semesterly[cols]
    
    # Sort by date
    semesterly = semesterly.sort_values('date').reset_index(drop=True)
    
    print(f"\n{'=' * 80}")
    print("SEMESTERLY DATASET SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total variables: {len(variables)}")
    print(f"Date range: {semesterly['date'].min().date()} to {semesterly['date'].max().date()}")
    print(f"Total observations: {len(semesterly)}")
    
    # Save
    output_file = OUTPUT_DIR / "smf_semesterly_data.csv"
    semesterly.to_csv(output_file, index=False)
    print(f"\n✅ Saved to: {output_file}")
    print(f"   Shape: {semesterly.shape}")
    
    # Save summary
    stats_file = OUTPUT_DIR / "smf_semesterly_summary.txt"
    with open(stats_file, 'w') as f:
        f.write("SMF Semesterly Dataset Summary\n")
        f.write(f"{'=' * 80}\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("Created by aggregating Quarterly data\n\n")
        f.write(f"Total Variables: {len(variables)}\n")
        f.write(f"Date Range: {semesterly['date'].min().date()} to {semesterly['date'].max().date()}\n")
        f.write(f"Total Observations: {len(semesterly)}\n\n")
        f.write("Aggregation Methods:\n")
        for var in variables:
            method = "AVERAGE" if agg_dict[var] == 'mean' else "SUM"
            non_null = semesterly[var].notna().sum()
            pct = (non_null / len(semesterly)) * 100
            f.write(f"  {var:40s} {method:7s} {non_null:3d} obs ({pct:5.1f}%)\n")
        
        f.write(f"\n{'=' * 80}\n")
        f.write("Descriptive Statistics:\n")
        f.write(f"{'=' * 80}\n\n")
        f.write(semesterly.describe().to_string())
    
    print(f"✅ Saved summary to: {stats_file}")
    
    return semesterly


def main():
    """Main function to process all frequencies"""
    print("=" * 80)
    print("SMF DATASET MERGER V2")
    print("Including Informal Employment + Semesterly Aggregation")
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
    quarterly_df = None
    
    for frequency in ['Monthly', 'Quarterly', 'Weekly', 'Yearly', 'Daily']:
        try:
            # Informal employment only available for Monthly, Quarterly, Yearly
            include_informal = frequency in ['Quarterly', 'Yearly']
            df = merge_datasets_by_frequency(frequency, include_informal=include_informal)
            if df is not None:
                results[frequency] = df
                if frequency == 'Quarterly':
                    quarterly_df = df
        except Exception as e:
            print(f"\n❌ Error processing {frequency}: {e}")
            import traceback
            traceback.print_exc()
    
    # Create Semesterly from Quarterly
    if quarterly_df is not None:
        try:
            semesterly_df = create_semesterly_from_quarterly(quarterly_df)
            if semesterly_df is not None:
                results['Semesterly'] = semesterly_df
        except Exception as e:
            print(f"\n❌ Error creating Semesterly: {e}")
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
    for f in sorted(OUTPUT_DIR.glob("smf_*")):
        print(f"  • {f.name}")


if __name__ == "__main__":
    main()

