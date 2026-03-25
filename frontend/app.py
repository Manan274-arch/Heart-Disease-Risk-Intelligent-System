import streamlit as st
from styles import apply_styles

st.set_page_config(
    page_title="Heart Risk AI",
    layout="wide"
)

apply_styles()

# -----------------------------
# HERO SECTION
# -----------------------------

st.markdown("""
# 🫀 Heart Disease Risk Intelligence System
""")

st.markdown("""
### AI-powered clinical risk assessment platform

This system helps estimate the probability of heart disease using advanced machine learning models,
while also providing interpretable insights into contributing risk factors.
""")

st.divider()

# -----------------------------
# FEATURE CARDS
# -----------------------------

col1,col2,col3=st.columns(3)

with col1:
    st.markdown("""
    ### 🧠 Intelligent Prediction
    - Ensemble ML models  
    - Calibrated probabilities  
    - Clinically meaningful outputs  
    """)

with col2:
    st.markdown("""
    ### 📊 Risk Stratification
    - Low / Medium / High categorization  
    - Visual risk indicators  
    - Decision-support ready  
    """)

with col3:
    st.markdown("""
    ### 🔍 Explainability
    - SHAP-based insights  
    - Risk drivers vs protectors  
    - Transparent predictions  
    """)

st.divider()

# -----------------------------
# HOW TO USE
# -----------------------------

st.markdown("""
## 🚀 How to Use

1. Go to **Assessment** page  
2. Enter patient clinical data  
3. View prediction in **Results**  
4. Understand factors in **Insights**

---
""")

# -----------------------------
# TRUST SECTION
# -----------------------------

st.info("""
🔒 Your data is used only for real-time prediction and is not stored without consent.
""")