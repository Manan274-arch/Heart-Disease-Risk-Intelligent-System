import streamlit as st

st.title("📊 Prediction Results")

# -----------------------------
# STATE INIT
# -----------------------------
if "go_to_insights" not in st.session_state:
    st.session_state["go_to_insights"] = False

# -----------------------------
# SAFETY CHECK
# -----------------------------
if "result" not in st.session_state:
    st.warning("Run assessment first.")
    st.stop()

result = st.session_state["result"]

score = result["risk_score"]
category = result["risk_category"]
factors = result.get("top_factors", [])

# -----------------------------
# RISK SCORE DISPLAY
# -----------------------------
st.markdown("### 🧮 Risk Score")

st.progress(score)
st.metric("Predicted Risk", f"{round(score*100,2)}%")

# -----------------------------
# CATEGORY DISPLAY
# -----------------------------
st.markdown("### 🚦 Risk Category")

if category == "Low":
    st.success("🟢 LOW RISK")
elif category == "Medium":
    st.warning("🟠 MEDIUM RISK")
else:
    st.error("🔴 HIGH RISK")

# -----------------------------
# INTERPRETATION
# -----------------------------
st.markdown("### 🧾 Clinical Interpretation")

if category == "Low":
    st.info("""
This assessment indicates a low estimated probability of heart disease based on the provided inputs.

This does not rule out disease completely, but the overall pattern of entered values appears less concerning in comparison to higher-risk profiles.
""")
elif category == "Medium":
    st.warning("""
This assessment indicates a moderate estimated probability of heart disease.

Some of the entered features may be associated with elevated cardiovascular risk. A closer review of symptoms, history, and medical evaluation may be appropriate.
""")
else:
    st.error("""
This assessment indicates a high estimated probability of heart disease.

The input profile contains multiple features that are strongly associated with elevated cardiovascular risk. Prompt professional medical review is advised.
""")

st.markdown("---")
st.caption("See the Insights page for a detailed explanation of the factors influencing this result.")

# -----------------------------
# WHY THIS RISK (PREVIEW)
# -----------------------------
st.markdown("### 🔍 Why this risk?")

drivers = [f for f in factors if f["effect"] == "increase"]
protectors = [f for f in factors if f["effect"] == "decrease"]

def clean(name):
    mapping = {
        "Oldpeak": "ST Depression",
        "Cholesterol": "Cholesterol Level",
        "MaxHR": "Maximum Heart Rate",
        "ExerciseAngina_Y": "Exercise-Induced Angina",
        "ExerciseAngina_N": "No Exercise Angina",
        "ST_Slope_Up": "ST Segment Upsloping",
        "ST_Slope_Flat": "ST Segment Flat",
        "ST_Slope_Down": "ST Segment Downsloping"
    }
    return mapping.get(name, name.replace("_", " "))

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Increasing Risk")
    if drivers:
        for d in drivers[:3]:
            st.markdown(f"- **{clean(d['feature'])}**")
    else:
        st.write("No major risk drivers detected.")

with col2:
    st.subheader("🟢 Reducing Risk")
    if protectors:
        for p in protectors[:3]:
            st.markdown(f"- **{clean(p['feature'])}**")
    else:
        st.write("No strong protective factors detected.")

# -----------------------------
# NAVIGATION BUTTON (NEW)
# -----------------------------
st.markdown("---")

st.success("Prediction ready. View detailed insights for deeper explanation.")

if st.button("🔍 View Detailed Insights"):
    st.session_state["go_to_insights"] = True
    st.switch_page("pages/3_Insights.py")

# -----------------------------
# FOOTER NOTE
# -----------------------------
st.markdown("---")

st.caption("""
⚠️ This tool is for **risk estimation only** and does not replace professional medical advice.
""")