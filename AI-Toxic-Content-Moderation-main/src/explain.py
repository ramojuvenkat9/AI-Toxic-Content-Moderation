import pandas as pd

def create_explanation(prediction):
    df = pd.DataFrame({
        "Category": prediction.keys(),
        "Score": prediction.values()
    })

    df = df.sort_values(
        by="Score",
        ascending=False
    )

    return df