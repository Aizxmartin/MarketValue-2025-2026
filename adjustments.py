
import pandas as pd
from docx import Document
from datetime import date
import tempfile

def process_adjustments(df, subject_info, zillow, redfin, real_avm, pdf_text):
    df["NetPrice"] = df["close price"] - df["concessions"].fillna(0)
    df["PricePerSF"] = df["NetPrice"] / df["above grade finished area"]
    avg_ppsf = df["PricePerSF"].mean()

    online_estimates = [v for v in [zillow, redfin, real_avm] if v]
    online_avg = sum(online_estimates) / len(online_estimates) if online_estimates else 0
    est_subject_price = avg_ppsf * subject_info["sqft"]

    blended_est = (online_avg + est_subject_price) / 2 if online_avg else est_subject_price

    doc = Document()
    doc.add_heading("Market Valuation Report", 0)
    doc.add_paragraph(f"Date: {date.today().strftime('%B %d, %Y')}")
    doc.add_heading("Subject Property", level=1)
    doc.add_paragraph(f"Address: {subject_info['address']}")
    doc.add_paragraph(f"Above Grade SqFt: {subject_info['sqft']}")
    doc.add_paragraph(f"Basement SqFt: {subject_info['basement']}")
    doc.add_paragraph(f"Bedrooms: {subject_info['beds']}")
    doc.add_paragraph(f"Bathrooms: {subject_info['baths']}")
    doc.add_paragraph(f"Close Price: ${subject_info['price']:,.0f}")

    doc.add_heading("Estimates", level=1)
    doc.add_paragraph(f"Online Estimates Average: ${online_avg:,.0f}")
    doc.add_paragraph(f"PPSF Estimate: ${est_subject_price:,.0f}")
    doc.add_paragraph(f"Blended Estimate: ${blended_est:,.0f}")

    doc.add_heading("Comparable Properties", level=1)
    for _, row in df.iterrows():
        doc.add_paragraph(
            f"{row['address']} - Net ${row['NetPrice']:,.0f} | {row['above grade finished area']} SqFt | PPSF ${row['PricePerSF']:,.2f}",
            style="List Bullet"
        )

    if pdf_text:
        doc.add_heading("Public Record Details", level=1)
        doc.add_paragraph(pdf_text)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_file.name)
    return temp_file.name
