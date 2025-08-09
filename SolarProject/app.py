import streamlit as st
import pandas as pd
import joblib
import numpy as np

# --- Load Trained Model ---
try:
    model = joblib.load('solar_model.joblib')
except FileNotFoundError:
    st.error("Model file ('solar_model.joblib') not found. Please run 'python3 train_model.py' first.")
    st.stop()

# --- Web App UI ---
st.set_page_config(page_title="Solar Power Predictor", page_icon="☀️", layout="wide")
st.title("☀️ Smart Solar Power Management System")
st.write("---")


# --- Sidebar for All Inputs ---
st.sidebar.header("System & Weather Controls")

# Section for user to define their solar setup
st.sidebar.subheader("1. My Solar Setup")
panel_wattage = st.sidebar.number_input("Watts per Panel (e.g., 330, 550)", min_value=100, value=550)
num_panels = st.sidebar.number_input("Number of Panels", min_value=1, value=4)
total_system_capacity_watts = panel_wattage * num_panels
st.sidebar.metric(label="Total System Capacity", value=f"{(total_system_capacity_watts / 1000):.2f} kW")
st.sidebar.write("---")

# Section for weather conditions
st.sidebar.subheader("2. Live Weather Conditions")
temp = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
irradiance = st.sidebar.slider("Sunlight Intensity (0=Shade, 1=Full Sun)", 0.0, 1.0, 0.5)


# --- Create a two-column layout for the main page ---
col1, col2 = st.columns((1, 1.5))

with col1:
    # --- Live Prediction ---
    st.header("⚡ Live Power Output")
    
    base_prediction = model.predict(pd.DataFrame([[temp, irradiance]], columns=['temperature', 'irradiance']))[0]
    
    MODEL_PEAK_OUTPUT = 950 
    scaling_factor = total_system_capacity_watts / MODEL_PEAK_OUTPUT if MODEL_PEAK_OUTPUT > 0 else 0
    scaled_prediction = base_prediction * scaling_factor
    
    st.metric(label="Predicted Power (Watts)", value=f"{scaled_prediction:.2f} W")
    if total_system_capacity_watts > 0:
        st.progress(scaled_prediction / total_system_capacity_watts)
    st.write("---")
    
    # --- Appliance Load Calculation ---
    st.header("🔌 Load Calculator")
    
    # --- UPDATED: Changed checkboxes to a dropdown (multiselect) ---
    appliances = {
        "Fan": 75, "LED Light": 20, "Television": 100, "Laptop Charger": 65, 
        "Inverter Fridge": 150, "Water Pump": 200, "Air Conditioner": 1500, 
        "Heater": 2000, "Washing Machine": 500, "Microwave": 800, 
        "Electric Kettle": 1500, "Electric Stove": 2000, "Desktop Computer": 300, 
        "Gaming Console": 200, "Electric Iron": 1200, "Electric Geyser": 3000, 
        "Electric Water Heater": 3000, "Electric Oven": 1500,
    }
    
    selected_appliances = st.multiselect(
        "Select appliances to run:",
        options=list(appliances.keys())
    )
    
    # Calculate load from selected dropdown items
    total_load = sum(appliances[name] for name in selected_appliances)
    
    # Add manual load
    manual_load = st.number_input("Add Custom Load (Watts)", min_value=0, step=10)
    total_load += manual_load

    # --- NEW: Live Load Bar and Metrics ---
    st.subheader("Current Load Consumption")
    load_col1, load_col2 = st.columns(2)
    load_col1.metric(label="Total Load (Watts)", value=f"{total_load} W")
    load_col2.metric(label="Total Load (Kilowatts)", value=f"{(total_load / 1000):.3f} kW")
    
    # Live progress bar for load vs. generation
    if scaled_prediction > 0:
        load_percentage = min(total_load / scaled_prediction, 1.0) # Cap at 100%
        st.progress(load_percentage)
    else:
        st.progress(0)

    # Load check logic
    if total_load > 0:
        if scaled_prediction >= total_load:
            st.success("System Stable: Your current power generation is sufficient for the selected load.")
        else:
            deficit = total_load - scaled_prediction
            st.error(f"Power Alert: Generation is insufficient. You need an additional {deficit:.2f} Watts.")

with col2:
    # --- Daily Performance Forecast ---
    st.header("📊 Daily Performance Forecast")
    
    hours = np.arange(6, 19, 1)
    daily_irradiance = np.sin((hours - 6) * np.pi / 12)
    daily_irradiance[daily_irradiance < 0] = 0
    
    graph_data = pd.DataFrame({'temperature': [temp] * len(hours), 'irradiance': daily_irradiance})
    daily_base_prediction = model.predict(graph_data)
    
    daily_scaled_prediction = daily_base_prediction * scaling_factor
    
    chart_df = pd.DataFrame({'Hour': hours, 'Predicted Power (W)': daily_scaled_prediction}).set_index('Hour')
    st.line_chart(chart_df)
    st.caption("This graph shows the estimated power generation throughout the day for your specific system setup.")
    st.write("---")

    # --- Savings Calculator ---
    st.header("💰 Daily Savings Calculator")
    
    total_daily_energy_wh = np.sum(daily_scaled_prediction)
    total_daily_energy_kwh = total_daily_energy_wh / 1000
    
    unit_price = st.number_input("Enter Your Electricity Unit Price (e.g., PKR 35)", min_value=0.0, value=35.0, step=1.0)
    
    total_savings = total_daily_energy_kwh * unit_price
    
    st.metric(label="Estimated Total Daily Savings", value=f"PKR {total_savings:.2f}")
    st.caption(f"Based on a total generation of {total_daily_energy_kwh:.2f} kWh for the day.")