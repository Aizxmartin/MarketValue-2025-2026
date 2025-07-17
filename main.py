
import streamlit as st

st.set_page_config(page_title="CMA Diagnostic", layout="centered")
st.title("🛠 CMA Diagnostic Tool")

st.markdown("Use this version to confirm app functionality and troubleshoot display issues.")

# Step 1: File Uploads
csv_file = st.file_uploader("Upload MLS CSV/XLSX", type=["csv", "xlsx"])
pdf_file = st.file_uploader("Upload PDF (optional)", type=["pdf"])

if csv_file:
    st.success("CSV/XLSX uploaded successfully.")
else:
    st.info("Please upload a valid MLS CSV/XLSX file.")

if pdf_file:
    st.success("PDF uploaded successfully.")

# Step 2: Form Inputs
with st.form("property_info_form"):
    st.markdown("### Enter Subject Property Information")
    address = st.text_input("Property Address")
    sqft = st.number_input("Above Grade SqFt", min_value=0)
    basement = st.number_input("Basement SqFt", min_value=0)
    beds = st.number_input("Bedrooms", min_value=0)
    baths = st.number_input("Bathrooms", min_value=0)
    submitted = st.form_submit_button("Submit Property Info")

if submitted:
    st.success("Form submitted successfully!")
    st.write("Address:", address)
    st.write("Above Grade SqFt:", sqft)
    st.write("Basement SqFt:", basement)
    st.write("Bedrooms:", beds)
    st.write("Bathrooms:", baths)
