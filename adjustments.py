def calculate_adjustments(subject, comp, ag_rate=40, basement_rate=10):
    ag_diff = subject["sqft"] - comp["AG SF"]
    basement_diff = subject["basement"] - comp["Basement SF"]
    ag_adj = ag_diff * ag_rate
    basement_adj = basement_diff * basement_rate
    concession = comp.get("Concessions", 0)
    adjusted_price = comp["Close Price"] - concession + ag_adj + basement_adj
    adj_ppsf = adjusted_price / comp["AG SF"] if comp["AG SF"] else 0
    return {
        "Adjusted Price": adjusted_price,
        "AG Diff": ag_diff,
        "Basement Diff": basement_diff,
        "Adjusted PPSF": round(adj_ppsf, 2),
    }