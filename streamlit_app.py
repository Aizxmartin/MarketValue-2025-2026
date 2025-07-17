import streamlit as st
from adjustments import calculate_adjustments
from utils import extract_real_avm, parse_uploaded_csv, generate_report

st.set_page_config(page_title="📊 CMA Tool – Final Report Format", layout="wide")
st.title("📊 CMA Tool – Final Report Format")

uploaded_csv = st.file_uploader("Upload MLS Data", type=["csv", "xlsx"])
uploaded_pdf = st.file_uploader("Upload Public Records PDF", type=["pdf"])

if uploaded_csv:
    df = parse_uploaded_csv(uploaded_csv)
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
        real_avm = extract_real_avm(uploaded_pdf, return_number=True)

    if st.button("Generate Report"):
        report_path = generate_report(
            df,
            subject_info={
                "address": subject_address,
                "sqft": subject_sqft,
                "basement": subject_basement,
                "beds": subject_beds,
                "baths": subject_baths,
            },
            zillow=zillow,
            redfin=redfin,
            real_avm=real_avm
        )
        with open(report_path, "rb") as f:
            st.download_button("📄 Download Report", f, file_name="Market_Valuation_Report.docx")