
def calculate_adjustments(subject_info, comp_row):
    ag_diff = subject_info["sqft"] - comp_row["AG SF"]
    bsmt_diff = subject_info["basement"] - comp_row.get("Basement SF", 0)
    ag_adj = ag_diff * 40
    bsmt_adj = bsmt_diff * 10
    total_adj = ag_adj + bsmt_adj
    return total_adj, ag_adj, bsmt_adj, ag_diff, bsmt_diff
