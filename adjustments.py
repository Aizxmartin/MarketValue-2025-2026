def calculate_adjustments(comp_row, subject, ag_rate, bsmt_rate):
    ag_diff = subject["sqft"] - comp_row["AG SF"]
    bsmt_diff = subject["basement"] - comp_row["Basement SF"]
    ag_adj = ag_diff * ag_rate
    bsmt_adj = bsmt_diff * bsmt_rate
    return ag_adj + bsmt_adj