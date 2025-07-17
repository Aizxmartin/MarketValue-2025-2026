def calculate_adjustments(subject_info, comp_row):
    AG_RATE = 40
    BASEMENT_RATE = 10

    subject_ag_sf = subject_info.get("sqft", 0)
    subject_basement_sf = subject_info.get("basement", 0)

    comp_ag_sf = comp_row.get("AG SF", comp_row.get("Above Grade Finished Area", 0))
    comp_basement_sf = comp_row.get("Basement SF", 0)

    ag_diff = subject_ag_sf - comp_ag_sf
    basement_diff = subject_basement_sf - comp_basement_sf

    ag_adjustment = ag_diff * AG_RATE
    basement_adjustment = basement_diff * BASEMENT_RATE

    total_adjustment = ag_adjustment + basement_adjustment

    return total_adjustment, ag_adjustment, basement_adjustment, ag_diff, basement_diff