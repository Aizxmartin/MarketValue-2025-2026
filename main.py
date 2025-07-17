import streamlit as st
import base64
from adjustments import process_adjustments
from utils import extract_real_avm, parse_uploaded_csv

st.title("📊 Advanced CMA Tool")

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
    subject_price = st.number_input("Close Price", min_value=0)
    zillow = st.number_input("Zillow Estimate", min_value=0)
    redfin = st.number_input("Redfin Estimate", min_value=0)

    pdf_text = ""
    real_avm = None
    if uploaded_pdf is not None:
        try:
            pdf_text = extract_real_avm(uploaded_pdf)
            real_avm = extract_real_avm(uploaded_pdf, return_number=True)
        except Exception as e:
            st.warning("PDF could not be read. Continuing without AVM.")
            pdf_text = ""
            real_avm = None

    if st.button("Generate Report"):
        report_path = process_adjustments(
            df,
            subject_info={
                "address": subject_address,
                "sqft": subject_sqft,
                "basement": subject_basement,
                "beds": subject_beds,
                "baths": subject_baths,
                "price": subject_price
            },
            zillow=zillow,
            redfin=redfin,
            real_avm=real_avm,
            pdf_text=pdf_text
        )
        with open(report_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Market_Valuation_Report.docx">📄 Download Report</a>'
            st.markdown(href, unsafe_allow_html=True)
