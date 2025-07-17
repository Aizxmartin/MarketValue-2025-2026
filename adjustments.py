def calculate_adjustments(subject_info, comp_row):
    """
    Calculate adjustments for comparable properties based on square footage differences.
    
    Args:
        subject_info: Dictionary with subject property details
        comp_row: Pandas Series with comparable property data
    
    Returns:
        tuple: (total_adjustment, ag_adjustment, basement_adjustment, ag_diff, basement_diff)
    """
    # Standard adjustment rates per square foot
    AG_RATE = 40  # $/sf for above grade
    BASEMENT_RATE = 10  # $/sf for basement
    
    # Get subject property details
    subject_ag_sf = subject_info.get("sqft", 0)
    subject_basement_sf = subject_info.get("basement", 0)
    
    # Get comparable property details
    comp_ag_sf = comp_row.get("AG SF", comp_row.get("Above Grade Finished Area", 0))
    comp_basement_sf = comp_row.get("Basement SF", 0)
    
    # Calculate differences (Subject - Comparable)
    ag_diff = subject_ag_sf - comp_ag_sf
    basement_diff = subject_basement_sf - comp_basement_sf
    
    # Calculate adjustments
    ag_adjustment = ag_diff * AG_RATE
    basement_adjustment = basement_diff * BASEMENT_RATE
    
    total_adjustment = ag_adjustment + basement_adjustment
    
    return total_adjustment, ag_adjustment, basement_adjustment, ag_diff, basement_diff
