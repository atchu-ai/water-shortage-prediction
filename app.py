import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Water Shortage Prediction",
    page_icon="💧",
    layout="wide"
)

# Title
st.title("💧 Water Shortage Prediction System")
st.write("AI-powered ward-wise water shortage prediction")

# Load CSV
file_path = "water_shortage_predictions.csv"

try:
    data = pd.read_csv(file_path)

    st.success("Prediction data loaded successfully!")

    # Clean column names
    data.columns = data.columns.str.strip()

    # Check required columns
    required_columns = [
        "Ward Name",
        "Consumption in ML",
        "Previous_Consumption"
    ]

    missing = [col for col in required_columns if col not in data.columns]

    if missing:
        st.error(f"Missing columns: {missing}")
        st.write("Available columns:")
        st.write(data.columns.tolist())
        st.stop()

    # Convert numeric columns
    data["Consumption in ML"] = pd.to_numeric(
        data["Consumption in ML"],
        errors="coerce"
    )

    data["Previous_Consumption"] = pd.to_numeric(
        data["Previous_Consumption"],
        errors="coerce"
    )

    # Remove invalid rows
    data = data.dropna(
        subset=["Ward Name", "Consumption in ML", "Previous_Consumption"]
    )

    # Ward selection
    wards = sorted(
        data["Ward Name"].dropna().unique().tolist()
    )

    selected_ward = st.selectbox(
        "📍 Select Ward",
        wards
    )

    # Get selected ward data
    ward_data = data[
        data["Ward Name"] == selected_ward
    ].copy()

    # Use latest record
    ward = ward_data.iloc[-1]

    # -----------------------------
    # Prediction calculation
    # -----------------------------

    previous_consumption = float(
        ward["Previous_Consumption"]
    )

    current_consumption = float(
        ward["Consumption in ML"]
    )

    # Predicted next demand
    if previous_consumption > 0:
        growth_rate = (
            current_consumption - previous_consumption
        ) / previous_consumption
    else:
        growth_rate = 0

    predicted_demand = (
        current_consumption * (1 + growth_rate)
    )

    # Available water estimation
    available_water = current_consumption * 0.90

    # Shortage
    shortage = max(
        predicted_demand - available_water,
        0
    )

    # Shortage percentage
    if predicted_demand > 0:
        shortage_percentage = (
            shortage / predicted_demand
        ) * 100
    else:
        shortage_percentage = 0

    # Risk level
    if shortage_percentage <= 10:
        risk_level = "Low"
    elif shortage_percentage <= 20:
        risk_level = "Moderate"
    elif shortage_percentage <= 30:
        risk_level = "High"
    else:
        risk_level = "Critical"

    # -----------------------------
    # Display
    # -----------------------------

    st.subheader(
        f"📊 Prediction for {selected_ward}"
    )

    # First row
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Predicted Demand",
            f"{predicted_demand:.2f} ML"
        )

    with col2:
        st.metric(
            "Available Water",
            f"{available_water:.2f} ML"
        )

    with col3:
        st.metric(
            "Shortage",
            f"{shortage:.2f} ML"
        )

    st.divider()

    # Second row
    col4, col5 = st.columns(2)

    with col4:
        st.metric(
            "Shortage Percentage",
            f"{shortage_percentage:.2f}%"
        )

    with col5:
        st.metric(
            "Risk Level",
            risk_level
        )

    # Warning
    if risk_level == "Critical":
        st.error(
            "🚨 Critical water shortage risk!"
        )
    elif risk_level == "High":
        st.warning(
            "⚠️ High water shortage risk!"
        )
    elif risk_level == "Moderate":
        st.warning(
            "🟡 Moderate water shortage risk."
        )
    else:
        st.success(
            "🟢 Water availability is relatively stable."
        )

    # AI recommendation
    st.subheader("🤖 Smart Distribution Recommendation")

    if risk_level == "Critical":
        st.write(
            "Prioritize drinking water supply and "
            "reduce non-essential water usage."
        )
    elif risk_level == "High":
        st.write(
            "Increase monitoring and prioritize "
            "high-demand areas."
        )
    elif risk_level == "Moderate":
        st.write(
            "Monitor consumption and optimize "
            "ward-wise water distribution."
        )
    else:
        st.write(
            "Maintain normal distribution and "
            "continue monitoring water consumption."
        )

except FileNotFoundError:

    st.error(
        "water_shortage_predictions.csv not found."
    )

    st.info(
        "Please keep the CSV file in the same folder as app.py."
    )

except Exception as e:

    st.error(
        f"Error: {e}"
    )