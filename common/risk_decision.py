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

    final_result = {
        "file_path": file_event["file_path"],
        "integrity_status": crypto_result["integrity_status"],
        "ml_label": ml_label,
        "risk_score": risk_score,
        "risk_level": risk_level
    }

    return final_result

if __name__ == "__main__":
    file_event = {
        "file_path": "test.exe"
    }

    crypto_result = {
        "integrity_status": "MISMATCH"
    }

    ml_label = "malicious"

    result = make_risk_decision(file_event, crypto_result, ml_label)
    print(result)
