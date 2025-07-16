
import pandas as pd
import fitz

def parse_uploaded_csv(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
    df.columns = [c.strip().lower() for c in df.columns]
    df["address"] = (
        df["street number"].astype(str).str.strip() + " " +
        df["street name"].str.strip()
    )
    return df

def extract_real_avm(pdf_file, return_number=False):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    avm_value = None
    for page in doc:
        pg_text = page.get_text()
        text += pg_text + "\n"
        if "RealAVM" in pg_text and return_number:
            lines = pg_text.split("\n")
            for l in lines:
                if "RealAVM" in l:
                    parts = l.replace("$","").replace(",","").split()
                    for p in parts:
                        if p.isdigit():
                            avm_value = int(p)
    return avm_value if return_number else text
