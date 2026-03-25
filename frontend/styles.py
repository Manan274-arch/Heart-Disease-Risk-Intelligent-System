import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    body {
        background-color: #f7fbfc;
    }

    .stButton>button {
        background-color: #0ea5a5;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
    }

    .risk-low {
        color: green;
        font-weight: bold;
    }

    .risk-medium {
        color: orange;
        font-weight: bold;
    }

    .risk-high {
        color: red;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)