import pandas as pd
from docx import Document
import tempfile

def generate_report(df, subject_info, zillow_val=None, redfin_val=None, real_avm=None):
    comps = []
    AG_RATE = 40

    for _, row in df.iterrows():
        try:
            ag_sf = row.get("AG SF", row.get("Above Grade Finished Area", 0))
            ag_diff = subject_info.get("sqft", 0) - ag_sf
            ag_adjustment = ag_diff * AG_RATE
            close_price = row.get("Close Price", 0)
            concessions = row.get("Concessions", 0)
            adjusted_price = close_price + concessions + ag_adjustment
            ppsf = adjusted_price / ag_sf if ag_sf > 0 else 0

            comps.append({
                "Address": row.get("Street Address", row.get("Address", "N/A")),
                "Close Price": close_price,
                "Concessions": concessions,
                "AG SF": ag_sf,
                "AG Diff": ag_diff,
                "Adjustment": ag_adjustment,
                "Adjusted Price": round(adjusted_price),
                "Adjusted PPSF": round(ppsf, 2)
            })
        except:
            continue

    doc = Document()
    doc.add_heading("Market Valuation Report", 0)
    doc.add_paragraph(f"Address: {subject_info.get('address', 'N/A')}")
    doc.add_paragraph(f"Above Grade SF: {subject_info.get('sqft', 0)}")
    doc.add_paragraph(f"Bedrooms: {subject_info.get('bedrooms', 0)} | Bathrooms: {subject_info.get('bathrooms', 0)}")

    if comps:
        doc.add_heading("Comparable Sales", level=1)
        table = doc.add_table(rows=1, cols=len(comps[0]))
        hdr_cells = table.rows[0].cells
        for i, key in enumerate(comps[0].keys()):
            hdr_cells[i].text = key
        for comp in comps:
            row_cells = table.add_row().cells
            for i, key in enumerate(comp.keys()):
                row_cells[i].text = str(comp[key])

        avg_adj = sum(c['Adjusted Price'] for c in comps) / len(comps)
        doc.add_heading("Valuation Summary", level=1)
        if real_avm:
            doc.add_paragraph(f"RealAVM: ${real_avm:,}")
            doc.add_paragraph(f"Estimated Range: ${real_avm:,} – ${int(avg_adj):,}")
        else:
            doc.add_paragraph(f"Average Adjusted Price: ${int(avg_adj):,}")

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp.name)
    return temp.name
