# app.py


import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Kosi Basin Forecast", layout="wide")

st.title("🌊 Kosi Basin Transformer Forecast System")

uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx"]
)

if uploaded_file is not None:

    # ============================================================
    # READ FILE
    # ============================================================
    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Uploaded Data")
    st.dataframe(df.head())

    # ============================================================
    # SAVE INPUT FILE
    # ============================================================
    df.to_excel("input.xlsx", index=False)

    # ============================================================
    # RUN PREDICTION SCRIPT
    # ============================================================
    if st.button("🚀 Run Prediction"):

        with st.spinner("Running Transformer model... Please wait..."):

            os.system("python predict.py")

        # ============================================================
        # LOAD OUTPUT
        # ============================================================
        pred = pd.read_csv("output.csv")

        st.success("✅ Prediction Completed!")

        st.subheader("📈 Forecast Results")

        st.dataframe(pred)

        # ============================================================
        # DOWNLOAD BUTTON
        # ============================================================
        csv = pred.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="📥 Download Forecast CSV",
            data=csv,
            file_name="Kosi_Forecast.csv",
            mime="text/csv"
        )

