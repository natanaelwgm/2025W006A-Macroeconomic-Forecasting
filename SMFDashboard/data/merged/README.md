# 📊 SMF Merged Datasets

**Successfully merged X and Y variables by frequency**

**Now available in both CSV and Excel formats!** ⭐

---

## 📁 **File Formats Available**

### CSV Files (for Python/R):
- All 5 frequency datasets in CSV format
- Easy to import with pandas/tidyverse
- Lightweight and universal

### Excel Files (for Excel/GUI): ⭐
- **`SMF_All_Frequencies.xlsx`** - Master file with all datasets (RECOMMENDED)
  - 6 sheets: Summary + 5 frequencies
  - Professional formatting
  - 865 KB total
- Individual `.xlsx` files for each frequency
- Blue headers, auto-sized columns
- Ready for analysis and presentation

**📖 See `EXCEL_FILES_GUIDE.md` for detailed Excel usage instructions**

---

## ✅ **Datasets Created**

### 1. **Monthly Dataset**
- **File:** `smf_monthly_data.csv`
- **Size:** 41 variables × 870 observations
- **Date Range:** 1953-04-01 to 2025-09-01
- **Summary:** `smf_monthly_summary.txt`

**Y Variables (9):**
- Govt Bond Yield 10 Yr
- Real GDP Growth
- BI7DRR
- Deposit Rate 1M, 3M, 6M, 12M
- CPI
- JISDOR Exchange Rate

**X Variables (32):**
- Cement, Stock Index, Fed Funds, FX, FPI, IPI
- JIBOR (x2), PMI, Money Supply (x2)
- Motor Sales, Retail, CCI
- Exports, Imports, Loans, Trade Bal
- Unemployment, Gov Bond
- Household Consumption, Fiscal Balance
- Terms of Trade, Crude Oil Price
- Disposable Income, GFCF
- Import/Export Price Index
- Imports Capital Goods, Household Debt
- Capacity Utilization, Tax Revenue

---

### 2. **Quarterly Dataset**
- **File:** `smf_quarterly_data.csv`
- **Size:** 36 variables × 289 observations
- **Date Range:** 1953-06-01 to 2025-06-01
- **Summary:** `smf_quarterly_summary.txt`

**Y Variables (7):**
- Real GDP Growth
- BI7DRR
- Deposit Rate 1M, 3M, 6M, 12M
- CPI

**X Variables (29):**
- Same categories as monthly, quarterly aggregation

---

### 3. **Weekly Dataset**
- **File:** `smf_weekly_data.csv`
- **Size:** 39 variables × 3,783 observations
- **Date Range:** 1953-04-06 to 2025-09-29
- **Summary:** `smf_weekly_summary.txt`

**Y Variables (7):**
- Govt Bond Yield 10 Yr
- Real GDP Growth
- BI7DRR
- Deposit Rate 3M, 6M, 12M
- JISDOR Exchange Rate

**X Variables (32):**
- High-frequency data, weekly observations

---

### 4. **Yearly Dataset**
- **File:** `smf_yearly_data.csv`
- **Size:** 28 variables × 112 observations
- **Date Range:** 1954-12-01 to 2025-02-01
- **Summary:** `smf_yearly_summary.txt`

**Y Variables (8):**
- All major Y variables aggregated annually

**X Variables (20):**
- Key economic indicators, yearly aggregation

---

## 📁 **File Structure**

```
merged/
├── smf_monthly_data.csv          ← Monthly time series
├── smf_monthly_summary.txt       ← Monthly statistics
├── smf_quarterly_data.csv        ← Quarterly time series
├── smf_quarterly_summary.txt     ← Quarterly statistics
├── smf_weekly_data.csv           ← Weekly time series
├── smf_weekly_summary.txt        ← Weekly statistics
├── smf_yearly_data.csv           ← Yearly time series
├── smf_yearly_summary.txt        ← Yearly statistics
└── README.md                     ← This file
```

---

## 🔍 **Data Format**

All CSV files have the same structure:
- **First column:** `date` (datetime format)
- **Remaining columns:** Variable values
- **Missing data:** Some variables have different coverage periods (NaN for missing)

**Example:**
```csv
date,CPI,GDP Growth,BI7DRR,FX,...
2020-01-01,105.3,5.2,4.5,14200,...
2020-02-01,106.1,5.1,4.5,14350,...
2020-03-01,106.8,4.8,4.25,14500,...
```

---

## 📈 **Usage Examples**

### Load Data in Python:
```python
import pandas as pd

# Load monthly data
df = pd.read_excel('smf_monthly_data.csv', parse_dates=['date'])

# Check shape
print(f"Shape: {df.shape}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")

# Check variables
print(f"Variables: {df.columns.tolist()}")

# Check data coverage
print(df.isnull().sum())
```

### Use in Excel Dashboard:
```python
# In your dashboard code
import pandas as pd

# Load the appropriate frequency
frequency = "monthly"  # or quarterly, weekly, yearly
df = pd.read_csv(f'data/merged/smf_{frequency}_data.csv', parse_dates=['date'])

# Write to Excel
data_view.range('A3').value = df
```

### Filter by Date Range:
```python
# Get data from 2020 onwards
df_recent = df[df['date'] >= '2020-01-01']

# Get specific variables
df_subset = df[['date', 'CPI', 'Real GDP Growth', 'BI7DRR']]
```

---

## ⚠️ **Important Notes**

### Missing Data
- Not all variables cover the same time period
- Some variables have more history than others
- Check summary files for exact coverage per variable

### Data Coverage by Variable (Monthly):
```
Variable                    Coverage    % Complete
──────────────────────────────────────────────────
Gov Bond                    868 obs     99.8%
CPI                         679 obs     78.0%
Money Supply                689 obs     79.2%
BI7DRR                      121 obs     13.9%  ← Recent variable
PMI                          36 obs      4.1%  ← Very recent
```

### Duplicate Variables
- Some variables appear twice (e.g., JIBOR, Money Supply)
- Check original source sheets if in doubt
- May represent different calculation methods

---

## 🎯 **Best Practices**

### 1. **Choose Right Frequency:**
- **Monthly:** Good balance, most variables available
- **Quarterly:** Good for GDP-related analysis
- **Weekly:** High frequency, good for financial variables
- **Yearly:** Long-term trends, fewer observations

### 2. **Handle Missing Data:**
```python
# Option 1: Drop columns with too many NaN
df_clean = df.dropna(axis=1, thresh=len(df)*0.5)  # Keep if 50%+ available

# Option 2: Forward fill
df_filled = df.fillna(method='ffill')

# Option 3: Interpolate
df_interp = df.interpolate(method='time')
```

### 3. **Align Date Ranges:**
```python
# Find common date range across all variables
common_start = df.dropna(axis=0, how='all').dropna(axis=1, how='all')['date'].min()
common_end = df['date'].max()

# Filter to common period
df_aligned = df[(df['date'] >= common_start) & (df['date'] <= common_end)]
```

---

## 📊 **Quick Statistics**

| Frequency | Variables | Observations | Date Range | File Size |
|-----------|-----------|--------------|------------|-----------|
| Monthly   | 41        | 870          | 1953-2025  | 185 KB    |
| Quarterly | 36        | 289          | 1953-2025  | 71 KB     |
| Weekly    | 39        | 3,783        | 1953-2025  | 750 KB    |
| Yearly    | 28        | 112          | 1954-2025  | 16 KB     |

---

## 🔧 **Regenerate Datasets**

If you need to regenerate or modify:

```bash
cd /Users/schalkeanindya/SMFdashboard/data
python3 merge_datasets.py
```

Script will:
1. Read all sheets from Y and X variable files
2. Extract data starting from row 30
3. Merge on date column
4. Create one CSV per frequency
5. Generate summary statistics

---

## 📞 **Data Dictionary**

### Y Variables (Target/Dependent)
- **Govt Bond Yield 10 Yr:** Government bond yield, 10 years
- **Real GDP Growth:** Real GDP growth rate (%)
- **BI7DRR:** Bank Indonesia 7-day reverse repo rate (%)
- **Deposit Rates:** Deposit rates for 1M, 3M, 6M, 12M maturities (%)
- **CPI:** Consumer Price Index
- **JISDOR:** Jakarta Interbank Spot Dollar Rate (IDR/USD)

### X Variables (Predictors/Independent)
- **Cement:** Cement production/sales
- **Stock Index:** Stock market index
- **Fed Funds:** US Federal Funds Rate (%)
- **FX:** Foreign exchange reserves (USD mn)
- **FPI:** Foreign Portfolio Investment
- **IPI:** Industrial Production Index
- **JIBOR:** Jakarta Interbank Offered Rate
- **PMI:** Purchasing Managers Index
- **Money Supply:** M1, M2 monetary aggregates
- **Motor Sales:** Automobile sales
- **Retail:** Retail sales index
- **CCI:** Consumer Confidence Index
- **Exports/Imports:** Trade values (USD mn)
- **Loans:** Bank lending
- **Trade Bal:** Trade balance
- **Unemployment:** Unemployment rate (%)
- **Gov Bond:** Government bond yields
- And more...

---

## ✅ **Ready to Use!**

Your consolidated datasets are ready for:
- ✅ Forecasting models
- ✅ Econometric analysis
- ✅ Dashboard integration
- ✅ Time series analysis
- ✅ Machine learning

**All data merged by date, cleaned, and ready to use! 🎉**

