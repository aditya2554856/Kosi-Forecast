import streamlit as st
import pandas as pd
import subprocess
import os

# ============================================================

# PAGE CONFIG

# ============================================================

st.set_page_config(
page_title="Kosi Basin Forecast",
layout="wide"
)

# ============================================================

# TITLE

# ============================================================

st.title("🌊 Kosi Basin Transformer Forecast System")

# ============================================================

# FILE UPLOADER

# ============================================================

uploaded_file = st.file_uploader(
"📂 Upload Excel File",
type=["xlsx"]
)

# ============================================================

# PROCESS FILE

# ============================================================

if uploaded_file is not None:

# READ DATA
df = pd.read_excel(uploaded_file)

st.subheader("📊 Uploaded Data")

st.dataframe(df.head())

# SAVE INPUT
df.to_excel("input.xlsx", index=False)

# RUN MODEL
if st.button("🚀 Run Prediction"):

    with st.spinner("Running Transformer Model..."):

        result = subprocess.run(
            ["python", "predict.py"],
            capture_output=True,
            text=True
        )

    # SHOW TERMINAL OUTPUT
    st.subheader("🖥 Prediction Logs")

    st.text(result.stdout)

    # SHOW ERRORS
    if result.returncode != 0:

        st.error("❌ Prediction Failed")

        st.text(result.stderr)

    else:

        # CHECK OUTPUT EXISTS
        if os.path.exists("output.csv"):

            pred = pd.read_csv("output.csv")

            st.success("✅ Prediction Completed!")

            st.subheader("📈 Forecast Results")

            st.dataframe(pred)

            # DOWNLOAD BUTTON
            csv = pred.to_csv(index=False).encode('utf-8')

            st.download_button(
                label="📥 Download Forecast CSV",
                data=csv,
                file_name="Kosi_Forecast.csv",
                mime="text/csv"
            )

        else:

            st.error("❌ output.csv was not created")
