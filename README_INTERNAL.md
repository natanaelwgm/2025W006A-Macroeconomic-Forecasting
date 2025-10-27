# Internal Testing - Macroeconomic Forecasting Models

**Internal Repository for Model Testing and Development**  
*Private testing environment for implementing and evaluating econometric and ML models*

## 🎯 Project Overview

This repository contains internal testing implementations for macroeconomic nowcasting models as requested by management. The system focuses on Indonesian economic indicators using both traditional econometric models and modern machine learning approaches.

## 📊 Current Status (September 2025)

### ✅ **Implemented & Tested Models**
| Model Category | Model | Status | Performance |
|---------------|-------|--------|-------------|
| **Econometric** | DFM (Dynamic Factor Model) | ✅ Working | 🏆 **Best for CPI** (RMSE: 0.6013) |
| **Econometric** | DFM2 (2-Factor DFM) | ✅ Working | Excellent |
| **ML Regression** | ElasticNet | ✅ Working | Strong (RMSE: 0.6426) |
| **ML Regression** | Lasso | ✅ Working | Good (RMSE: 0.6484) |
| **ML Regression** | Ridge | ✅ Working | Excellent (RMSE: 0.6401) |
| **ML Ensemble** | RandomForest | ✅ Working | Good (RMSE: 0.9330+) |
| **Baseline** | AR1/ARp | ✅ Working | Competitive |

### 🔄 **Models To Be Implemented**
| Model | Priority | Purpose | Target Timeline |
|-------|----------|---------|-----------------|
| **BVAR** (Bayesian VAR) | High | Feedback loops between variables | Week 1 |
| **MIDAS** (Mixed Data Sampling) | High | Mixed-frequency data handling | Week 2 |
| **GARCH/TVP** | Medium | Volatility modeling (USD/IDR) | Week 3 |
| **LSTM** | Medium | Deep learning approach | Week 4 |

## 📈 **Key Targets & Performance**

### Indonesian Macroeconomic Indicators:
- **CPI Year-over-Year**: ✅ Best model: DFM2 (RMSE: 0.6013)
- **GDP Year-over-Year**: ✅ Best model: AR1 (RMSE: 2.2174) 
- **Policy Rate (BI 7DRR)**: ✅ Best model: AR1 (RMSE: 0.3129)
- **USD/IDR Exchange Rate**: ⚠️ Needs additional data processing

## 🚀 **Quick Start**

### Prerequisites
```bash
python3 -m pip install pandas numpy matplotlib seaborn
```

### Running Tests
```bash
# Test existing priority models
python3 run_multi_targets.py recipes/2109_model_test.json --verbose

# Generate enhanced report
python3 report_multi_targets_v2.py outputs/[latest-output-directory]
```

### Data Setup
- **Source**: Excel files with Indonesian macro data (1969-2025)
- **Processed**: `data/processed/indonesia_macro_monthly.csv` (679 rows, 14 variables)
- **Frequency**: Monthly data with end-of-month timestamps

## 📁 **Project Structure**

```
├── src/
│   ├── core/              # Core nowcasting engine
│   └── models/            # Model implementations
│       ├── ar1/           # Autoregressive models ✅
│       ├── dfm/           # Dynamic Factor Models ✅
│       ├── elastic_net/   # ElasticNet regression ✅
│       ├── lasso/         # Lasso regression ✅
│       ├── ridge/         # Ridge regression ✅
│       ├── random_forest/ # Random Forest ✅
│       ├── bvar/          # 🔄 BVAR (to implement)
│       ├── midas/         # 🔄 MIDAS (to implement)
│       ├── garch_tvp/     # 🔄 GARCH/TVP (to implement)
│       └── lstm/          # 🔄 LSTM (to implement)
├── recipes/               # Configuration files
├── data/                  # Data files
├── outputs/               # Model results and reports
├── IMPLEMENTATION_TODO.md # Detailed implementation plan
└── README_INTERNAL.md     # This file
```

## 🔧 **Development Workflow**

### Testing New Models
1. **Create model**: Implement in `src/models/[model_name]/`
2. **Follow interface**: Inherit from `BaseModel` class
3. **Test individually**: Use single-target recipes first
4. **Multi-target test**: Run comprehensive evaluation
5. **Generate report**: Create enhanced performance report

### Model Implementation Template
```python
# src/models/[model_name]/model.py
from core.base import BaseModel

NAME = "ModelName"
SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [1]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any"
}

class _ModelClass(BaseModel):
    def fit(self, X, y): ...
    def predict_row(self, x_row): ...
    def get_params(self): ...
    def set_params(self, params): ...

def create(params):
    return _ModelClass(**params)
```

## 📊 **Latest Results (2109 Test)**

**Generated**: 2025-09-22 00:28:39  
**Output**: `outputs/2109_model_test-20250922-002632/ENHANCED_REPORT.md`

### Top Performers by Target:
- **CPI YoY**: DFM2 (0.6013 RMSE) → Excellent for inflation nowcasting
- **GDP YoY**: AR1 (2.2174 RMSE) → Simple models work well  
- **Policy Rate**: AR1 (0.3129 RMSE) → Autoregressive patterns strong
- **USD/IDR**: Data processing needed → Priority for GARCH implementation

## 🎯 **Internal Testing Objectives**

1. **✅ Validate existing implementations** - COMPLETED
2. **🔄 Implement missing econometric models** - IN PROGRESS
3. **🔄 Add deep learning capabilities** - PLANNED
4. **📈 Optimize hyperparameters** - ONGOING
5. **📊 Generate comparative reports** - AUTOMATED

## 📝 **Notes for Development Team**

- **Framework**: Plugin-based architecture allows easy model addition
- **Caching**: Intelligent caching system prevents redundant training
- **Reporting**: Automated enhanced reports with visualizations
- **Data**: Monthly Indonesian macro data from 1969-2025
- **Testing**: Multi-target, multi-horizon evaluation framework

## 🔒 **Internal Use Only**

This repository contains proprietary model implementations and testing frameworks. All code and results are for internal evaluation purposes only.

---
**Last Updated**: September 2025  
**Status**: Active Development  
**Next Milestone**: Complete BVAR implementation
