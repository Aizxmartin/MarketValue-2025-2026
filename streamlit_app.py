
import streamlit as st
from utils.generate_report import generate_report
import pandas as pd
import base64
from PyPDF2 import PdfReader
import os

def main():
    st.title("📊 CMA Diagnostic Tool")

    uploaded_csv = st.file_uploader("Upload MLS CSV/XLSX", type=["csv", "xlsx"])
    uploaded_pdf = st.file_uploader("Upload PDF (optional)", type=["pdf"])

    if uploaded_csv:
        if uploaded_csv.name.endswith(".csv"):
            df = pd.read_csv(uploaded_csv)
        else:
            df = pd.read_excel(uploaded_csv)

        st.success("CSV/XLSX uploaded successfully.")

        # Normalize column names
        df.columns = [col.strip() for col in df.columns]

        # Generate Basement SF if not present
        if "Basement SF" not in df.columns:
            df["Basement SF"] = df["Building Area Total"] - df["Above Grade Finished Area"]

        # Convert key fields to numeric
        df["Close Price"] = pd.to_numeric(df["Close Price"], errors='coerce').fillna(0)
        df["Concessions"] = pd.to_numeric(df["Concessions"], errors='coerce').fillna(0)

        subject_info = {}
        subject_info["address"] = st.text_input("Property Address")
        subject_info["sqft"] = st.number_input("Above Grade SqFt", step=1)
        subject_info["basement"] = st.number_input("Basement SqFt", step=1)
        subject_info["bedrooms"] = st.number_input("Bedrooms", step=1)
        subject_info["bathrooms"] = st.number_input("Bathrooms", step=1)
        zestimate = st.number_input("Zillow Estimate", step=1000)
        redfin_est = st.number_input("Redfin Estimate", step=1000)

        if st.button("Generate Report"):
            pdf_text = ""
            if uploaded_pdf:
                pdf = PdfReader(uploaded_pdf)
                for page in pdf.pages:
                    pdf_text += page.extract_text() + "\n"

            report_path = generate_report(
                df,
                subject_info=subject_info,
                zillow_val=zestimate,
                redfin_val=redfin_est,
                pdf_text=pdf_text,
                real_avm=(zestimate + redfin_est) / 2 if zestimate and redfin_est else None
            )

            with open(report_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="Market_Valuation_Report.docx">📥 Download Report</a>'
                st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
