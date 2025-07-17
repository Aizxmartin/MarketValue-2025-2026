def calculate_adjustments(subject_info, comp_row, ag_rate=40, basement_rate=10):
    ag_sf = comp_row.get("AG SF", 0) or 0
    bsmt_sf = comp_row.get("Basement SF", 0) or 0
    close_price = comp_row.get("Close Price", 0) or 0
    concessions = comp_row.get("Concessions", 0) or 0

    ag_diff = subject_info.get("sqft", 0) - ag_sf
    bsmt_diff = subject_info.get("basement", 0) - bsmt_sf

    adj_price = close_price + concessions + (ag_diff * ag_rate) + (bsmt_diff * basement_rate)
    adjusted_ppsf = round(adj_price / ag_sf, 2) if ag_sf else 0

    return {
        "AG Diff": ag_diff,
        "Basement Diff": bsmt_diff,
        "Adjusted Price": adj_price,
        "Adjusted PPSF": adjusted_ppsf
    }
