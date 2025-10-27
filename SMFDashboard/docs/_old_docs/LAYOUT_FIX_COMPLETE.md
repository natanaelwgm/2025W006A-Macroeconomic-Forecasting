# 🎨 RECIPE_CONFIG LAYOUT FIX - Complete

## ✅ Problem Solved

**Issue:** Target variables were overwriting forecast settings (same columns A-C)

**Solution:** Reorganized Recipe_Config into 3-column layout:
- **Left (A-C):** Models + Settings
- **Middle (E-G):** Target/Outcome Variables  
- **Right (I-K):** Exogenous/Feature Variables

---

## 📐 New Recipe_Config Layout

```
┌─────────────────┬───────────────────┬──────────────────┐
│   LEFT (A-C)    │  MIDDLE (E-G)     │   RIGHT (I-K)    │
├─────────────────┼───────────────────┼──────────────────┤
│ Recipe Name     │ TARGET VARIABLES  │ EXOG VARIABLES   │
│ Data Path       │                   │                  │
│                 │ [✓] CPI      1,3  │ [ ] CPI      0,1 │
│ MODELS (44)     │ [✓] GDP      1,3  │ [ ] GDP      0,1 │
│ [✓] Naive       │ [✓] BI7DRR   1,3  │ [ ] BI7DRR   0,1 │
│ [✓] Linear      │ [✓] FX       1,3  │ [ ] FX       0,1 │
│ [✓] Ridge       │ ...               │ ...              │
│ ...             │                   │                  │
│ (rows 10-53)    │ (rows 10-59)      │ (rows 10-59)     │
│                 │                   │                  │
│ SETTINGS        │                   │                  │
│ Frequency       │                   │                  │
│ Horizons        │                   │                  │
│ Train Dates     │                   │                  │
│ Test Dates      │                   │                  │
│ (rows 54-62)    │                   │                  │
│                 │                   │                  │
│ HYPERPARAMS     │                   │                  │
│ (rows 64+)      │                   │                  │
└─────────────────┴───────────────────┴──────────────────┘
```

---

## 📍 Detailed Section Locations

### Left Column (A-C): Models & Settings

| Rows | Section | Content |
|------|---------|---------|
| 1-7 | Header | Recipe name, data path, dataset info |
| 8-9 | Models Header | "SELECT MODELS TO TEST" |
| 10-53 | **Models List** | 44 models with checkboxes |
| 54 | Settings Header | "FORECAST SETTINGS & DATA FREQUENCY" |
| 55 | Column Headers | Setting / Value / Description |
| 56 | Data Frequency | Monthly/Quarterly/etc (auto-detected) |
| 57 | Horizons | Comma-separated (e.g., 1,3,6,12) |
| 58 | Train Start Date | YYYY-MM-DD format |
| 59 | Train End Date | YYYY-MM-DD format |
| 60 | Test Start Date | YYYY-MM-DD format |
| 61 | Test End Date | YYYY-MM-DD format |
| 62 | Date Column | Column name (e.g., 'date') |
| 64+ | Hyperparameters | Model-specific settings |

### Middle Column (E-G): Target Variables

| Rows | Content |
|------|---------|
| 8 | Header: "TARGET/OUTCOME VARIABLES" |
| 9 | Column Headers: ✓ / Variable Name / Horizons |
| 10-59 | **Target variables** (up to 50, auto-populated) |

**Format:**
- Column E: Checkbox (✓ = forecast this variable)
- Column F: Variable name
- Column G: Horizons for this variable (e.g., "1,3,6,12")

**Behavior:**
- ✅ Checked by default when data loads
- ✏️ Editable: Uncheck to exclude from forecast
- 🎯 Per-variable horizons customizable

### Right Column (I-K): Exogenous Variables

| Rows | Content |
|------|---------|
| 8 | Header: "EXOGENOUS/FEATURE VARIABLES" |
| 9 | Column Headers: ✓ / Variable Name / Lags |
| 10-59 | **Exog variables** (up to 50, auto-populated) |

**Format:**
- Column I: Checkbox (✓ = use as feature)
- Column J: Variable name  
- Column K: Lags to use (e.g., "0,1" = current + 1 lag)

**Behavior:**
- ❌ Unchecked by default
- ✏️ Check to include as explanatory variable
- 🔢 Customize lags per variable

---

## 🔑 Key Cell References

### Recipe Info:
```
B4  = Recipe Name
B5  = Data Path
B6  = Dataset Info (read-only)
```

### Models (Checklist):
```
A10-A53  = Model checkboxes
B10-B53  = Model names
C10-C53  = Model descriptions
```

### Settings:
```
B56 = Data Frequency (Monthly/Quarterly/Semesterly/Yearly)
B57 = Horizons (comma-separated)
B58 = Train Start Date
B59 = Train End Date
B60 = Test Start Date
B61 = Test End Date
B62 = Date Column Name
```

### Target Variables:
```
E10-E59 = Target checkboxes
F10-F59 = Target variable names
G10-G59 = Target-specific horizons
```

### Exog Variables:
```
I10-I59 = Exog checkboxes
J10-J59 = Exog variable names
K10-K59 = Exog variable lags
```

---

## 🚀 How It Works Now

### 1. Load Data
```python
Click: [Load Real Data]

Auto-populates:
✓ Data Frequency (B56) based on date intervals
✓ Target Variables (E10-E59) - ALL CHECKED
✓ Exog Variables (I10-I59) - ALL UNCHECKED
✓ Default horizons based on frequency
```

### 2. Select Targets
```
Go to column E (rows 10+)
✓ Check = forecast this variable
☐ Uncheck = skip this variable

Customize horizons in column G if needed
(Each variable can have different horizons!)
```

### 3. Select Exog Variables
```
Go to column I (rows 10+)
☐ Default = not used
✓ Check = use as explanatory variable

Customize lags in column K:
"0,1"    = current + 1 lag
"0,1,3"  = current + lags 1 and 3
"1,2,3"  = lags 1, 2, and 3 only
```

### 4. Run Analysis
```
[Run Backcast]
→ Uses only CHECKED targets (column E)
→ Uses only CHECKED exog vars (column I)
→ Applies appropriate lags to exog vars

[Refresh Charts]
→ Creates charts for CHECKED targets only
→ Can incorporate exog variables in models
```

---

## 📊 Example Usage

### Forecasting CPI with Features:

**Targets (E-G):**
```
✓ CPI             1,3,6,12
☐ GDP Growth      (unchecked - not forecasting)
☐ BI7DRR          (unchecked)
```

**Exog Variables (I-K):**
```
☐ CPI             (don't use own lags)
✓ GDP Growth      0,1,3     (current + lags 1,3)
✓ Money Supply    0,1       (current + lag 1)
✓ Oil Price       0,1,3,6   (current + lags 1,3,6)
```

**Result:**
- Forecasts only CPI (horizons 1,3,6,12)
- Uses GDP, Money Supply, Oil Price as features
- Each with specified lags

---

## 🔄 Functions Updated

### 1. `setup_recipe_config_sheet()`
- Reorganized layout into 3 sections
- Target section: E8-G10 (header)
- Exog section: I8-K10 (header)
- Settings: A54-C62 (left side)

### 2. `load_data_from_recipe()`
- Populates targets in columns E-G (rows 10+)
- Populates exog vars in columns I-K (rows 10+)
- Targets checked by default
- Exog unchecked by default
- Up to 50 variables each

### 3. `get_selected_targets()` 
- Reads from E10-E59 (checkboxes)
- Reads from F10-F59 (names)
- Reads from G10-G59 (horizons)
- Returns list of checked targets with horizons

### 4. `get_selected_exog()` NEW
- Reads from I10-I59 (checkboxes)
- Reads from J10-J59 (names)
- Reads from K10-K59 (lags)
- Returns list of checked exog vars with lags

### 5. All Cell References Updated
- Settings now at B56-B62 (was B61-B67)
- No more overlap with target variables
- All functions use correct cell refs

---

## ✅ Benefits

1. **No Overlap** - Settings and variables in different columns
2. **Exog Support** - Can select explanatory variables
3. **Per-Variable Control** - Custom horizons/lags per variable
4. **Visual Clarity** - Three distinct sections
5. **Scalable** - Up to 50 variables each section
6. **Flexible** - Mix and match targets/exog as needed

---

## 🎓 Advanced Use Cases

### Case 1: Multiple Targets with Shared Features
```
Targets (E):        Exog (I):
✓ CPI               ✓ Oil Price
✓ GDP               ✓ FX Rate
✓ Unemployment      ✓ Interest Rate

Forecast all 3 targets using the same 3 exog features
```

### Case 2: Single Target with Many Features
```
Target (E):         Exog (I):
✓ GDP               ✓ CPI
                    ✓ Money Supply
                    ✓ Credit Growth
                    ✓ PMI
                    ✓ Exports
                    ✓ Oil Price
                    ✓ FX Rate

Forecast GDP using 7 explanatory variables
```

### Case 3: Different Horizons Per Target
```
Targets (E-G):
✓ CPI          1,3,6,12        (short to medium term)
✓ GDP          1,4,8           (quarterly intervals)
✓ Debt/GDP     1,2,3,5         (long term)
```

---

## 📝 Cell Reference Summary

| What | Old Location | New Location | Why |
|------|-------------|--------------|-----|
| Target Variables | A56-C86 | E10-G59 | Avoid settings overlap |
| Exog Variables | N/A | I10-K59 | NEW feature |
| Data Frequency | B61 | B56 | Settings consolidated |
| Horizons | B62 | B57 | Settings moved up |
| Train Start | B63 | B58 | Settings moved up |
| Train End | B64 | B59 | Settings moved up |
| Test Start | B65 | B60 | Settings moved up |
| Test End | B66 | B61 | Settings moved up |
| Date Column | B67 | B62 | Settings moved up |

---

## 🔧 Migration Notes

### From Previous Version:
1. Old recipes still work (no breaking changes)
2. Target selection now in middle columns (E-G)
3. New exog selection feature (I-K)
4. Settings cell refs updated (B56-B62)

### First Time Setup:
1. Close Excel completely
2. Delete Recipe_Config sheet manually (if exists)
3. Reopen Excel
4. Click "Setup Recipe Dashboard"
5. Load your data → auto-populates!

---

## 🎉 What's New

- ✅ Target variables don't overwrite settings
- ✅ Exogenous variable selection
- ✅ Up to 50 variables (was 30)
- ✅ Cleaner 3-column layout
- ✅ Per-variable horizons AND lags
- ✅ Visual separation of concerns

---

**Version:** 4.0
**Date:** 2025-10-26  
**Status:** ✅ Layout fixed, exog support added
**Compatibility:** All data frequencies supported

