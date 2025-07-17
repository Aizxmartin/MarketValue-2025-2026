import streamlit as st
from utils.utils import generate_report
from utils.column_map import remap_columns
import pandas as pd

st.set_page_config(page_title="CMA Tool", layout="centered")
st.title("📊 CMA Tool – Final Report Format")

uploaded_csv = st.file_uploader("Upload MLS Data", type=["csv", "xlsx"])
uploaded_pdf = st.file_uploader("Upload Public Records PDF", type=["pdf"])

if uploaded_csv:
    if uploaded_csv.name.endswith(".csv"):
        df = pd.read_csv(uploaded_csv)
    else:
        df = pd.read_excel(uploaded_csv)
    df = remap_columns(df)
    st.write("Detected columns:", df.columns.tolist())

    subject_address = st.text_input("Subject Address")
    subject_sqft = st.number_input("Above Grade SqFt", min_value=0)
    subject_basement = st.number_input("Basement SqFt", min_value=0)
    subject_beds = st.number_input("Bedrooms", min_value=0)
    subject_baths = st.number_input("Bathrooms", min_value=0)
    zillow = st.number_input("Zillow Estimate", min_value=0)
    redfin = st.number_input("Redfin Estimate", min_value=0)

    real_avm = None
    if uploaded_pdf:
        from utils.extract_real_avm import extract_real_avm
        real_avm = extract_real_avm(uploaded_pdf, return_number=True)

    if st.button("Generate Report"):
        subject_info = {
            "address": subject_address,
            "sqft": subject_sqft,
            "basement": subject_basement,
            "beds": subject_beds,
            "baths": subject_baths,
        }
        report_path = generate_report(df, subject_info, zillow, redfin, real_avm)
        with open(report_path, "rb") as f:
            st.download_button("📄 Download Report", f, file_name="Market_Valuation_Report.docx")
