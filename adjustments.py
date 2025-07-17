def calculate_adjustments(subject_info, comp_row):
    """
    Calculate adjustments for comparable properties based only on above grade square footage differences.

    Args:
        subject_info: Dictionary with subject property details
        comp_row: Pandas Series with comparable property data

    Returns:
        tuple: (total_adjustment, ag_adjustment, ag_diff)
    """
    AG_RATE = 40  # $/sf for above grade

    subject_ag_sf = subject_info.get("sqft", 0)
    comp_ag_sf = comp_row.get("AG SF", comp_row.get("Above Grade Finished Area", 0))

    ag_diff = subject_ag_sf - comp_ag_sf
    ag_adjustment = ag_diff * AG_RATE

    return ag_adjustment, ag_adjustment, ag_diff
