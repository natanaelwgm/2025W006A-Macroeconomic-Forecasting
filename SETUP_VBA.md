# VBA Setup Instructions

## How to Add VBA Macros to Excel

1. **Open `SMFdashboard.xlsm` in Excel**

2. **Enable Developer Tab:**
   - Excel Menu → Preferences
   - → Ribbon & Toolbar
   - → Check "Developer" in the right column
   - → OK

3. **Open VBA Editor:**
   - Developer Tab → Visual Basic (or press `Alt + F11` on Windows, `Option + F11` on Mac)

4. **Import Modules:**

   a. **Insert → Module** (create new module)
   
   b. **Copy all code** from `VBA_CODE_RECIPE_V2.txt`
   
   c. **Paste** into the module
   
   d. **Save** (Command + S / Ctrl + S)

5. **Add Button to Dashboard:**

   a. Go to **Dashboard** sheet
   
   b. **Developer Tab → Insert → Button** (from Form Controls)
   
   c. **Draw button** on the sheet
   
   d. **Right-click** the button → **Assign Macro**
   
   e. **Select** `LoadRealData` from the list
   
   f. **Click OK**

6. **Repeat for other buttons:**

   - Create buttons and assign these macros:
     - `RunBackcast` → "Run Backcast" button
     - `RefreshCharts` → "Refresh Charts" button
     - `RunForecast` → "Run Forecast" button
     - `ViewModelRankings` → "View Rankings" button
     - `LoadRealData` → "Load Data" button

## Quick Buttons List

Copy these button names when creating buttons:

```
📥 Load Data          → LoadRealData()
🔍 Run Backcast       → RunBackcast()
📊 Refresh Charts     → RefreshCharts()
🔮 Run Forecast       → RunForecast()
🏆 View Rankings      → ViewModelRankings()
```

## Save Your Work

1. **Save as Macro-Enabled Workbook:**
   - File → Save As
   - Format: Excel Macro-Enabled Workbook (.xlsm)
   - Name: `SMFdashboard.xlsm`

2. **Verify Macros are enabled:**
   - Open Excel → Security Preferences
   - → Enable "Disable all macros with notification"

## Testing

1. Click **"Load Data"** button
2. Should see status update in cell `B27`
3. Click **"Run Backcast"**
4. Should see progress in `B27`
5. Click **"Refresh Charts"**
6. Charts should appear on Dashboard

## Troubleshooting

**"Macros are disabled" Error:**
- Go to Excel → Preferences → Security
- → Check "Enable all macros" (temporary)
- OR use "Disable all macros with notification" (recommended)
- → When opening, click "Enable Macros"

**Button doesn't do anything:**
- Check that macro is assigned (right-click button → Assign Macro)
- Verify macro exists in VBA editor

**Python errors:**
- Make sure Python path is correct in xlwings
- Tools → References → Check "xlwings" is referenced

---

**Once VBA is set up, you're ready to use the dashboard!** ✅
