import streamlit as st

st.title("🧠 Risk Insights")

# -----------------------------
# NAVIGATION GUARD
# -----------------------------
if not st.session_state.get("go_to_insights", False):
    st.warning("Please generate a prediction from the Results page first.")
    st.stop()

# -----------------------------
# SAFETY CHECK
# -----------------------------
if "result" not in st.session_state or "patient_data" not in st.session_state:
    st.warning("Run assessment first.")
    st.stop()

result = st.session_state["result"]
patient = st.session_state["patient_data"]
factors = result.get("top_factors", [])

drivers = [f for f in factors if f["effect"] == "increase"]
protectors = [f for f in factors if f["effect"] == "decrease"]

# -----------------------------
# ✅ % CONTRIBUTION (ADDED)
# -----------------------------
total_impact = sum(abs(f["impact"]) for f in factors) or 1
for f in factors:
    f["percent"] = abs(f["impact"]) / total_impact * 100

# -----------------------------
# CLEAN FUNCTION (UNCHANGED)
# -----------------------------
def clean(name):
    mapping = {
        "Oldpeak": "ST Depression (Oldpeak)",
        "Cholesterol": "Cholesterol Level",
        "MaxHR": "Maximum Heart Rate",
        "ExerciseAngina_Y": "Exercise-Induced Angina",
        "ExerciseAngina_N": "No Exercise-Induced Angina",
        "ST_Slope_Up": "ST Segment Upsloping",
        "ST_Slope_Flat": "ST Segment Flat",
        "ST_Slope_Down": "ST Segment Downsloping",
        "ChestPainType_ASY": "Asymptomatic Chest Pain Pattern",
        "ChestPainType_ATA": "Atypical Angina Pattern",
        "ChestPainType_NAP": "Non-Anginal Pain Pattern",
        "ChestPainType_TA": "Typical Angina Pattern",
        "FastingBS": "Fasting Blood Sugar",
        "RestingBP": "Resting Blood Pressure",
        "RestingECG_LVH": "ECG: Left Ventricular Hypertrophy",
        "RestingECG_ST": "ECG: ST-T Abnormality",
        "RestingECG_Normal": "ECG: Normal Pattern",
        "Age": "Age",
        "Sex_M": "Male Sex",
        "Sex_F": "Female Sex"
    }
    return mapping.get(name, name.replace("_", " "))

# -----------------------------
# ✅ NATURAL LANGUAGE SUMMARY (ADDED)
# -----------------------------
def generate_summary(drivers, protectors):

    def top_features(features, n=2):
        return [clean(f["feature"]) for f in sorted(features, key=lambda x: abs(x["impact"]), reverse=True)[:n]]

    top_drivers = top_features(drivers)
    top_protectors = top_features(protectors)

    summary = ""

    if top_drivers:
        if len(top_drivers) == 1:
            summary += f"Your predicted risk is mainly driven by **{top_drivers[0]}**"
        else:
            summary += f"Your predicted risk is mainly driven by **{top_drivers[0]}** and **{top_drivers[1]}**"

    if top_protectors:
        if summary:
            summary += ", while "
        else:
            summary += "Your risk is influenced by "

        if len(top_protectors) == 1:
            summary += f"factors such as **{top_protectors[0]}** are helping reduce your risk"
        else:
            summary += f"factors such as **{top_protectors[0]}** and **{top_protectors[1]}** are helping reduce your risk"

    summary += "."
    return summary

# -----------------------------
# PAGE EXPLANATION (UNCHANGED)
# -----------------------------
st.markdown("### What this page shows")
st.info("""
This page explains why the model produced your risk score.

The model identifies:
- **Risk drivers**: factors that pushed your score upward
- **Protective factors**: factors that pushed your score downward

These do not prove causation by themselves. They explain how your entered profile influenced the model's prediction.
""")

# -----------------------------
# SHAP DISPLAY (ONLY % ADDED)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔴 Top Factors Increasing Your Risk")
    if drivers:
        for d in drivers:
            val = round(d["impact"], 3)
            pct = round(d["percent"], 1)
            st.markdown(f"**{clean(d['feature'])}**")
            st.write(f"{val:+} → contributes {pct}% to increased risk")
    else:
        st.write("No major risk-increasing features were highlighted.")

with col2:
    st.subheader("🟢 Top Factors Reducing Your Risk")
    if protectors:
        for p in protectors:
            val = round(p["impact"], 3)
            pct = round(p["percent"], 1)
            st.markdown(f"**{clean(p['feature'])}**")
            st.write(f"{val:+} → contributes {pct}% to risk reduction")
    else:
        st.write("No strong risk-reducing features were highlighted.")

# -----------------------------
# SHAP EXPLANATION (UNCHANGED)
# -----------------------------
st.markdown("### 📊 Understanding These Risk Factors")

st.markdown("""
Each factor above shows how it influenced your predicted risk score.

- Positive values increase risk  
- Negative values reduce risk  
- Percentages show relative importance among all factors  
""")

# -----------------------------
# ✅ KEY TAKEAWAY (ADDED)
# -----------------------------
st.markdown("---")
st.markdown("### 🧠 Key Takeaway")

summary = generate_summary(drivers, protectors)
st.success(summary)

# -----------------------------
# CLINICAL SECTION (100% YOURS)
# -----------------------------
st.markdown("---")
st.markdown("### Clinical interpretation of your entered values")

age = patient["Age"]
bp = patient["RestingBP"]
chol = patient["Cholesterol"]
fbs = patient["FastingBS"]
hr = patient["MaxHR"]
angina = patient["ExerciseAngina"]
oldpeak = patient["Oldpeak"]
cp = patient["ChestPainType"]
ecg = patient["RestingECG"]
slope = patient["ST_Slope"]

st.markdown(f"**Age:** {age} years")
st.write("Increasing age is generally associated with greater cardiovascular risk.")

st.markdown(f"**Resting Blood Pressure:** {bp} mm Hg")
if bp >= 140:
    st.write("This is elevated and may contribute to increased cardiovascular strain.")
elif bp >= 120:
    st.write("This is mildly elevated and should be interpreted along with other risk features.")
else:
    st.write("This is not markedly elevated in isolation.")

st.markdown(f"**Cholesterol:** {chol} mg/dL")
if chol >= 240:
    st.write("This is high and can be associated with increased cardiovascular risk.")
elif chol >= 200:
    st.write("This is borderline-high and may matter alongside other findings.")
else:
    st.write("This is not markedly elevated by itself.")

st.markdown(f"**Fasting Blood Sugar Indicator:** {fbs}")
if fbs == 1:
    st.write("This suggests elevated fasting blood sugar, which can add metabolic risk.")
else:
    st.write("No elevated fasting blood sugar indicator was entered.")

st.markdown(f"**Maximum Heart Rate:** {hr}")
st.write("Heart rate response may influence risk interpretation depending on the broader clinical picture.")

st.markdown(f"**Exercise-Induced Angina:** {angina}")
if angina == "Y":
    st.write("Exercise-induced angina is an important symptom feature and can increase concern.")
else:
    st.write("Absence of exercise-induced angina is generally less concerning than its presence.")

st.markdown(f"**Oldpeak / ST Depression:** {oldpeak}")
if oldpeak >= 2:
    st.write("This is notably elevated and may indicate a more concerning cardiac stress response.")
elif oldpeak > 0:
    st.write("This shows some ST depression and should be interpreted clinically.")
else:
    st.write("No ST depression was indicated.")

st.markdown(f"**Chest Pain Type:** {cp}")
cp_map = {
    "ASY": "Asymptomatic presentations can still be clinically important and should not be dismissed.",
    "ATA": "Atypical angina may still carry diagnostic relevance depending on context.",
    "NAP": "Non-anginal pain is often less suggestive of coronary disease than classic angina patterns.",
    "TA": "Typical angina is often a clinically important symptom pattern."
}
st.write(cp_map.get(cp, "Chest pain pattern contributes to the overall profile."))

st.markdown(f"**Resting ECG:** {ecg}")
ecg_map = {
    "Normal": "A normal ECG pattern is generally less concerning in isolation.",
    "ST": "ST-T abnormalities may carry diagnostic importance depending on the broader clinical context.",
    "LVH": "Left ventricular hypertrophy can be associated with chronic cardiovascular strain."
}
st.write(ecg_map.get(ecg, "ECG pattern contributes to the overall risk profile."))

st.markdown(f"**ST Slope:** {slope}")
slope_map = {
    "Up": "Upsloping ST patterns are often less concerning than flat or downsloping patterns.",
    "Flat": "Flat ST slope patterns can be more concerning in cardiac evaluation.",
    "Down": "Downsloping ST patterns are often considered more suspicious clinically."
}
st.write(slope_map.get(slope, "ST slope contributes to the overall profile."))

st.markdown("---")
st.caption("These explanations support understanding of the model output and do not replace clinical diagnosis.")