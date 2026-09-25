

import pickle
import streamlit as st
import time

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="Disease Prediction System",
    page_icon="🩺",
    layout="centered"
)

# 2. Custom CSS to make the predict button and UI look beautiful
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff3333;
        border: 2px solid #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cache the model loading for better performance
# This prevents the app from reloading the pickle file every time a button is clicked
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("dp.pkl", "rb"))
    except FileNotFoundError:
        return None

dp = load_model()

# 4. Header Section
st.title("🩺 AI Disease Prediction System")
st.markdown(
    "Welcome to the AI health assistant. Please enter your vital signs below for a quick health assessment."
)
st.divider()

# 5. Input Section (Using Columns for a balanced layout)
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("🧑 Age (Years)", min_value=1, max_value=120, value=30, step=1)
    bt = st.number_input("🌡️ Body Temperature (°C)", min_value=30.0, max_value=45.0, value=37.0, step=0.1)

with col2:
    hrb = st.number_input("❤️ Heart Rate (BPM)", min_value=30, max_value=250, value=72, step=1)
    os = st.number_input("🩸 Oxygen Saturation (%)", min_value=50, max_value=100, value=98, step=1)

st.write("") # Adding a little empty space

# 6. Prediction Logic
if st.button("Analyze Vitals 🚀"):
    if dp is None:
        st.error("⚠️ Model file (`dp.pkl`) not found! Please ensure it is in the same folder as this script.")
    else:
        # Add a spinner to give the user visual feedback that it's working
        with st.spinner("Analyzing vitals through AI model..."):
            time.sleep(0.8) # Adding a slight pause for a smoother UI experience
            try:
                # Predicting the result
                res = dp.predict([[age, hrb, bt, os]])[0]
                
                # Displaying the result beautifully
                st.success("✅ Analysis Complete!")
                
                # Use a metric box or markdown header for the final result
                st.markdown(f"""
                <div style="background-color:#d4edda;padding:20px;border-radius:10px;">
                    <h3 style="color:#155724;text-align:center;">Expected Condition / Disease: <br> <b>{res}</b></h3>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred during prediction: {e}")