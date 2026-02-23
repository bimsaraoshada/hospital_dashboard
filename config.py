"""
Configuration file for Hospital Dashboard
Modify these settings to customize the dashboard
"""

# Dashboard Settings
DASHBOARD_TITLE = "Hospital Management Dashboard"
DASHBOARD_ICON = "🏥"

# Data Settings
DEFAULT_NUM_PATIENTS = 100
DEFAULT_NUM_BEDS = 50
HISTORICAL_DAYS = 90

# Risk Level Thresholds
RISK_THRESHOLDS = {
    'low': 40,      # Risk score < 40 = Low
    'medium': 70    # 40 <= Risk score < 70 = Medium, >= 70 = High
}

# Bed Type Distribution (percentages)
BED_DISTRIBUTION = {
    'General': 0.60,    # 60%
    'ICU': 0.25,        # 25%
    'Emergency': 0.15   # 15%
}

# Vital Signs Normal Ranges
NORMAL_RANGES = {
    'heart_rate': (60, 100),
    'blood_pressure_systolic': (90, 140),
    'blood_pressure_diastolic': (60, 90),
    'temperature': (36.1, 37.2),
    'respiratory_rate': (12, 20),
    'oxygen_saturation': (95, 100)
}

# TabPFN Model Settings
TABPFN_CONFIG = {
    'device': 'cpu',  # Use 'cuda' if GPU available
    'N_ensemble_configurations': 4  # Reduce for faster predictions, increase for accuracy
}

# Color Scheme
COLORS = {
    'low_risk': '#4caf50',      # Green
    'medium_risk': '#ff9800',   # Orange
    'high_risk': '#f44336',     # Red
    'primary': '#2196F3',       # Blue
    'available': '#4caf50',     # Green
    'occupied': '#f44336',      # Red
    'maintenance': '#ff9800'    # Orange
}

# Data Refresh Settings
AUTO_REFRESH = False
REFRESH_INTERVAL_SECONDS = 60

# Export Settings
EXPORT_FORMAT = 'csv'  # Options: 'csv', 'excel', 'json'

# Alert Settings
ENABLE_ALERTS = True
ALERT_THRESHOLDS = {
    'high_risk_patients': 10,   # Alert if high risk patients exceed this
    'bed_occupancy': 90,        # Alert if occupancy exceeds this percentage
    'icu_occupancy': 85         # Alert if ICU occupancy exceeds this percentage
}
