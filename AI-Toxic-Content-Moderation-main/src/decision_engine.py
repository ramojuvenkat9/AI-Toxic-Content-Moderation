def make_decision(severity, risk_score, rehab_score):

    if severity == "SAFE":
        return "Publish"

    elif severity == "MILD":

        if rehab_score >= 70:
            return "Publish with Warning"

        return "Warning"

    elif severity == "HIGH":

        if rehab_score >= 80:
            return "Rewrite Comment"

        return "Moderator Review"

    elif severity == "SEVERE":

        if risk_score >= 80:
            return "Block and Send to Moderator"

        return "Moderator Review"

    return "Unknown"


if __name__ == "__main__":

    severity = "HIGH"

    risk = 85.6

    rehab = 92

    decision = make_decision(
        severity,
        risk,
        rehab
    )

    print("=" * 50)
    print("Severity :", severity)
    print("Risk Score :", risk)
    print("Rehabilitation :", rehab)
    print("-" * 50)
    print("FINAL DECISION")
    print(decision)