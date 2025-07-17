import streamlit as st
from generate_report import generate_report
import pandas as pd
import base64
from PyPDF2 import PdfReader
import os

def main():
    st.title("📊 CMA Diagnostic Tool")
    st.write("Upload your MLS data and generate a comprehensive market valuation report.")

    uploaded_csv = st.file_uploader("Upload MLS CSV/XLSX", type=["csv", "xlsx"])
    uploaded_pdf = st.file_uploader("Upload PDF (optional)", type=["pdf"])

    if uploaded_csv:
        try:
            if uploaded_csv.name.endswith(".csv"):
                df = pd.read_csv(uploaded_csv)
            else:
                df = pd.read_excel(uploaded_csv)

            st.success("CSV/XLSX uploaded successfully.")
            st.write(f"Loaded {len(df)} properties")

            with st.expander("View Column Names"):
                st.write(df.columns.tolist())
            with st.expander("Preview Data"):
                st.dataframe(df.head())

            df.columns = [col.strip() for col in df.columns]

            numeric_columns = ["Close Price", "Concessions"]
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

            st.header("Subject Property Information")
            col1, col2 = st.columns(2)

            with col1:
                subject_info = {}
                subject_info["address"] = st.text_input("Property Address")
                subject_info["sqft"] = st.number_input("Above Grade SqFt", min_value=0, step=1)

            with col2:
                subject_info["bedrooms"] = st.number_input("Bedrooms", min_value=0, step=1)
                subject_info["bathrooms"] = st.number_input("Bathrooms", min_value=0.0, step=0.5)

            st.header("Automated Valuations")
            col3, col4 = st.columns(2)

            with col3:
                zestimate = st.number_input("Zillow Estimate", min_value=0, step=1000)
            with col4:
                redfin_est = st.number_input("Redfin Estimate", min_value=0, step=1000)

            if st.button("Generate Report", type="primary"):
                if not subject_info["address"]:
                    st.error("Please enter a property address.")
                    return
                if subject_info["sqft"] == 0:
                    st.error("Please enter the above grade square footage.")
                    return

                with st.spinner("Generating report..."):
                    try:
                        pdf_text = ""
                        if uploaded_pdf:
                            pdf = PdfReader(uploaded_pdf)
                            for page in pdf.pages:
                                pdf_text += page.extract_text() + "\n"

                        real_avm = None
                        if zestimate and redfin_est:
                            real_avm = (zestimate + redfin_est) / 2

                        report_path = generate_report(
                            df,
                            subject_info=subject_info,
                            zillow_val=zestimate if zestimate > 0 else None,
                            redfin_val=redfin_est if redfin_est > 0 else None,
                            pdf_text=pdf_text,
                            real_avm=real_avm
                        )

                        with open(report_path, "rb") as f:
                            b64 = base64.b64encode(f.read()).decode()
                            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Market_Valuation_Report.docx">📥 Download Report</a>'
                            st.markdown(href, unsafe_allow_html=True)

                        st.success("Report generated successfully!")

                        try:
                            os.unlink(report_path)
                        except:
                            pass
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                        st.write("Please check your data format and try again.")
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()
