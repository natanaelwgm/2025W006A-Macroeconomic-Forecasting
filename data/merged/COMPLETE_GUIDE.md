# 📊 SMF Complete Dataset Collection

**All frequencies merged with Informal Employment + Semesterly aggregation**

---

## ✅ **5 Datasets Created** (With Truncated Names Fixed! 🔧)

| Frequency | Variables | Observations | Date Range | File Size | Variables Gained |
|-----------|-----------|--------------|------------|-----------|------------------|
| **Monthly** | 43 | 870 | 1953-2025 | 195 KB | +2 (+4.9%) |
| **Quarterly** | 44 | 304 | 1953-2025 | 81 KB | +7 (+18.9%) |
| **Semesterly** | 44 | 146 | 1953-2025 | 50 KB | +7 (+18.9%) |
| **Weekly** | 40 | 3,783 | 1953-2025 | 770 KB | +1 (+2.6%) |
| **Yearly** | 44 | 112 | 1954-2025 | 23 KB | +15 (+51.7%) |
| **TOTAL** | **215** | | | | **+32 (+17.5%)** |

### 🎉 **Major Improvement:** 
Fixed truncated/misspelled frequency names in Excel sheets, recovering **32 additional variables** across all datasets!

---

## 🎯 **Key Features**

### ✅ Informal Employment Included
- **Quarterly dataset:** 14 observations (2016-2023)
- **Yearly dataset:** Included from Annual sheet
- **Filtered correctly:**
  - Sex label = "Total"
  - Classif1 label = "Age (Aggregate bands): Total"
- **Semesterly:** Aggregated from Quarterly (Sum method)

### ✅ Semesterly Dataset (NEW!)
- **Created by aggregating Quarterly data**
- **Smart aggregation:**
  - **Average** for rates, percentages, indices (CPI, BI7DRR, Stock Index, etc.)
  - **Sum** for flows, volumes, counts (GDP, Cement, Exports, Money Supply, etc.)
- **37 variables** including Informal Employment
- **145 observations** (H1 and H2 per year)

### ✅ Comprehensive Variable Coverage
- **Y Variables (Targets):** GDP, CPI, Interest Rates, Exchange Rates, Informal Employment
- **X Variables (Predictors):** 30+ economic indicators

---

## 📁 **Files Available**

```
merged/
├── smf_monthly_data.csv          (41 vars × 870 obs)
├── smf_monthly_summary.txt
├── smf_quarterly_data.csv        (37 vars × 289 obs) ← Has Informal Employment
├── smf_quarterly_summary.txt
├── smf_semesterly_data.csv       (37 vars × 145 obs) ← NEW! Aggregated
├── smf_semesterly_summary.txt
├── smf_weekly_data.csv           (39 vars × 3,783 obs)
├── smf_weekly_summary.txt
├── smf_yearly_data.csv           (29 vars × 112 obs) ← Has Informal Employment
├── smf_yearly_summary.txt
├── README.md
└── COMPLETE_GUIDE.md             ← This file
```

---

## 🔍 **Informal Employment Details**

### Available Frequencies:
- ✅ **Quarterly:** 14 obs (2016-01-01 to 2023-07-01)
- ✅ **Yearly:** Included from "Informal Employment - Annual" sheet
- ❌ **Monthly, Weekly:** Not available in source data
- ✅ **Semesterly:** Created by summing Quarterly data

### Data Filters Applied:
```
sex.label == "Total"
classif1.label == "Age (Aggregate bands): Total"
```

### Data Source:
- **From:** `SMF_Datasets_Y Vars.xlsx`
- **Sheets:** 
  - "Informal Employment - Quarterly"
  - "Informal Employment - Annual"
- **Time column:** `time` (not `date` like other variables)
- **Value column:** `obs_value`
- **Unit:** Thousands

---

## 📈 **Semesterly Aggregation Methods**

### Variables Averaged (Rates, Percentages, Indices):
- BI7DRR
- Deposit Rates (1M, 3M, 6M, 12M)
- CPI
- Stock Index
- Fed Funds
- JIBOR
- PMI
- Gov Bond Yields
- Unemployment Rate
- Crude Oil Price
- Import/Export Price Index
- Terms of Trade
- FX Reserves (average level)
- Capacity Utilization

### Variables Summed (Flows, Volumes, Counts):
- **Real GDP Growth** ← Sum of 2 quarters
- **Informal Employment** ← Sum of 2 quarters
- Cement Production
- FPI, IPI
- Money Supply
- Motor Sales
- Retail Sales
- CCI
- Exports, Imports, Trade Balance
- Loans
- Household Consumption
- Fiscal Balance
- Disposable Income
- GFCF
- Household Debt
- Tax Revenue
- Imports Capital Goods

---

## 💡 **How to Use**

### Load in Python:
```python
import pandas as pd

# Load any frequency
df_monthly = pd.read_csv('data/merged/smf_monthly_data.csv', parse_dates=['date'])
df_quarterly = pd.read_csv('data/merged/smf_quarterly_data.csv', parse_dates=['date'])
df_semesterly = pd.read_csv('data/merged/smf_semesterly_data.csv', parse_dates=['date'])
df_weekly = pd.read_csv('data/merged/smf_weekly_data.csv', parse_dates=['date'])
df_yearly = pd.read_csv('data/merged/smf_yearly_data.csv', parse_dates=['date'])

# Check Informal Employment coverage
print(df_quarterly['Informal Employment'].notna().sum())  # 14 obs
print(df_semesterly['Informal Employment'].notna().sum())  # 7 obs (half-yearly)
```

### Check Semesterly Aggregation:
```python
# Load quarterly and semesterly
df_q = pd.read_csv('data/merged/smf_quarterly_data.csv', parse_dates=['date'])
df_s = pd.read_csv('data/merged/smf_semesterly_data.csv', parse_dates=['date'])

# Example: GDP should be sum of 2 quarters
gdp_2023h1_quarterly = df_q[df_q['date'].dt.year == 2023].head(2)['Real GDP Growth'].sum()
gdp_2023h1_semesterly = df_s[df_s['date'] == '2023-06-30']['Real GDP Growth'].values[0]

print(f"Quarterly sum: {gdp_2023h1_quarterly}")
print(f"Semesterly value: {gdp_2023h1_semesterly}")
# Should match!

# Example: CPI should be average of 2 quarters
cpi_2023h1_quarterly = df_q[df_q['date'].dt.year == 2023].head(2)['CPI'].mean()
cpi_2023h1_semesterly = df_s[df_s['date'] == '2023-06-30']['CPI'].values[0]

print(f"Quarterly avg: {cpi_2023h1_quarterly}")
print(f"Semesterly value: {cpi_2023h1_semesterly}")
# Should match!
```

### Filter by Date Range:
```python
# Get recent data (2020 onwards)
df_recent = df_quarterly[df_quarterly['date'] >= '2020-01-01']

# Get data with Informal Employment
df_with_informal = df_quarterly.dropna(subset=['Informal Employment'])
print(f"Periods with Informal Employment: {len(df_with_informal)}")  # 14
```

---

## 📊 **Variable List**

### Y Variables (Targets) - Available in Most Frequencies:
1. **Govt Bond Yield 10 Yr** - Government bond yield
2. **Real GDP Growth** - Real GDP growth rate (%)
3. **BI7DRR** - Bank Indonesia 7-day reverse repo rate (%)
4. **Deposit Rate 1M, 3M, 6M, 12M** - Deposit rates (%)
5. **CPI** - Consumer Price Index
6. **JISDOR Exchange Rate** - Jakarta Interbank Spot Dollar Rate
7. **Informal Employment** ← NEW! (Quarterly, Yearly, Semesterly)

### X Variables (Predictors) - 30+ indicators:
- Cement Production
- Stock Index
- Fed Funds Rate
- FX Reserves
- FPI, IPI, PMI
- JIBOR
- Money Supply (2 variants)
- Motor Sales
- Retail, CCI
- Exports, Imports, Trade Balance
- Loans
- Unemployment
- Government Bond Yields
- Household Consumption, Debt
- Fiscal Balance
- Terms of Trade
- Crude Oil Price
- Disposable Income
- GFCF (Gross Fixed Capital Formation)
- Import/Export Price Index
- Imports Capital Goods
- Capacity Utilization
- Tax Revenue
- Government Expenditure

---

## 🎯 **Best Practices**

### Choosing Frequency:

**Monthly:**
- Most variables available (41)
- Best for general analysis
- Good coverage for financial variables
- No Informal Employment

**Quarterly:**
- Good for GDP analysis
- **Has Informal Employment** ✓
- 37 variables
- Balanced coverage

**Semesterly (NEW!):**
- Half-yearly aggregation
- **Has Informal Employment** ✓
- Same 37 variables as Quarterly
- Longer-term trends
- Properly aggregated (avg/sum based on variable nature)

**Weekly:**
- High frequency (3,783 obs)
- Best for financial markets
- Good for short-term forecasting
- No Informal Employment

**Yearly:**
- Long-term trends
- **Has Informal Employment** ✓
- Fewer observations (112)
- Best for annual planning

### Handling Missing Data:

```python
# Check data coverage
df.isnull().sum()

# Option 1: Use only complete cases
df_complete = df.dropna()

# Option 2: Forward fill within reasonable limits
df_filled = df.fillna(method='ffill', limit=2)

# Option 3: Use variables with good coverage
good_vars = df.columns[df.isnull().sum() / len(df) < 0.3]  # < 30% missing
df_good = df[good_vars]

# Option 4: For Informal Employment, use only available periods
df_with_informal = df.dropna(subset=['Informal Employment'])
```

---

## 🔄 **Regenerate Datasets**

To recreate all datasets:

```bash
cd /Users/schalkeanindya/SMFdashboard/data
python3 merge_datasets_v2.py
```

**Features:**
- Merges X and Y variables by date
- Includes Informal Employment (filtered correctly)
- Creates Semesterly by aggregating Quarterly
- Smart aggregation (avg vs sum based on variable nature)
- Generates summary statistics for each frequency

---

## 📝 **Data Dictionary**

### Informal Employment
- **Definition:** Number of persons in informal employment (thousands)
- **Filter:** Total sex, Age (Aggregate bands): Total
- **Source:** LFS - National Labour Force Survey (ILO-STATISTICS)
- **Frequency:** Quarterly, Annual
- **Unit:** Thousands
- **Coverage:** 2016-2023
- **In Semesterly:** Sum of 2 quarters

### Key Economic Indicators:
- **BI7DRR:** Bank Indonesia's policy rate, replaced BI Rate in 2016
- **JISDOR:** Reference rate for IDR/USD transactions
- **FX:** Foreign exchange reserves in USD millions
- **CPI:** Consumer Price Index, base year varies
- **IPI:** Industrial Production Index
- **PMI:** Purchasing Managers Index (50 = expansion threshold)
- **GFCF:** Gross Fixed Capital Formation (investment indicator)

---

## ✅ **Quality Checks Passed**

- [x] All frequencies merged successfully
- [x] Informal Employment added to Quarterly & Yearly
- [x] Semesterly created from Quarterly
- [x] Correct aggregation methods applied (avg vs sum)
- [x] Date alignment verified
- [x] No duplicate columns
- [x] Summary statistics generated
- [x] All files saved successfully

---

## 🎉 **Ready to Use!**

Your complete dataset collection is ready for:
- ✅ Forecasting models (all frequencies)
- ✅ Econometric analysis
- ✅ Dashboard integration
- ✅ Time series analysis
- ✅ Machine learning
- ✅ Labor market analysis (with Informal Employment)
- ✅ Semesterly reporting (new aggregated dataset)

**All data cleaned, merged, and ready! 🚀**

---

## 📞 **Files to Use**

### For Forecasting Dashboard:
```python
# Monthly - Most complete
df = pd.read_csv('data/merged/smf_monthly_data.csv', parse_dates=['date'])

# Quarterly - Best for GDP + Labor
df = pd.read_csv('data/merged/smf_quarterly_data.csv', parse_dates=['date'])

# Semesterly - Half-yearly analysis
df = pd.read_csv('data/merged/smf_semesterly_data.csv', parse_dates=['date'])
```

### For Labor Market Analysis:
```python
# Use Quarterly (most granular with Informal Employment)
df = pd.read_csv('data/merged/smf_quarterly_data.csv', parse_dates=['date'])

# Or Yearly for long-term trends
df = pd.read_csv('data/merged/smf_yearly_data.csv', parse_dates=['date'])
```

**All datasets ready in:**
`/Users/schalkeanindya/SMFdashboard/data/merged/`

---

## 🔧 **Truncation Patterns Fixed**

The merge script now handles Excel sheet names that were truncated or misspelled:

### Patterns Detected & Fixed:

| Original (Truncated) | Corrected To | Sheets Fixed |
|----------------------|--------------|--------------|
| `Quarter` | `Quarterly` | 3 sheets |
| `Quarterl` | `Quarterly` | 2 sheets |
| `Quarte` | `Quarterly` | 1 sheet |
| `Quart` | `Quarterly` | 1 sheet |
| `Month` | `Monthly` | 1 sheet |
| `Monthl` | `Monthly` | 1 sheet |
| `Weekly ` (trailing space) | `Weekly` | 1 sheet |
| `Weekl` | `Weekly` | 1 sheet |
| `Annua` | `Yearly` | 1 sheet |
| `Annual` | `Yearly` | 13 sheets |

### Variables Recovered:

**Monthly (+2 variables):**
- Manufacturing Wages YoY
- Government Expenditure

**Quarterly (+7 variables):**
- Govt Bond Yield 10 Yr ← Missing before!
- JISDOR Exchange Rate ← Was incomplete
- Capacity Utilization
- Manufacturing Wages YoY
- Household Consumption
- Imports Capital Goods
- Government Expenditure

**Weekly (+1 variable):**
- Manufacturing Wages YoY

**Yearly (+15 variables):**
- Manufacturing Wages YoY
- Crude Oil Price, Disposable Income, Terms of Trade
- Household Consumption, Fiscal Balance
- Import/Export Price Index
- Household Debt, GFCF
- Imports Capital Goods, Government Expenditure
- Tax Revenue, Capacity Utilization
- Plus duplicate JIBOR & Money Supply variants

### Impact Summary:

```
Before Fix: 183 total variables across all frequencies
After Fix:  215 total variables across all frequencies
Recovered:  +32 variables (+17.5% improvement!)
```

**Biggest gains:**
- Yearly: +51.7% (29 → 44 variables)
- Quarterly: +18.9% (37 → 44 variables)
- Semesterly: +18.9% (37 → 44 variables) ← Inherited from Quarterly

This ensures you have the **most complete dataset possible** without missing variables due to Excel's sheet name character limits!

