"""
Sample Data Generator for Hospital Dashboard
Generates realistic patient and bed data for demonstration purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_patient_data(num_patients=100, seed=42):
    """
    Generate synthetic patient data with realistic medical parameters
    No data cleaning or feature engineering - raw data generation
    """
    np.random.seed(seed)
    random.seed(seed)
    
    # Patient demographics
    patient_ids = [f"P{str(i).zfill(5)}" for i in range(1, num_patients + 1)]
    ages = np.random.normal(55, 20, num_patients).astype(int).clip(1, 95)
    genders = np.random.choice(['Male', 'Female'], num_patients, p=[0.48, 0.52])
    
    # Admission dates (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    admission_dates = [
        start_date + timedelta(days=random.randint(0, 30))
        for _ in range(num_patients)
    ]
    
    # Primary diagnoses
    diagnoses = np.random.choice(
        ['Cardiac', 'Respiratory', 'Neurological', 'Trauma', 'Infection', 'Other'],
        num_patients,
        p=[0.20, 0.18, 0.15, 0.12, 0.20, 0.15]
    )
    
    # Vital signs - realistic distributions
    patients_data = []
    
    for i in range(num_patients):
        # Base vital signs
        age = ages[i]
        diagnosis = diagnoses[i]
        
        # Heart rate (bpm) - varies by age and condition
        base_hr = 75 + (age - 55) * 0.2
        if diagnosis in ['Cardiac', 'Infection']:
            hr_variation = 30
        else:
            hr_variation = 20
        heart_rate = int(np.clip(np.random.normal(base_hr, hr_variation), 45, 150))
        
        # Blood pressure (mmHg) - varies by age
        bp_sys = int(np.clip(np.random.normal(120 + age * 0.3, 20), 90, 200))
        bp_dias = int(np.clip(np.random.normal(80 + age * 0.1, 15), 60, 120))
        
        # Temperature (°C)
        if diagnosis == 'Infection':
            temp = np.clip(np.random.normal(38.2, 1.0), 36.0, 40.5)
        else:
            temp = np.clip(np.random.normal(37.0, 0.5), 36.0, 38.5)
        
        # Respiratory rate (/min)
        if diagnosis == 'Respiratory':
            resp_rate = int(np.clip(np.random.normal(22, 6), 12, 35))
        else:
            resp_rate = int(np.clip(np.random.normal(16, 4), 12, 25))
        
        # Oxygen saturation (%)
        if diagnosis in ['Respiratory', 'Cardiac']:
            o2_sat = int(np.clip(np.random.normal(94, 4), 85, 100))
        else:
            o2_sat = int(np.clip(np.random.normal(98, 2), 92, 100))
        
        # Calculate risk level based on vital signs and demographics
        risk_factors = 0
        
        # Age risk
        if age > 70:
            risk_factors += 2
        elif age > 60:
            risk_factors += 1
        
        # Vital signs risk
        if heart_rate > 100 or heart_rate < 60:
            risk_factors += 1
        if bp_sys > 140 or bp_sys < 90:
            risk_factors += 1
        if temp > 38.5:
            risk_factors += 1
        if resp_rate > 20:
            risk_factors += 1
        if o2_sat < 95:
            risk_factors += 2
        
        # Diagnosis risk
        if diagnosis in ['Cardiac', 'Neurological', 'Trauma']:
            risk_factors += 1
        
        # Determine risk level and score
        if risk_factors >= 5:
            risk_level = 'High'
            risk_score = 70 + np.random.uniform(0, 30)
        elif risk_factors >= 3:
            risk_level = 'Medium'
            risk_score = 40 + np.random.uniform(0, 30)
        else:
            risk_level = 'Low'
            risk_score = 0 + np.random.uniform(0, 40)
        
        # Length of stay (days)
        if risk_level == 'High':
            los = np.random.poisson(7) + 3
        elif risk_level == 'Medium':
            los = np.random.poisson(4) + 1
        else:
            los = np.random.poisson(2) + 1
        
        patients_data.append({
            'patient_id': patient_ids[i],
            'age': age,
            'gender': genders[i],
            'admission_date': admission_dates[i],
            'primary_diagnosis': diagnosis,
            'heart_rate': heart_rate,
            'blood_pressure_systolic': bp_sys,
            'blood_pressure_diastolic': bp_dias,
            'temperature': round(temp, 1),
            'respiratory_rate': resp_rate,
            'oxygen_saturation': o2_sat,
            'risk_score': round(risk_score, 2),
            'risk_level': risk_level,
            'length_of_stay': los
        })
    
    df = pd.DataFrame(patients_data)
    
    # Sort by admission date
    df = df.sort_values('admission_date', ascending=False).reset_index(drop=True)
    
    return df

def generate_bed_data(num_beds=50, seed=42):
    """
    Generate hospital bed availability data
    """
    np.random.seed(seed)
    random.seed(seed)
    
    # Bed types distribution
    bed_types = []
    bed_types.extend(['General'] * int(num_beds * 0.60))  # 60% general
    bed_types.extend(['ICU'] * int(num_beds * 0.25))      # 25% ICU
    bed_types.extend(['Emergency'] * int(num_beds * 0.15)) # 15% emergency
    
    # Ensure we have exactly num_beds
    while len(bed_types) < num_beds:
        bed_types.append('General')
    bed_types = bed_types[:num_beds]
    
    # Shuffle bed types
    random.shuffle(bed_types)
    
    beds_data = []
    
    for i, bed_type in enumerate(bed_types, start=1):
        bed_id = f"B{str(i).zfill(3)}"
        
        # Determine floor based on type
        if bed_type == 'ICU':
            floor = random.choice([3, 4])
        elif bed_type == 'Emergency':
            floor = 1
        else:
            floor = random.choice([2, 3, 4, 5])
        
        # Room number
        room = f"{floor}{str(random.randint(1, 50)).zfill(2)}"
        
        # Bed status (realistic occupancy: ~75%)
        if bed_type == 'ICU':
            # ICU typically has higher occupancy
            status = np.random.choice(['Available', 'Occupied', 'Maintenance'], p=[0.15, 0.80, 0.05])
        elif bed_type == 'Emergency':
            # Emergency has variable occupancy
            status = np.random.choice(['Available', 'Occupied', 'Maintenance'], p=[0.30, 0.65, 0.05])
        else:
            # General wards
            status = np.random.choice(['Available', 'Occupied', 'Maintenance'], p=[0.25, 0.70, 0.05])
        
        # Patient ID if occupied
        patient_id = f"P{str(random.randint(1, 100)).zfill(5)}" if status == 'Occupied' else None
        
        # Last cleaned timestamp
        hours_ago = random.randint(1, 24)
        last_cleaned = datetime.now() - timedelta(hours=hours_ago)
        
        beds_data.append({
            'bed_id': bed_id,
            'bed_number': i,
            'type': bed_type,
            'floor': floor,
            'room': room,
            'status': status,
            'patient_id': patient_id,
            'last_cleaned': last_cleaned,
            'has_ventilator': bed_type == 'ICU' and random.random() > 0.3,
            'has_monitor': bed_type in ['ICU', 'Emergency'] or random.random() > 0.5
        })
    
    df = pd.DataFrame(beds_data)
    
    # Sort by bed type and number
    df = df.sort_values(['type', 'bed_number']).reset_index(drop=True)
    
    return df

def generate_historical_data(days=90, seed=42):
    """
    Generate historical data for trend analysis
    """
    np.random.seed(seed)
    
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    
    historical_data = []
    
    base_admissions = 15
    base_discharges = 14
    
    for i, date in enumerate(dates):
        # Add seasonal variation
        seasonal_factor = 1 + 0.2 * np.sin(i / 30 * np.pi)
        
        admissions = int(np.random.poisson(base_admissions * seasonal_factor))
        discharges = int(np.random.poisson(base_discharges * seasonal_factor))
        
        # Risk distribution
        high_risk = max(0, int(np.random.normal(admissions * 0.2, 2)))
        medium_risk = max(0, int(np.random.normal(admissions * 0.35, 3)))
        low_risk = admissions - high_risk - medium_risk
        
        historical_data.append({
            'date': date,
            'admissions': admissions,
            'discharges': discharges,
            'high_risk_admissions': high_risk,
            'medium_risk_admissions': medium_risk,
            'low_risk_admissions': low_risk,
            'average_los': np.random.normal(4.5, 1.5),
            'bed_occupancy_rate': np.random.uniform(65, 90)
        })
    
    return pd.DataFrame(historical_data)

def simulate_realtime_patient():
    """
    Simulate a new patient admission with random vital signs
    """
    age = random.randint(20, 85)
    gender = random.choice(['Male', 'Female', 'Other'])
    diagnosis = random.choice(['Cardiac', 'Respiratory', 'Neurological', 'Trauma', 'Infection', 'Other'])
    
    # Generate realistic vital signs
    heart_rate = random.randint(60, 120)
    bp_sys = random.randint(100, 160)
    bp_dias = random.randint(60, 100)
    temp = round(random.uniform(36.5, 38.5), 1)
    resp_rate = random.randint(12, 25)
    o2_sat = random.randint(90, 100)
    
    return {
        'age': age,
        'gender': gender,
        'primary_diagnosis': diagnosis,
        'heart_rate': heart_rate,
        'blood_pressure_systolic': bp_sys,
        'blood_pressure_diastolic': bp_dias,
        'temperature': temp,
        'respiratory_rate': resp_rate,
        'oxygen_saturation': o2_sat,
        'admission_date': datetime.now()
    }

if __name__ == "__main__":
    # Test data generation
    print("Generating sample data...")
    
    patients = generate_patient_data(100)
    print(f"\nGenerated {len(patients)} patients")
    print(patients.head())
    print(f"\nRisk distribution:")
    print(patients['risk_level'].value_counts())
    
    beds = generate_bed_data(50)
    print(f"\nGenerated {len(beds)} beds")
    print(beds.head())
    print(f"\nBed status:")
    print(beds['status'].value_counts())
    
    historical = generate_historical_data(30)
    print(f"\nGenerated {len(historical)} days of historical data")
    print(historical.head())
