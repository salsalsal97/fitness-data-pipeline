def build_base_record(target_date):
    """
    Common columns to both pipelines
    """
    out = {
        "date": target_date.isoformat(),
        "day": target_date.strftime("%A"),
    }
    return out
