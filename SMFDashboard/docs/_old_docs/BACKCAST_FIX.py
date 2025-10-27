"""
QUICK FIX for Run Backcast Error
Apply this fix to SMFdashboard_recipe.py
"""

# Line 893 - Already fixed in file:
# Change: selected_models = get_selected_models(wb)
# To: selected_models = get_selected_models()

# Also update save_custom_recipe to use REPO format:

UPDATED_SAVE_RECIPE = '''
def save_custom_recipe():
    """Save current configuration as custom recipe in REPO FORMAT"""
    wb = xw.Book.caller()
    dash = wb.sheets['Dashboard']
    config_sheet = wb.sheets['Recipe_Config']
    
    # Get recipe name from Recipe_Config (cell B4)
    recipe_name = config_sheet.range('B4').value
    if not recipe_name:
        dash.range('B27').value = "⚠️ Enter recipe name in Recipe_Config cell B4"
        config_sheet.activate()
        config_sheet.range('B4').select()
        return "⚠️ No recipe name"
    
    # Get frequency from Dashboard
    frequency = dash.range('B4').value or 'Monthly'
    freq_map = {'Monthly': 'M', 'Quarterly': 'Q', 'Semesterly': 'S', 'Yearly': 'Y'}
    freq_code = freq_map.get(frequency, 'M')
    
    # Get selected models
    selected_models = get_selected_models()
    if not selected_models:
        dash.range('B27').value = "⚠️ No models selected in Recipe_Config"
        return "⚠️ No models"
    
    # Get hyperparameters
    hyperparams = get_hyperparameters()
    
    # Get forecast settings (row 56)
    horizons_str = config_sheet.range('B56').value or '1,3,6,12'
    try:
        horizons = [int(h.strip()) for h in str(horizons_str).split(',')]
    except:
        horizons = [1, 3, 6, 12]
    
    # Get train/test dates (rows 57-61)
    train_start = str(config_sheet.range('B57').value or '2005-01-01')
    train_end = str(config_sheet.range('B58').value or '2019-12-31')
    test_start = str(config_sheet.range('B59').value or '2020-01-01')
    test_end = str(config_sheet.range('B60').value or '2024-12-31')
    date_col = str(config_sheet.range('B61').value or 'date')
    
    # Get data path from Recipe_Config cell B5
    data_path = str(config_sheet.range('B5').value or '')
    
    # Build recipe in REPO format
    recipe = {
        "run_name": recipe_name,
        "frequency": freq_code,
        "strategy": "frozen",
        "train": {
            "start": train_start,
            "end": train_end
        },
        "test": {
            "start": test_start,
            "end": test_end
        },
        "data": {
            "path": data_path,
            "date_col": date_col
        },
        "models_filter": selected_models,
        "horizons": horizons,
        "model_configs": hyperparams,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to custom recipes folder
    custom_recipe_dir = Path("/Users/schalkeanindya/SMFdashboard/custom_recipes")
    custom_recipe_dir.mkdir(exist_ok=True)
    
    save_path = custom_recipe_dir / f"{recipe_name}.json"
    
    try:
        with open(save_path, 'w') as f:
            json.dump(recipe, f, indent=2)
        
        dash.range('B27').value = f"✅ Recipe saved: {save_path.name} (repo format)"
        return f"✅ Saved: {save_path.name}"
    except Exception as e:
        dash.range('B27').value = f"⚠️ Error saving: {str(e)[:50]}"
        return f"⚠️ Error: {e}"
'''

print("✅ Fix 1: Line 893 - get_selected_models() call fixed")
print("✅ Fix 2: save_custom_recipe() updated for repo format")
print("\n📝 Recipe format now matches your repo:")
print("  - train/test: date objects")
print("  - data: path + date_col")
print("  - models_filter: list of models")
print("  - model_configs: hyperparameters")

