REWRITE_SENTENCES = {

    "you are an idiot":
        "I respectfully disagree with your opinion.",

    "you are stupid":
        "I think your argument could be improved.",

    "i hate you":
        "I disagree with your perspective.",

    "i will kill you":
        "This comment violates community guidelines.",

    "shut up":
        "Let's continue the discussion respectfully."
}


def rewrite_comment(comment):

    text = comment.lower().strip()

    text = text.replace(".", "")
    text = text.replace("!", "")
    text = text.replace("?", "")

    if text in REWRITE_SENTENCES:
        return REWRITE_SENTENCES[text]

    return "Please consider rephrasing your comment in a respectful manner."


if __name__ == "__main__":

    comment = input("Enter Comment : ")

    print("\nSuggested Rewrite:\n")

    print(rewrite_comment(comment))