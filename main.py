import pickle
import streamlit as st
import time

# 1. Page Configuration (Wide layout for a dashboard feel)
st.set_page_config(
    page_title="AI Health Diagnostics",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Advanced Custom CSS for Modern UI
st.markdown("""
    <style>
    /* Sleek gradient button with hover animation */
    div.stButton > button {
        background: linear-gradient(135deg, #FF416C 0%, #FF4B2B 100%);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 12px 24px;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4);
        width: 100%;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(255, 65, 108, 0.6);
        color: white;
    }
    
    /* Animated Results Card */
    .result-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 30px rgba(17, 153, 142, 0.3);
        animation: slideUp 0.6s ease-out;
    }
    .result-card h2 {
        color: white;
        margin-bottom: 5px;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Cache the model for instant loading
@st.cache_resource
def load_model():
    try:
        return pickle.load(open("dp.pkl", "rb"))
    except FileNotFoundError:
        return None

dp = load_model()

# 4. Sidebar Design
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=100) # Medical icon
    st.title("Patient Portal")
    st.markdown("Please adjust the sliders to match the patient's current vital signs.")
    
    st.divider()
    st.markdown("### ⚠️ Medical Disclaimer")
    st.info(
        "This AI tool is for educational purposes only and does not replace "
        "professional medical advice, diagnosis, or treatment."
    )

# 5. Main Dashboard Header
st.title("🫀 AI Disease Prediction Dashboard")
st.markdown("##### Real-time vital sign analysis powered by Machine Learning")
st.write("---")

# 6. Interactive Sliders (Looks much better than text inputs)
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Demographics & Core Vitals")
    age = st.slider("Age (Years)", min_value=1, max_value=100, value=30, step=1)
    bt = st.slider("Body Temperature (°C)", min_value=35.0, max_value=42.0, value=37.0, step=0.1)

with col2:
    st.markdown("### 🫀 Cardiovascular & Respiratory")
    hrb = st.slider("Heart Rate (BPM)", min_value=40, max_value=200, value=75, step=1)
    os = st.slider("Oxygen Saturation (SpO2 %)", min_value=70, max_value=100, value=98, step=1)

st.write("---")

# 7. Action Button & Prediction Output
col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1]) # Center the button

with col_btn_2:
    if st.button("Generate Diagnostic Report ⚡"):
        if dp is None:
            st.error("⚠️ Model file (`dp.pkl`) not found in the directory!")
        else:
            with st.spinner("Analyzing patient vitals..."):
                time.sleep(1.2) # Artificial delay for visual effect
                try:
                    # Make Prediction
                    res = dp.predict([[age, hrb, bt, os]])[0]
                    
                    st.balloons() # Fun celebration animation
                    
                    # Beautiful HTML Results Card
                    st.markdown(f"""
                        <div class="result-card">
                            <p style="font-size: 20px; margin-bottom: 0px;">Predicted Condition</p>
                            <h2>{res}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Dashboard Metrics Summary
                    st.write("")
                    st.markdown("### 📊 Vitals Summary")
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric(label="Age", value=age)
                    m2.metric(label="Temperature", value=f"{bt} °C")
                    m3.metric(label="Heart Rate", value=f"{hrb} BPM")
                    m4.metric(label="SpO2", value=f"{os} %")
                    
                except Exception as e:
                    st.error(f"An error occurred: {e}")