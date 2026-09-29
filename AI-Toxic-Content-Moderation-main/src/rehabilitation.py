def calculate_rehabilitation_score(risk_history):

    if len(risk_history) < 2:
        return 50

    improvement = risk_history[0] - risk_history[-1]

    score = 50 + improvement

    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return round(score, 2)


if __name__ == "__main__":

    risk_history = [
        92,
        81,
        70,
        56,
        44,
        28
    ]

    rehab = calculate_rehabilitation_score(
        risk_history
    )

    print("=" * 50)
    print("Risk History")
    print(risk_history)

    print("-" * 50)

    print("Rehabilitation Score :", rehab)