def get_severity(probabilities):

    max_score = max(probabilities.values())

    if max_score < 0.20:

        severity = "SAFE"
        action = "Publish"

    elif max_score < 0.50:

        severity = "MILD"
        action = "Warning"

    elif max_score < 0.80:

        severity = "HIGH"
        action = "Rewrite"

    else:

        severity = "SEVERE"
        action = "Moderator Review"

    return severity, action