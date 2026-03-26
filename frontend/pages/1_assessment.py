import streamlit as st
from api import get_prediction

# -----------------------------
# SESSION STATE INIT
# -----------------------------
if "has_run" not in st.session_state:
    st.session_state["has_run"] = False

if "result" not in st.session_state:
    st.session_state["result"] = None

if "patient_data" not in st.session_state:
    st.session_state["patient_data"] = None

if "just_ran" not in st.session_state:
    st.session_state["just_ran"] = False


# -----------------------------
# UI
# -----------------------------
st.title("📝 Patient Assessment")

with st.form("patient_form"):

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 20, 100)

        sex = st.selectbox("Sex", [
            "M (Male)",
            "F (Female)"
        ])

        cp = st.selectbox("Chest Pain Type", [
            "ATA (Atypical Angina)",
            "NAP (Non-Anginal Pain)",
            "ASY (Asymptomatic)",
            "TA (Typical Angina)"
        ])

        bp = st.number_input("Resting Blood Pressure (mm Hg)", 80, 200)

        chol = st.number_input("Cholesterol (mg/dL)", 100, 600)

    with col2:
        fbs = st.selectbox("Fasting Blood Sugar (>120 mg/dL)", [
            0,
            1
        ])

        ecg = st.selectbox("Resting ECG", [
            "Normal (Normal ECG)",
            "ST (ST-T Wave Abnormality)",
            "LVH (Left Ventricular Hypertrophy)"
        ])

        hr = st.number_input("Max Heart Rate", 60, 220)

        angina = st.selectbox("Exercise-Induced Angina", [
            "Y (Yes)",
            "N (No)"
        ])

        oldpeak = st.number_input("Oldpeak (ST Depression)", 0.0, 6.0)

        slope = st.selectbox("ST Slope", [
            "Up (Upsloping)",
            "Flat (Flat)",
            "Down (Downsloping)"
        ])

    submitted = st.form_submit_button("Predict Risk")


# -----------------------------
# PREDICTION LOGIC
# -----------------------------
if submitted:

    data = {
        "Age": age,
        "Sex": sex[0],
        "ChestPainType": cp.split()[0],
        "RestingBP": bp,
        "Cholesterol": chol,
        "FastingBS": fbs,
        "RestingECG": ecg.split()[0],
        "MaxHR": hr,
        "ExerciseAngina": angina[0],
        "Oldpeak": oldpeak,
        "ST_Slope": slope.split()[0]
    }

    with st.spinner("Analyzing patient risk..."):
        result = get_prediction(data)

    if "error" in result:
        st.error("⚠️ Backend not running.")
    else:
        st.session_state["result"] = result
        st.session_state["patient_data"] = data
        st.session_state["has_run"] = True
        st.session_state["just_ran"] = True


# -----------------------------
# SUCCESS MESSAGE + NAVIGATION
# -----------------------------
if st.session_state.get("just_ran"):

    st.success("✅ Prediction complete. Go to Results page →")

    if st.button("👉 View Results", use_container_width=True):
        st.session_state["just_ran"] = False
        st.switch_page("pages/2_results.py")