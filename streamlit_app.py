
import streamlit as st
import pandas as pd

st.title("🧪 CMA Diagnostic: CSV Stage")

uploaded_csv = st.file_uploader("Upload MLS CSV/XLSX File", type=["csv", "xlsx"])

if uploaded_csv:
    try:
        if uploaded_csv.name.endswith(".csv"):
            df = pd.read_csv(uploaded_csv)
        else:
            df = pd.read_excel(uploaded_csv)
        df.columns = [col.strip().lower() for col in df.columns]
        st.success("✅ CSV/XLSX uploaded and parsed successfully.")
        st.write("Detected columns:", df.columns.tolist())
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"❌ Error reading CSV/XLSX: {e}")
