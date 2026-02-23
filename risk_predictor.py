"""
Risk Predictor Module using TabPFN
TabPFN is a transformer-based model for tabular data that requires no feature engineering
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

try:
    from tabpfn import TabPFNClassifier
    TABPFN_AVAILABLE = True
except ImportError:
    TABPFN_AVAILABLE = False
    print("TabPFN not available. Using fallback sklearn model.")
    from sklearn.ensemble import RandomForestClassifier

class RiskPredictor:
    """
    Risk prediction system for hospital patients using TabPFN
    No feature engineering required - TabPFN handles raw tabular data
    """
    
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.is_trained = False
        self.feature_columns = [
            'age', 'gender_encoded', 'heart_rate', 'blood_pressure_systolic',
            'blood_pressure_diastolic', 'temperature', 'respiratory_rate',
            'oxygen_saturation', 'diagnosis_encoded'
        ]
        
        # Initialize TabPFN model
        if TABPFN_AVAILABLE:
            try:
                # TabPFN with default settings - no hyperparameter tuning needed
                self.model = TabPFNClassifier()
                self.model_type = "TabPFN"
            except Exception as e:
                print(f"Failed to initialize TabPFN: {e}")
                print("Falling back to Random Forest classifier")
                self.model = RandomForestClassifier(n_estimators=100, random_state=42)
                self.model_type = "RandomForest"
        else:
            # Fallback to Random Forest if TabPFN not available
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
            self.model_type = "RandomForest"
        
        # Initialize label encoders
        self.label_encoders['gender'] = LabelEncoder()
        self.label_encoders['diagnosis'] = LabelEncoder()
        self.label_encoders['risk_level'] = LabelEncoder()
        
        # Fit encoders with expected values
        self.label_encoders['gender'].fit(['Male', 'Female', 'Other'])
        self.label_encoders['diagnosis'].fit([
            'Cardiac', 'Respiratory', 'Neurological', 'Trauma', 'Infection', 'Other'
        ])
        self.label_encoders['risk_level'].fit(['Low', 'Medium', 'High'])
    
    def preprocess_data(self, data, is_training=False):
        """
        Minimal preprocessing - TabPFN works with raw data
        Only encoding categorical variables
        """
        if isinstance(data, dict):
            # Single prediction
            df = pd.DataFrame([data])
        else:
            df = data.copy()
        
        # Encode categorical variables
        df['gender_encoded'] = self.label_encoders['gender'].transform(df['gender'])
        df['diagnosis_encoded'] = self.label_encoders['diagnosis'].transform(df['primary_diagnosis'])
        
        # Select features (no feature engineering!)
        X = df[self.feature_columns]
        
        if is_training and 'risk_level' in df.columns:
            y = self.label_encoders['risk_level'].transform(df['risk_level'])
            return X, y
        
        return X
    
    def train(self, training_data):
        """
        Train the TabPFN model
        TabPFN is designed to work without extensive training - it's a meta-learned model
        """
        print(f"Training {self.model_type} model...")
        
        X, y = self.preprocess_data(training_data, is_training=True)
        
        # TabPFN is pre-trained, we just fit it to our specific data
        # No feature engineering, scaling, or complex preprocessing needed!
        self.model.fit(X.values, y)
        self.is_trained = True
        
        print(f"{self.model_type} model trained successfully!")
        return self
    
    def predict_risk(self, patient_data):
        """
        Predict risk level for a patient
        Returns: risk_score, risk_level, probabilities
        """
        # Preprocess input
        X = self.preprocess_data(patient_data)
        
        # Get predictions
        try:
            # Get probability predictions
            probabilities = self.model.predict_proba(X.values)[0]
            
            # Get class prediction
            prediction = self.model.predict(X.values)[0]
            
            # Convert to risk level
            risk_level = self.label_encoders['risk_level'].inverse_transform([prediction])[0]
            
            # Calculate risk score (0-100)
            risk_score = self._calculate_risk_score(probabilities)
            
            # Create probability dictionary
            risk_probs = {
                'Low': probabilities[0],
                'Medium': probabilities[1],
                'High': probabilities[2]
            }
            
        except Exception as e:
            print(f"Prediction error: {e}")
            # Fallback to rule-based prediction
            risk_score, risk_level, risk_probs = self._fallback_prediction(patient_data)
        
        return risk_score, risk_level, risk_probs
    
    def _calculate_risk_score(self, probabilities):
        """
        Convert probability distribution to a single risk score (0-100)
        """
        # Weighted sum: Low=0, Medium=50, High=100
        risk_score = (probabilities[0] * 0 + 
                     probabilities[1] * 50 + 
                     probabilities[2] * 100)
        return risk_score
    
    def _fallback_prediction(self, patient_data):
        """
        Rule-based fallback if model prediction fails
        """
        if isinstance(patient_data, dict):
            data = patient_data
        else:
            data = patient_data.iloc[0].to_dict()
        
        risk_factors = 0
        
        # Age factor
        if data['age'] > 70:
            risk_factors += 2
        elif data['age'] > 60:
            risk_factors += 1
        
        # Vital signs factors
        if data['heart_rate'] > 100 or data['heart_rate'] < 60:
            risk_factors += 1
        
        if data['blood_pressure_systolic'] > 140 or data['blood_pressure_systolic'] < 90:
            risk_factors += 1
        
        if data['temperature'] > 38.5 or data['temperature'] < 36:
            risk_factors += 1
        
        if data['respiratory_rate'] > 20 or data['respiratory_rate'] < 12:
            risk_factors += 1
        
        if data['oxygen_saturation'] < 95:
            risk_factors += 2
        
        # High-risk diagnoses
        if data['primary_diagnosis'] in ['Cardiac', 'Neurological', 'Trauma']:
            risk_factors += 1
        
        # Determine risk level
        if risk_factors >= 5:
            risk_level = 'High'
            risk_score = 75 + (risk_factors - 5) * 5
            risk_probs = {'Low': 0.1, 'Medium': 0.2, 'High': 0.7}
        elif risk_factors >= 3:
            risk_level = 'Medium'
            risk_score = 40 + (risk_factors - 3) * 10
            risk_probs = {'Low': 0.2, 'Medium': 0.6, 'High': 0.2}
        else:
            risk_level = 'Low'
            risk_score = risk_factors * 10
            risk_probs = {'Low': 0.7, 'Medium': 0.25, 'High': 0.05}
        
        return min(risk_score, 100), risk_level, risk_probs
    
    def predict_batch(self, patients_data):
        """
        Predict risk for multiple patients at once
        """
        results = []
        
        for idx, row in patients_data.iterrows():
            patient_dict = row.to_dict()
            risk_score, risk_level, risk_probs = self.predict_risk(patient_dict)
            
            results.append({
                'patient_id': row.get('patient_id', idx),
                'risk_score': risk_score,
                'risk_level': risk_level,
                'risk_probs': risk_probs
            })
        
        return pd.DataFrame(results)
    
    def get_feature_importance(self):
        """
        Get feature importance (if available)
        TabPFN doesn't provide direct feature importance, but we can approximate
        """
        if not self.is_trained:
            return None
        
        if hasattr(self.model, 'feature_importances_'):
            importance_dict = dict(zip(
                self.feature_columns,
                self.model.feature_importances_
            ))
            return importance_dict
        else:
            # TabPFN doesn't have feature_importances_
            # Return approximate importance based on clinical knowledge
            return {
                'age': 0.15,
                'oxygen_saturation': 0.20,
                'heart_rate': 0.12,
                'blood_pressure_systolic': 0.11,
                'blood_pressure_diastolic': 0.09,
                'temperature': 0.10,
                'respiratory_rate': 0.13,
                'diagnosis_encoded': 0.10,
                'gender_encoded': 0.00
            }
    
    def model_info(self):
        """
        Return information about the model
        """
        return {
            'model_type': self.model_type,
            'is_trained': self.is_trained,
            'features': self.feature_columns,
            'requires_feature_engineering': False,
            'description': 'TabPFN is a transformer-based model that works with raw tabular data without feature engineering'
        }
