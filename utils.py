import pandas as pd
import fitz

def parse_uploaded_csv(uploaded_csv):
    if uploaded_csv.name.endswith(".csv"):
        return pd.read_csv(uploaded_csv)
    else:
        return pd.read_excel(uploaded_csv)

def extract_real_avm(pdf_file, return_number=False):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    if return_number:
        import re
        match = re.search(r"Real AVM[^\d]*(\$?[\d,]+)", text)
        if match:
            return int(match.group(1).replace(",", "").replace("$", ""))
        return None
    return text
