import numpy as np
import streamlit as st
import pandas as pd
import subprocess
import os
import sys

st.set_page_config(
page_title="Kosi Forecast",
layout="wide"
)

st.title("🌊 Kosi Basin Transformer Forecast System")

uploaded_file = st.file_uploader(
"📂 Upload Excel File",
type=["xlsx"]
)

if uploaded_file is not None:


    df = pd.read_excel(uploaded_file)

if np.issubdtype(df['date'].dtype, np.number):
    df['date'] = pd.to_datetime(
    df['date'],
    origin='1899-12-30',
    unit='D'
)
else:
df['date'] = pd.to_datetime(df['date'])


    st.subheader("📊 Uploaded Data")

    st.dataframe(df.head())

# SAVE INPUT FILE
df.to_excel("input.xlsx", index=False)

# RUN MODEL
if st.button("🚀 Run Prediction"):

    with st.spinner("Running Transformer Model..."):

        result = subprocess.run(
            [sys.executable, "predict.py"],
            capture_output=True,
            text=True
        )

    # SHOW LOGS
    st.subheader("🖥 Prediction Logs")

    st.text(result.stdout)

    # ERROR HANDLING
    if result.returncode != 0:

        st.error("❌ Prediction Failed")

        st.text(result.stderr)

    else:

        # CHECK OUTPUT
        if os.path.exists("output.csv"):

            pred = pd.read_csv("output.csv")

            st.success("✅ Prediction Completed!")

            st.subheader("📈 Forecast Results")

            st.dataframe(pred)

            # DOWNLOAD BUTTON
            csv = pred.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Forecast CSV",
                data=csv,
                file_name="Kosi_Forecast.csv",
                mime="text/csv"
            )

        else:

            st.error("❌ output.csv was not created")
