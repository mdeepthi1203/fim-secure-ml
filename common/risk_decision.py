def make_risk_decision(file_event, crypto_result, ml_label):
    """
    Converts ML label into final security risk decision
    """

    if ml_label.lower() == "benign":
        risk_score = 0
        risk_level = "LOW"
    else:
        risk_score = 1
        risk_level = "HIGH"

    # FINAL ACTION LOGIC (THIS WAS MISSING)
    file_path = file_event["file_path"].lower()
    if crypto_result["integrity_status"] == "MISMATCH" and (
    risk_level == "HIGH" or file_path.endswith(".exe")
):
        final_action = "ALERT RAISED"
    else:
        final_action = "LOG ONLY"




    final_result = {
        "file_path": file_event["file_path"],
        "integrity_status": crypto_result["integrity_status"],
        "ml_label": ml_label,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "final_action": final_action
    }

    return final_result
