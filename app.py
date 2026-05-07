import streamlit as st
import pandas as pd
import os

# ============================================================
# TITLE
# ============================================================
st.title("🌊 Kosi Basin Transformer Forecast System")

# ============================================================
# FILE UPLOAD
# ============================================================
uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx"]
)

# ============================================================
# MAIN
# ============================================================
if uploaded_file:

    df = pd.read_excel(uploaded_file)

    st.subheader("📊 Uploaded Data")
    st.dataframe(df.head())

    # Save uploaded file
    df.to_excel("/Users/aditya/Desktop/input.xlsx", index=False)

    if st.button("🔮 Run Transformer Prediction"):

        with st.spinner("Running Transformer Model..."):

            # Run prediction script
            os.system("python /Users/aditya/Desktop/predict.py")

            # Load prediction
            pred = pd.read_csv("/Users/aditya/Desktop/output.csv")

        st.success("✅ Prediction Completed")

        st.subheader("📈 Forecast Results")
        st.dataframe(pred)

        # Download
        st.download_button(
            label="📥 Download Forecast",
            data=pred.to_csv(index=False),
            file_name="Transformer_Predictions.csv",
            mime="text/csv"
        )