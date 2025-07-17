def calculate_adjustments(subject_info, comp_row):
    ag_rate = 50
    bsmt_rate = 20
    ag_diff = subject_info["sqft"] - comp_row["Above Grade Finished Area"]
    bsmt_diff = subject_info["basement"] - comp_row["Basement SF"]
    adj = (ag_diff * ag_rate) + (bsmt_diff * bsmt_rate)
    return adj, ag_diff * ag_rate, bsmt_diff * bsmt_rate, ag_diff, bsmt_diff
