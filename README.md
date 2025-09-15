# Indonesia Macroeconomic Nowcasting System

A comprehensive machine learning framework for nowcasting Indonesian macroeconomic indicators using direct multi-horizon forecasting.

## Overview

This system provides state-of-the-art nowcasting capabilities for key Indonesian economic indicators including:
- Consumer Price Index (CPI) Year-over-Year
- GDP Year-over-Year
- USD/IDR Exchange Rate
- Policy Rates (BI 7-Day Reverse Repo Rate)
- Deposit Rates (1M, 3M, 6M, 12M)

## Features

- **Multi-Model Framework**: Supports AR, Tree-based models (RandomForest, GradientBoosting, ExtraTrees), and ensemble methods
- **Direct Forecasting**: Independent models for each horizon (H=1, H=3, H=6 months)
- **Intelligent Caching**: Avoids redundant model training through smart result caching
- **Feature Engineering**: Automated lag generation, technical indicators, and normalization strategies
- **Comprehensive Reporting**: Enhanced reports with model diversity analysis and forecast visualizations

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/2025W006A-Macroeconomic-Forecasting.git
cd 2025W006A-Macroeconomic-Forecasting

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Single Target Forecasting
```bash
python3 run_v2.py recipes/test_quick.json --all
```

### Multi-Target Forecasting
```bash
python3 run_multi_targets.py recipes/recipe_multi_all_valid_y.json --verbose
```

### Generate Reports
```bash
python3 report_multi_targets_v2.py outputs/[output-directory]
```

## Project Structure

```
├── src/
│   ├── core/           # Core nowcasting engine
│   ├── models/         # Model implementations
│   └── utils/          # Utility functions
├── recipes/            # Configuration files for experiments
├── data/
│   └── processed/      # Processed data files
├── outputs/            # Model outputs and results
└── model_library/      # Cached models and results
```

## Model Performance

Recent results on Indonesian macroeconomic data (2005-2025):

| Indicator | Best Model | RMSE (H=1) | R² |
|-----------|------------|------------|-----|
| CPI YoY | AR1 | 0.73 | - |
| Policy Rate | AR1 | 0.28 | - |
| USD/IDR | AR1 | 502.65 | - |
| Deposit Rate 6M | AR1 | 0.29 | 0.92 |

## Configuration

Recipes are JSON configuration files that specify:
- Target variables and forecast horizons
- Data sources and date ranges
- Model types to evaluate
- Feature engineering parameters
- Output directories

Example recipe structure:
```json
{
  "target_id": "cpi_yoy",
  "horizons": [1, 3, 6],
  "strategy": "frozen",
  "train": {"start": "2005-01-31", "end": "2019-12-31"},
  "test": {"start": "2020-01-31", "end": "2025-07-31"},
  "models_filter": ["AR1", "RandomForest", "GradientBoosting"]
}
```

## Citation

If you use this system in your research, please cite:
```
@software{indonesia_nowcasting_2025,
  title={Indonesia Macroeconomic Nowcasting System},
  year={2025},
  url={https://github.com/yourusername/2025W006A-Macroeconomic-Forecasting}
}
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
