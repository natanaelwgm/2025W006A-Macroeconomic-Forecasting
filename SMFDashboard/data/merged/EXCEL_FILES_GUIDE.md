# 📊 Excel Files - Complete Guide

All SMF datasets are now available in **Excel format (.xlsx)** with professional formatting!

---

## 📁 **Files Available**

### 1. **Master File (Recommended)** 🌟

**`SMF_All_Frequencies.xlsx`** (865 KB)

- **6 sheets in one file:**
  - 📊 Summary (overview of all datasets)
  - Monthly (43 vars × 870 obs)
  - Quarterly (44 vars × 304 obs)
  - Semesterly (44 vars × 146 obs)
  - Weekly (40 vars × 3,783 obs)
  - Yearly (44 vars × 112 obs)

- **Best for:**
  - Quick browsing and comparison
  - Switching between frequencies
  - Presenting to stakeholders
  - One-file distribution

### 2. **Individual Frequency Files**

| File | Size | Variables | Observations | Date Range |
|------|------|-----------|--------------|------------|
| `smf_monthly_data.xlsx` | 187 KB | 43 | 870 | 1953-2025 |
| `smf_quarterly_data.xlsx` | 79 KB | 44 | 304 | 1953-2025 |
| `smf_semesterly_data.xlsx` | 44 KB | 44 | 146 | 1953-2025 |
| `smf_weekly_data.xlsx` | 543 KB | 40 | 3,783 | 1953-2025 |
| `smf_yearly_data.xlsx` | 30 KB | 44 | 112 | 1954-2025 |

- **Best for:**
  - Focus on single frequency
  - Lighter file size
  - Email attachments
  - Specific analysis

---

## 🎨 **Formatting Features**

All Excel files include:

✅ **Professional Headers**
- Blue header row with white text
- Bold font
- Easy to read

✅ **Auto-Sized Columns**
- All columns automatically fitted to content
- Maximum width capped at 50 characters

✅ **Date Formatting**
- Dates displayed as `YYYY-MM-DD`
- Excel recognizes as date format
- Easy to filter and sort

✅ **Data Quality**
- All 215+ variables preserved
- No data loss from CSV conversion
- Numeric precision maintained

---

## 💡 **How to Use**

### Quick Start:

1. **Open Master File:**
   ```
   Open: SMF_All_Frequencies.xlsx
   ```

2. **Check Summary Sheet:**
   - First sheet shows overview
   - Lists all available frequencies
   - Date ranges and variable counts

3. **Navigate Between Frequencies:**
   - Click sheet tabs at bottom
   - Each frequency has its own sheet
   - Formatted and ready to use

### For Analysis:

**Option A: Use in Excel**
```excel
1. Open the file
2. Select your frequency sheet
3. Use Excel's Data > Filter
4. Create pivot tables, charts
5. Run Excel formulas
```

**Option B: Import to Python**
```python
import pandas as pd

# Read specific sheet
df = pd.read_excel('data/merged/SMF_All_Frequencies.xlsx', 
                   sheet_name='Quarterly',
                   parse_dates=['date'])

# Or read all sheets
all_data = pd.read_excel('data/merged/SMF_All_Frequencies.xlsx', 
                         sheet_name=None,
                         parse_dates=['date'])

# Access each frequency
monthly = all_data['Monthly']
quarterly = all_data['Quarterly']
```

**Option C: Import to R**
```r
library(readxl)

# Read specific sheet
quarterly_data <- read_excel("data/merged/SMF_All_Frequencies.xlsx", 
                             sheet = "Quarterly")

# Read all sheets
sheet_names <- excel_sheets("data/merged/SMF_All_Frequencies.xlsx")
all_data <- lapply(sheet_names, function(x) {
  read_excel("data/merged/SMF_All_Frequencies.xlsx", sheet = x)
})
names(all_data) <- sheet_names
```

---

## 📊 **Excel Features You Can Use**

### 1. **Filters & Sorting**
```
Select header row → Data → Filter
- Filter by date range
- Sort by any variable
- Find specific values
```

### 2. **Pivot Tables**
```
Insert → PivotTable
- Summarize by time periods
- Calculate statistics
- Cross-tabulate variables
```

### 3. **Charts & Visualizations**
```
Select data → Insert → Chart
- Time series plots
- Scatter plots
- Trend analysis
```

### 4. **Formulas & Calculations**
```
- AVERAGE, SUM, COUNT
- CORREL for correlations
- FORECAST for predictions
- Custom formulas
```

### 5. **Conditional Formatting**
```
Home → Conditional Formatting
- Highlight trends
- Color scales
- Data bars
```

---

## 🔍 **Data Structure**

### All Excel files follow this structure:

| Column | Type | Description |
|--------|------|-------------|
| `date` | Date | Time period (YYYY-MM-DD) |
| `Variable1` | Number | First economic indicator |
| `Variable2` | Number | Second economic indicator |
| ... | Number | ... |
| `VariableN` | Number | Last economic indicator |

### Frequencies:

- **Monthly:** First day of month (e.g., 2023-01-01)
- **Quarterly:** Last month of quarter (e.g., 2023-03-01)
- **Semesterly:** June 30 or December 30
- **Weekly:** Monday of each week
- **Yearly:** December 1st of each year

---

## 📈 **Common Use Cases**

### 1. **Time Series Visualization**
```
Steps:
1. Open SMF_All_Frequencies.xlsx
2. Go to Quarterly sheet
3. Select date + CPI + Real GDP Growth columns
4. Insert → Line Chart
5. Customize as needed
```

### 2. **Export for Presentation**
```
Steps:
1. Open desired frequency sheet
2. Select data range
3. Copy → Paste into PowerPoint/Word
4. Already formatted nicely!
```

### 3. **Quick Statistics**
```
Excel formulas:
=AVERAGE(B2:B305)     Average of first variable
=STDEV(B2:B305)       Standard deviation
=CORREL(B2:B305, C2:C305)  Correlation between variables
=MAX(B2:B305)         Maximum value
=MIN(B2:B305)         Minimum value
```

### 4. **Filter by Date Range**
```
Steps:
1. Click filter dropdown on date column
2. Select "Date Filters"
3. Choose "Between"
4. Enter start and end dates
5. Click OK
```

### 5. **Export to CSV (if needed)**
```
Steps:
1. Open Excel file
2. File → Save As
3. Choose "CSV (Comma delimited)"
4. Save
```

---

## 🎯 **Best Practices**

### For Excel Analysis:
- ✅ Use **Master File** for comparison across frequencies
- ✅ Use **Individual Files** for focused analysis
- ✅ Create a **backup** before making changes
- ✅ Use **Freeze Panes** (View → Freeze Top Row) for easier scrolling
- ✅ Save your analysis in a **separate workbook**

### For Data Integrity:
- ⚠️ Don't overwrite original files
- ⚠️ Don't delete columns without backing up
- ⚠️ Don't manually edit dates (use formulas)
- ⚠️ Check for filters before calculating statistics

### For Sharing:
- ✅ **Master File** is best for sharing (all data in one place)
- ✅ Add a **cover sheet** with metadata if needed
- ✅ **Protect sheets** to prevent accidental edits
- ✅ Use **Comments** to annotate unusual values

---

## 🔄 **Regenerating Excel Files**

If you update the CSV files and need to regenerate Excel:

```bash
cd /Users/schalkeanindya/SMFdashboard/data/merged

python3 << 'EOF'
import pandas as pd
from pathlib import Path

datasets = [
    ('Monthly', 'smf_monthly_data.csv'),
    ('Quarterly', 'smf_quarterly_data.csv'),
    ('Semesterly', 'smf_semesterly_data.csv'),
    ('Weekly', 'smf_weekly_data.csv'),
    ('Yearly', 'smf_yearly_data.csv')
]

# Convert each CSV to Excel
for freq_name, csv_file in datasets:
    df = pd.read_csv(csv_file, parse_dates=['date'])
    excel_file = csv_file.replace('.csv', '.xlsx')
    df.to_excel(excel_file, sheet_name=freq_name, index=False)
    print(f"✓ Created {excel_file}")

# Create master file
with pd.ExcelWriter('SMF_All_Frequencies.xlsx') as writer:
    for freq_name, csv_file in datasets:
        df = pd.read_csv(csv_file, parse_dates=['date'])
        df.to_excel(writer, sheet_name=freq_name, index=False)
    print("✓ Created SMF_All_Frequencies.xlsx")

EOF
```

---

## 📞 **File Locations**

All Excel files are in:
```
/Users/schalkeanindya/SMFdashboard/data/merged/
```

**Individual Files:**
- `smf_monthly_data.xlsx`
- `smf_quarterly_data.xlsx`
- `smf_semesterly_data.xlsx`
- `smf_weekly_data.xlsx`
- `smf_yearly_data.xlsx`

**Master File:**
- `SMF_All_Frequencies.xlsx` ⭐ **Start here!**

---

## ✅ **What's Included**

### All Excel Files Contain:

✅ **Complete Data**
- All 215 variables (deduplicated)
- 70+ years of data (1953-2025)
- Informal Employment (where available)
- All truncation fixes applied

✅ **Professional Formatting**
- Blue headers with white text
- Auto-sized columns
- Proper date formatting
- Ready for presentation

✅ **Data Quality**
- No missing truncated variables
- Duplicate variables renamed (JIBOR → JIBOR & JIBOR_1)
- All 32 recovered variables included
- Consistent structure across all files

---

## 🎉 **Summary**

You now have **6 Excel files** ready to use:

1. ⭐ **SMF_All_Frequencies.xlsx** - Master file with all data (RECOMMENDED)
2. 📅 **smf_monthly_data.xlsx** - Monthly data (43 vars)
3. 📊 **smf_quarterly_data.xlsx** - Quarterly + Informal Employment (44 vars)
4. 📈 **smf_semesterly_data.xlsx** - Semesterly aggregated (44 vars)
5. 📉 **smf_weekly_data.xlsx** - High frequency (40 vars)
6. 📆 **smf_yearly_data.xlsx** - Long-term + Informal Employment (44 vars)

**Total Size:** ~1.1 MB (all files combined)

**All files are professionally formatted and ready for:**
- ✅ Analysis in Excel
- ✅ Importing to Python/R
- ✅ Presentations
- ✅ Sharing with stakeholders
- ✅ Forecasting models
- ✅ Dashboard integration

---

**Open `SMF_All_Frequencies.xlsx` to get started! 🚀**



