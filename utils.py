
import pandas as pd
import fitz  # PyMuPDF
from docx import Document
import tempfile

def extract_real_avm(uploaded_pdf, return_number=False):
    doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
    for page in doc:
        text = page.get_text()
        for line in text.split("\n"):
            if "RealAVM" in line and "$" in line:
                try:
                    value = int("".join(filter(str.isdigit, line)))
                    return value if return_number else f"${value:,.0f}"
                except:
                    continue
    return None

def parse_uploaded_csv(uploaded_csv):
    df = pd.read_csv(uploaded_csv)
    # Remap known headers to standard ones
    column_map = {
        "close price": "Close Price",
        "concessions": "Concessions",
        "above grade finished area": "AG SF",
        "basement sqft": "Basement SF",
        "address": "Address"
    }
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={k.lower(): v for k, v in column_map.items()})
    return df

def generate_report(df, subject_info, zillow, redfin, real_avm):
    from adjustments import calculate_adjustments

    results = []
    for _, row in df.iterrows():
        adj = calculate_adjustments(subject_info, row)
        results.append({
            "Address": row["Address"],
            "Close Price": row["Close Price"],
            "Concessions": row["Concessions"],
            "AG SF": row["AG SF"],
            "Basement SF": row["Basement SF"],
            "AG Adj ($/sf)": 40,
            "Basement Adj ($/sf)": 10,
            **adj
        })

    doc = Document()
    doc.add_heading("Market Valuation Report – Adjusted Comparison with Breakdown", level=1)
    doc.add_paragraph("Below is a breakdown of how adjustments were applied to comparable properties. "
                      "Close Price remains the original sale price. Adjustments are applied based on square footage differences for Above Grade (AG) and Basement Finished area.")

    table = doc.add_table(rows=1, cols=len(results[0]))
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(results[0].keys()):
        hdr_cells[i].text = col

    for result in results:
        row_cells = table.add_row().cells
        for i, val in enumerate(result.values()):
            row_cells[i].text = f"{val:,.0f}" if isinstance(val, (int, float)) else str(val)

    doc.add_paragraph()
    doc.add_heading("Finalized Listing Agent Blurb (with Value Range)", level=2)
    start_range = round((real_avm + zillow + redfin) / 3)
    avg_adjusted = sum(r["Adjusted Price"] for r in results) / len(results)
    doc.add_paragraph("We've provided a valuation report using a consistent, data-driven adjustment model "
                      "designed for real-time market pricing—not retrospective appraisals. "
                      "All comparable properties were selected within a 20% range of the subject's above-grade square footage "
                      "and adjusted using a tiered system that distinguishes above-grade, basement, and finished basement areas separately. "
                      "We also accounted for features like walkout basements, concessions, garage bays, and views.")
    doc.add_paragraph(
        f"Market Range: ${start_range:,.0f} – ${int(avg_adjusted):,}"
    )
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_file.name)
    return temp_file.name
