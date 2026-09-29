class UserProfile:

    def __init__(self):

        self.previous_scores = []

        self.warnings = 0

        self.rewrites_accepted = 0

        self.moderator_reviews = 0

    def add_comment(self, toxicity_score):

        self.previous_scores.append(toxicity_score)

    def add_warning(self):

        self.warnings += 1

    def add_rewrite(self):

        self.rewrites_accepted += 1

    def add_moderator_review(self):

        self.moderator_reviews += 1

    def average_toxicity(self):

        if len(self.previous_scores) == 0:

            return 0

        return sum(self.previous_scores) / len(self.previous_scores)

    def display(self):

        print("=" * 50)

        print("USER PROFILE")

        print("=" * 50)

        print("Previous Comments :", len(self.previous_scores))

        print("Average Toxicity  :", round(self.average_toxicity(), 3))

        print("Warnings          :", self.warnings)

        print("Rewrite Accepted  :", self.rewrites_accepted)

        print("Moderator Reviews :", self.moderator_reviews)


if __name__ == "__main__":

    user = UserProfile()

    user.add_comment(0.95)

    user.add_comment(0.82)

    user.add_comment(0.15)

    user.add_warning()

    user.add_rewrite()

    user.display()