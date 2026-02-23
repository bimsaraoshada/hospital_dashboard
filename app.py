import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from risk_predictor import RiskPredictor
from data_generator import generate_patient_data, generate_bed_data

# Page configuration
st.set_page_config(
    page_title="Hospital Management Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .high-risk {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
    }
    .medium-risk {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
    }
    .low-risk {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'risk_predictor' not in st.session_state:
    st.session_state.risk_predictor = RiskPredictor()
    st.session_state.patients_df = generate_patient_data(100)
    st.session_state.beds_df = generate_bed_data(50)

# Sidebar
with st.sidebar:
    st.title("🏥 Hospital Dashboard")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["Overview", "Risk Predictions", "Bed Management", "Patient Analytics"]
    )
    
    st.markdown("---")
    st.subheader("Quick Stats")
    total_beds = len(st.session_state.beds_df)
    occupied_beds = len(st.session_state.beds_df[st.session_state.beds_df['status'] == 'Occupied'])
    st.metric("Total Beds", total_beds)
    st.metric("Occupied", occupied_beds)
    st.metric("Available", total_beds - occupied_beds)
    st.metric("Total Patients", len(st.session_state.patients_df))

# Main content area
if page == "Overview":
    st.title("Hospital Overview Dashboard")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        high_risk_count = len(st.session_state.patients_df[st.session_state.patients_df['risk_level'] == 'High'])
        st.metric("High Risk Patients", high_risk_count, delta=None)
    
    with col2:
        avg_age = st.session_state.patients_df['age'].mean()
        st.metric("Average Patient Age", f"{avg_age:.1f}", delta=None)
    
    with col3:
        occupancy_rate = (occupied_beds / total_beds) * 100
        st.metric("Bed Occupancy Rate", f"{occupancy_rate:.1f}%", delta=None)
    
    with col4:
        icu_occupied = len(st.session_state.beds_df[
            (st.session_state.beds_df['type'] == 'ICU') & 
            (st.session_state.beds_df['status'] == 'Occupied')
        ])
        st.metric("ICU Beds Occupied", icu_occupied, delta=None)
    
    st.markdown("---")
    
    # Charts Row
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        risk_counts = st.session_state.patients_df['risk_level'].value_counts()
        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            color=risk_counts.index,
            color_discrete_map={'Low': '#4caf50', 'Medium': '#ff9800', 'High': '#f44336'},
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Bed Availability by Type")
        bed_summary = st.session_state.beds_df.groupby(['type', 'status']).size().reset_index(name='count')
        fig = px.bar(
            bed_summary,
            x='type',
            y='count',
            color='status',
            barmode='group',
            color_discrete_map={'Available': '#4caf50', 'Occupied': '#f44336', 'Maintenance': '#ff9800'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent Admissions
    st.markdown("---")
    st.subheader("Recent Patient Activity")
    recent_patients = st.session_state.patients_df.sort_values('admission_date', ascending=False).head(10)
    st.dataframe(
        recent_patients[['patient_id', 'age', 'gender', 'admission_date', 'risk_level', 'primary_diagnosis']],
        use_container_width=True,
        hide_index=True
    )

elif page == "Risk Predictions":
    st.title("Patient Risk Predictions")
    
    tab1, tab2 = st.tabs(["Existing Patients", "New Prediction"])
    
    with tab1:
        st.subheader("Risk Assessment for Current Patients")
        
        # Filter options
        col1, col2 = st.columns([1, 3])
        with col1:
            risk_filter = st.multiselect(
                "Filter by Risk Level",
                options=['Low', 'Medium', 'High'],
                default=['Medium', 'High']
            )
        
        filtered_patients = st.session_state.patients_df[
            st.session_state.patients_df['risk_level'].isin(risk_filter)
        ].sort_values('risk_score', ascending=False)
        
        st.markdown(f"**Showing {len(filtered_patients)} patients**")
        
        # Display patients with color-coded risk
        for idx, patient in filtered_patients.iterrows():
            risk_class = f"{patient['risk_level'].lower()}-risk"
            
            with st.container():
                st.markdown(f'<div class="prediction-box {risk_class}">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    st.write(f"**Patient ID:** {patient['patient_id']}")
                    st.write(f"**Age:** {patient['age']} | **Gender:** {patient['gender']}")
                
                with col2:
                    st.write(f"**Diagnosis:** {patient['primary_diagnosis']}")
                    st.write(f"**Admitted:** {patient['admission_date'].strftime('%Y-%m-%d')}")
                
                with col3:
                    st.write(f"**Risk Score:** {patient['risk_score']:.2f}")
                    st.write(f"**Risk Level:** {patient['risk_level']}")
                
                with col4:
                    if st.button("Details", key=f"detail_{patient['patient_id']}"):
                        st.session_state[f"show_{patient['patient_id']}"] = True
                
                if st.session_state.get(f"show_{patient['patient_id']}", False):
                    st.write("**Clinical Parameters:**")
                    st.write(f"- Heart Rate: {patient['heart_rate']} bpm")
                    st.write(f"- Blood Pressure: {patient['blood_pressure_systolic']}/{patient['blood_pressure_diastolic']} mmHg")
                    st.write(f"- Temperature: {patient['temperature']:.1f}°C")
                    st.write(f"- Respiratory Rate: {patient['respiratory_rate']} /min")
                    st.write(f"- Oxygen Saturation: {patient['oxygen_saturation']}%")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.subheader("Predict Risk for New Patient")
        st.write("Enter patient data to get risk prediction using TabPFN model")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_age = st.number_input("Age", min_value=0, max_value=120, value=50)
            new_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            new_heart_rate = st.number_input("Heart Rate (bpm)", min_value=30, max_value=200, value=75)
            new_bp_sys = st.number_input("Blood Pressure Systolic", min_value=60, max_value=250, value=120)
            new_bp_dias = st.number_input("Blood Pressure Diastolic", min_value=40, max_value=150, value=80)
        
        with col2:
            new_temp = st.number_input("Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0, step=0.1)
            new_resp = st.number_input("Respiratory Rate (/min)", min_value=8, max_value=40, value=16)
            new_o2 = st.number_input("Oxygen Saturation (%)", min_value=70, max_value=100, value=98)
            new_diagnosis = st.selectbox("Primary Diagnosis", 
                ["Cardiac", "Respiratory", "Neurological", "Trauma", "Infection", "Other"])
        
        if st.button("Predict Risk", type="primary"):
            with st.spinner("Analyzing patient data with TabPFN..."):
                # Create patient data
                new_patient_data = {
                    'age': new_age,
                    'gender': new_gender,
                    'heart_rate': new_heart_rate,
                    'blood_pressure_systolic': new_bp_sys,
                    'blood_pressure_diastolic': new_bp_dias,
                    'temperature': new_temp,
                    'respiratory_rate': new_resp,
                    'oxygen_saturation': new_o2,
                    'primary_diagnosis': new_diagnosis
                }
                
                # Get prediction
                risk_score, risk_level, risk_probs = st.session_state.risk_predictor.predict_risk(new_patient_data)
                
                st.success("Prediction Complete!")
                
                # Display results
                risk_class = f"{risk_level.lower()}-risk"
                st.markdown(f'<div class="prediction-box {risk_class}">', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Risk Score", f"{risk_score:.2f}")
                    st.metric("Risk Level", risk_level)
                
                with col2:
                    st.write("**Risk Probabilities:**")
                    st.write(f"Low Risk: {risk_probs['Low']*100:.1f}%")
                    st.write(f"Medium Risk: {risk_probs['Medium']*100:.1f}%")
                    st.write(f"High Risk: {risk_probs['High']*100:.1f}%")
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Visualization of risk factors
                st.subheader("Clinical Parameter Analysis")
                fig = go.Figure()
                
                parameters = ['Heart Rate', 'BP Systolic', 'Temperature', 'Respiratory Rate', 'O2 Saturation']
                values = [new_heart_rate/200*100, new_bp_sys/250*100, (new_temp-35)/7*100, 
                         new_resp/40*100, new_o2]
                
                fig.add_trace(go.Bar(
                    x=parameters,
                    y=values,
                    marker_color=['#2196F3', '#2196F3', '#2196F3', '#2196F3', '#2196F3']
                ))
                fig.update_layout(
                    yaxis_title="Normalized Value (%)",
                    showlegend=False,
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

elif page == "Bed Management":
    st.title("Bed Availability & Management")
    
    # Bed Status Overview
    col1, col2, col3 = st.columns(3)
    
    bed_types = ['General', 'ICU', 'Emergency']
    for col, bed_type in zip([col1, col2, col3], bed_types):
        with col:
            type_beds = st.session_state.beds_df[st.session_state.beds_df['type'] == bed_type]
            available = len(type_beds[type_beds['status'] == 'Available'])
            total = len(type_beds)
            
            st.subheader(f"{bed_type} Ward")
            st.metric("Available Beds", f"{available}/{total}")
            
            # Progress bar
            occupancy = ((total - available) / total) * 100 if total > 0 else 0
            st.progress(occupancy / 100)
            st.caption(f"{occupancy:.0f}% Occupied")
    
    st.markdown("---")
    
    # Bed Details Table
    st.subheader("Detailed Bed Status")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=['Available', 'Occupied', 'Maintenance'],
            default=['Available', 'Occupied']
        )
    
    with col2:
        type_filter = st.multiselect(
            "Filter by Type",
            options=['General', 'ICU', 'Emergency'],
            default=['General', 'ICU', 'Emergency']
        )
    
    filtered_beds = st.session_state.beds_df[
        (st.session_state.beds_df['status'].isin(status_filter)) &
        (st.session_state.beds_df['type'].isin(type_filter))
    ]
    
    # Color code the dataframe
    def color_status(val):
        if val == 'Available':
            return 'background-color: #c8e6c9'
        elif val == 'Occupied':
            return 'background-color: #ffcdd2'
        else:
            return 'background-color: #ffe0b2'
    
    styled_df = filtered_beds.style.applymap(color_status, subset=['status'])
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Bed Occupancy Timeline
    st.markdown("---")
    st.subheader("Bed Occupancy Trend (Simulated)")
    
    # Generate timeline data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    occupancy_data = []
    
    for date in dates:
        for bed_type in bed_types:
            total = len(st.session_state.beds_df[st.session_state.beds_df['type'] == bed_type])
            occupied = np.random.randint(int(total * 0.4), int(total * 0.9))
            occupancy_data.append({
                'date': date,
                'type': bed_type,
                'occupied': occupied,
                'total': total,
                'occupancy_rate': (occupied / total) * 100
            })
    
    occupancy_df = pd.DataFrame(occupancy_data)
    
    fig = px.line(
        occupancy_df,
        x='date',
        y='occupancy_rate',
        color='type',
        title='30-Day Bed Occupancy Rate Trend',
        labels={'occupancy_rate': 'Occupancy Rate (%)', 'date': 'Date'}
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

elif page == "Patient Analytics":
    st.title("Patient Analytics & Insights")
    
    # Age Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Age Distribution")
        fig = px.histogram(
            st.session_state.patients_df,
            x='age',
            nbins=20,
            color='risk_level',
            color_discrete_map={'Low': '#4caf50', 'Medium': '#ff9800', 'High': '#f44336'},
            labels={'age': 'Age', 'count': 'Number of Patients'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Diagnosis Distribution")
        diagnosis_counts = st.session_state.patients_df['primary_diagnosis'].value_counts()
        fig = px.bar(
            x=diagnosis_counts.index,
            y=diagnosis_counts.values,
            labels={'x': 'Diagnosis', 'y': 'Number of Patients'},
            color=diagnosis_counts.values,
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Vital Signs Analysis
    st.markdown("---")
    st.subheader("Vital Signs Distribution by Risk Level")
    
    vital_metric = st.selectbox(
        "Select Vital Sign",
        ['heart_rate', 'blood_pressure_systolic', 'temperature', 'respiratory_rate', 'oxygen_saturation']
    )
    
    fig = px.box(
        st.session_state.patients_df,
        x='risk_level',
        y=vital_metric,
        color='risk_level',
        color_discrete_map={'Low': '#4caf50', 'Medium': '#ff9800', 'High': '#f44336'},
        labels={vital_metric: vital_metric.replace('_', ' ').title(), 'risk_level': 'Risk Level'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation Analysis
    st.markdown("---")
    st.subheader("Vital Signs Correlation Matrix")
    
    vital_cols = ['age', 'heart_rate', 'blood_pressure_systolic', 'blood_pressure_diastolic', 
                  'temperature', 'respiratory_rate', 'oxygen_saturation', 'risk_score']
    
    corr_matrix = st.session_state.patients_df[vital_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect='auto',
        color_continuous_scale='RdBu_r',
        labels=dict(color="Correlation")
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Hospital Management Dashboard | Powered by TabPFN | Real-time Monitoring & Predictions</p>
    </div>
    """,
    unsafe_allow_html=True
)
