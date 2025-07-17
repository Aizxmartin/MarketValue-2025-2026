from docx import Document
import tempfile
from adjustments import calculate_adjustments

def generate_report(df, subject_info, zillow_val, redfin_val, pdf_text, real_avm):
    doc = Document()
    doc.add_heading("Market Valuation Report", 0)
    doc.add_paragraph(f"Subject Property: {subject_info['address']}")

    avg_adjusted = 0
    for _, row in df.iterrows():
        adj, ag_adj, bsmt_adj, ag_diff, bsmt_diff = calculate_adjustments(subject_info, row)
        adjusted_price = row["Close Price"] + row.get("Concessions", 0) + adj
        avg_adjusted += adjusted_price
        doc.add_paragraph(f"Comp: {row.get('Address', 'Unknown')}, Adj Price: ${adjusted_price:,.2f}")

    if len(df) > 0:
        avg_adjusted /= len(df)
        doc.add_paragraph(f"Average Adjusted Value: ${avg_adjusted:,.2f}")

    if real_avm:
        doc.add_paragraph(f"Real AVM (avg of Zillow & Redfin): ${real_avm:,.2f}")

    if pdf_text:
        doc.add_heading("PDF Notes", level=2)
        doc.add_paragraph(pdf_text)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        doc.save(tmp.name)
        return tmp.name
