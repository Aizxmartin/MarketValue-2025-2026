
import pandas as pd
from docx import Document
import tempfile
import fitz

def extract_real_avm(pdf_file, return_number=False):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "".join([page.get_text() for page in doc])
    import re
    match = re.search(r"RealAVM™\s+\$([\d,]+)", text)
    if match:
        val = int(match.group(1).replace(",", ""))
        return val if return_number else f"${val:,}"
    return None

def parse_uploaded_csv(uploaded_csv):
    df = pd.read_csv(uploaded_csv) if uploaded_csv.name.endswith(".csv") else pd.read_excel(uploaded_csv)

    # Rename columns
    df = df.rename(columns={
        "Above Grade Finished Area": "AG SF",
        "Close Price": "Close Price",
        "Concessions": "Concessions",
        "Building Area Total": "Total SF"
    })

    # Compute Basement SF
    df["Basement SF"] = df["Total SF"] - df["AG SF"]

    return df

def generate_report(df, subject_info, zillow, redfin, real_avm):
    from adjustments import calculate_adjustments

    comps = []
    for _, row in df.iterrows():
        adj, ag_adj, bsmt_adj, ag_diff, bsmt_diff = calculate_adjustments(subject_info, row)
        adjusted_price = row["Close Price"] + row.get("Concessions", 0) + adj
        ppsf = adjusted_price / row["AG SF"]
        comps.append({
            "Address": row.get("Street Address", "N/A"),
            "Close Price": row["Close Price"],
            "Concessions": row.get("Concessions", 0),
            "AG SF": row["AG SF"],
            "Basement SF": row["Basement SF"],
            "AG Adj ($/sf)": 40,
            "Basement Adj ($/sf)": 10,
            "AG Diff": ag_diff,
            "Basement Diff": bsmt_diff,
            "Adjusted Price": round(adjusted_price),
            "Adjusted PPSF": round(ppsf, 2)
        })

    doc = Document()
    doc.add_heading("Market Valuation Report – Adjusted Comparison with Breakdown", 0)
    doc.add_paragraph("Date: July 17, 2025")
    doc.add_paragraph("Below is a breakdown of how adjustments were applied to comparable properties. Close Price remains the original sale price. Adjustments are applied based on square footage differences for Above Grade (AG) and Basement Finished area.")

    table = doc.add_table(rows=1, cols=len(comps[0]))
    table.style = 'Light Grid'
    hdr_cells = table.rows[0].cells
    for i, key in enumerate(comps[0].keys()):
        hdr_cells[i].text = key

    for comp in comps:
        row_cells = table.add_row().cells
        for i, key in enumerate(comp.keys()):
            row_cells[i].text = f"{comp[key]:,}" if isinstance(comp[key], (int, float)) else str(comp[key])

    doc.add_paragraph()
    doc.add_paragraph("Finalized Listing Agent Blurb (with Value Range)")
    doc.add_paragraph("We've provided a valuation report using a consistent, data-driven adjustment model...")

    start_range = round((real_avm + zillow + redfin) / 3) if all([real_avm, zillow, redfin]) else 800000
    avg_adjusted = sum(c['Adjusted Price'] for c in comps) / len(comps)
    doc.add_paragraph(f"Market Range: ${start_range:,.0f} – ${int(avg_adjusted):,}")
    doc.add_paragraph(f"The starting value (${start_range:,.0f}) reflects an average of public-facing automated estimates from RealAVM, Zillow, and Redfin.")

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp.name)
    return temp.name
