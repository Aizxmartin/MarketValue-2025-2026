
def calculate_adjustments(subject_info, comp_row, ag_rate=40, basement_rate=10):
    ag_diff = subject_info["sqft"] - comp_row["AG SF"]
    bsmt_diff = subject_info["basement"] - comp_row["Basement SF"]
    adj_price = comp_row["Close Price"] - comp_row["Concessions"]
    adj_price += ag_diff * ag_rate + bsmt_diff * basement_rate
    return {
        "AG Diff": ag_diff,
        "Basement Diff": bsmt_diff,
        "Adjusted Price": adj_price,
        "Adjusted PPSF": round(adj_price / comp_row["AG SF"], 2)
    }
