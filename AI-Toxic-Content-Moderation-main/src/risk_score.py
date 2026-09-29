from src.user_profile import UserProfile


def calculate_risk_score(current_toxicity, user):

    score = (
        current_toxicity * 60
        + user.average_toxicity() * 25
        + user.warnings * 5
        + user.moderator_reviews * 10
    )

    if score > 100:
        score = 100

    return round(score, 2)


if __name__ == "__main__":

    user = UserProfile()

    user.add_comment(0.95)
    user.add_comment(0.82)
    user.add_comment(0.15)

    user.add_warning()
    user.add_moderator_review()

    current_toxicity = 0.91

    risk = calculate_risk_score(
        current_toxicity,
        user
    )

    print("=" * 50)
    print("CURRENT TOXICITY :", current_toxicity)
    print("AVERAGE HISTORY  :", round(user.average_toxicity(), 2))
    print("WARNINGS         :", user.warnings)
    print("MODERATOR        :", user.moderator_reviews)
    print("-" * 50)
    print("RISK SCORE       :", risk)