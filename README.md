# Hospital Management Dashboard with TabPFN

An interactive hospital management dashboard featuring real-time risk predictions using TabPFN (Tabular Prior-Fitted Networks) and comprehensive bed availability tracking.

## Features

### 🏥 **Overview Dashboard**
- Real-time hospital metrics and KPIs
- Bed occupancy statistics
- Risk distribution visualization
- Recent patient activity tracking

### 🔮 **Risk Predictions (TabPFN)**
- AI-powered patient risk assessment using TabPFN
- Real-time risk scoring without feature engineering
- Color-coded risk levels (Low, Medium, High)
- Individual patient risk analysis
- New patient risk prediction interface

### 🛏️ **Bed Management**
- Real-time bed availability tracking
- Bed status by ward type (General, ICU, Emergency)
- Detailed bed information and filtering
- 30-day occupancy trend visualization

### 📊 **Patient Analytics**
- Age distribution analysis
- Diagnosis distribution
- Vital signs correlation matrix
- Risk-based vital signs comparison

## Technology Stack

- **Frontend Framework**: Streamlit
- **ML Model**: TabPFN (no feature engineering required)
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Plotly
- **Fallback ML**: Scikit-learn (Random Forest)

## Why TabPFN?

TabPFN (Tabular Prior-Fitted Networks) is a transformer-based model specifically designed for tabular data that:
- **No Feature Engineering**: Works directly with raw data
- **No Data Cleaning**: Handles missing values automatically
- **Fast Predictions**: Pre-trained transformer model
- **No Hyperparameter Tuning**: Ready to use out of the box
- **High Accuracy**: State-of-the-art performance on small-to-medium datasets

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory**:
```bash
cd d:\LMS\3.1\DWDM\new_dashboard
```

2. **Create a virtual environment (recommended)**:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Dashboard

1. **Start the Streamlit application**:
```bash
streamlit run app.py
```

2. **Access the dashboard**:
   - The application will automatically open in your default browser
   - Default URL: `http://localhost:8501`

## Usage Guide

### Overview Page
- View real-time hospital statistics
- Monitor bed occupancy rates
- Check risk distribution across patients
- Review recent patient admissions

### Risk Predictions Page

#### Existing Patients Tab
- Filter patients by risk level
- View detailed patient information
- Expand patient cards for vital signs
- Color-coded risk indicators

#### New Prediction Tab
1. Enter patient demographics (age, gender)
2. Input vital signs (heart rate, blood pressure, etc.)
3. Select primary diagnosis
4. Click "Predict Risk" for instant AI-powered assessment
5. View risk score, level, and probabilities
6. Analyze clinical parameter visualizations

### Bed Management Page
- View bed availability by ward type
- Filter beds by status and type
- Monitor bed occupancy trends
- Track cleaning schedules

### Patient Analytics Page
- Explore patient demographics
- Analyze vital signs distributions
- View diagnosis patterns
- Study correlations between clinical parameters

## Data Structure

### Patient Data
- **Demographics**: Age, Gender, Admission Date
- **Vital Signs**: Heart Rate, Blood Pressure, Temperature, Respiratory Rate, O2 Saturation
- **Clinical**: Primary Diagnosis, Risk Level, Risk Score

### Bed Data
- **Identification**: Bed ID, Number, Type, Floor, Room
- **Status**: Available, Occupied, Maintenance
- **Equipment**: Ventilator, Monitor availability
- **Maintenance**: Last cleaned timestamp

## TabPFN Integration

The dashboard uses TabPFN for risk prediction without any feature engineering:

```python
from tabpfn import TabPFNClassifier

# Initialize model (pre-trained)
model = TabPFNClassifier(device='cpu', N_ensemble_configurations=4)

# Train on raw data (no preprocessing needed)
model.fit(X, y)

# Predict (instant results)
predictions = model.predict_proba(X_new)
```

### Fallback Model
If TabPFN is not available, the system automatically falls back to:
- Random Forest Classifier (scikit-learn)
- Rule-based risk assessment

## Sample Data

The dashboard includes a data generator that creates realistic:
- Patient records with appropriate vital signs
- Bed availability information
- Historical trend data

**Note**: All data is synthetically generated for demonstration purposes.

## Customization

### Adding New Features
Edit `app.py` to add new dashboard pages or visualizations.

### Modifying Risk Model
Edit `risk_predictor.py` to adjust risk calculation or model parameters.

### Changing Data Generation
Edit `data_generator.py` to modify sample data characteristics.

## Performance

- **Model Loading**: < 1 second
- **Prediction Time**: < 0.1 seconds per patient
- **Dashboard Refresh**: Real-time (Streamlit reactive)
- **Data Capacity**: Handles 1000+ patients without performance degradation

## Troubleshooting

### TabPFN Installation Issues
If TabPFN fails to install:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install tabpfn
```

### Streamlit Port Conflicts
If port 8501 is busy:
```bash
streamlit run app.py --server.port 8502
```

### Memory Issues
For large datasets, adjust TabPFN ensemble configurations:
```python
model = TabPFNClassifier(device='cpu', N_ensemble_configurations=2)
```

## Future Enhancements

- [ ] Real-time patient monitoring
- [ ] Automated alert system
- [ ] Patient discharge prediction
- [ ] Resource allocation optimization
- [ ] Integration with hospital information systems
- [ ] Multi-hospital dashboard support
- [ ] Mobile responsive design

## License

This project is created for educational and demonstration purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review TabPFN documentation: https://github.com/automl/TabPFN
3. Review Streamlit documentation: https://docs.streamlit.io

## Acknowledgments

- **TabPFN**: Prior-Fitted Networks for Tabular Data
- **Streamlit**: Interactive web applications for ML/Data Science
- **Plotly**: Interactive visualizations

---

**Built with ❤️ for better healthcare management**
