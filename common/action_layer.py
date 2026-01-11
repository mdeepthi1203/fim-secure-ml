def take_action(final_result):
    """
    Action layer: alert or log based on risk level
    """

    if final_result["risk_level"] == "HIGH":
        print("🚨 ALERT: Malicious file change detected")
    else:
        print("ℹ️ Benign file change logged")

if __name__ == "__main__":
    test_result_high = {
        "risk_level": "HIGH"
    }

    test_result_low = {
        "risk_level": "LOW"
    }

    take_action(test_result_high)
    take_action(test_result_low)
