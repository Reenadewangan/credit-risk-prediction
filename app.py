# 1 = Good (Lower Risk)
# 0 = Bad (Higher Risk)

import streamlit as st
import pandas as pd
import joblib

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Credit Risk Prediction",
    page_icon="🏦",
    layout="centered"
)

# --------------------------------------------------
# Load model and encoders
# --------------------------------------------------

model = joblib.load("best_dt_model.pkl")

encoders = {
    col: joblib.load(f"{col}_encoder.pkl")
    for col in [
        "Sex",
        "Housing",
        "Saving accounts",
        "Checking account"
    ]
}

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 20px;
    margin-bottom: 15px;
}

div.stButton > button {
    width: 100%;
    height: 50px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🏦 Credit Risk Prediction</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Assess the credit risk of an applicant using a machine learning model.</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# Personal Information
# --------------------------------------------------

st.markdown(
    '<div class="section-title">👤 Personal Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=30
    )

with col2:
    sex = st.selectbox(
        "Sex",
        ["male", "female"]
    )

col1, col2 = st.columns(2)

with col1:
    job = st.number_input(
        "Job Level",
        min_value=0,
        max_value=3,
        value=1,
        help="Job level ranges from 0 to 3."
    )

with col2:
    housing = st.selectbox(
        "Housing",
        ["own", "rent", "free"]
    )

# --------------------------------------------------
# Financial Information
# --------------------------------------------------

st.markdown(
    '<div class="section-title">💳 Financial Information</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    saving_accounts = st.selectbox(
        "Saving Accounts",
        ["little", "moderate", "rich", "quite rich"]
    )

with col2:
    checking_account = st.selectbox(
        "Checking Account",
        ["little", "moderate", "rich"]
    )

col1, col2 = st.columns(2)

with col1:
    credit_amount = st.number_input(
        "Credit Amount",
        min_value=0,
        value=100,
        step=100
    )

with col2:
    duration = st.number_input(
        "Duration (Months)",
        min_value=1,
        value=12
    )

st.divider()

# --------------------------------------------------
# Create input dataframe
# --------------------------------------------------

input_df = pd.DataFrame({
    "Age": [age],
    "Sex": [encoders["Sex"].transform([sex])[0]],
    "Job": [job],
    "Credit amount": [credit_amount],
    "Housing": [encoders["Housing"].transform([housing])[0]],
    "Saving accounts": [
        encoders["Saving accounts"].transform([saving_accounts])[0]
    ],
    "Checking account": [
        encoders["Checking account"].transform([checking_account])[0]
    ],
    "Duration": [duration]
})

# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button("🔍 Predict Credit Risk"):

    pred = model.predict(input_df)[0]

    st.subheader("Prediction Result")

    if pred == 1:
        st.success(
            "✅ Good Credit Risk — Lower Risk"
        )

    else:
        st.error(
            "⚠️ Bad Credit Risk — Higher Risk"
        )