import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dataset/clean_train.csv")

labels = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]

counts = [df[label].sum() for label in labels]

plt.figure(figsize=(10,5))
plt.bar(labels, counts)

plt.title("Distribution of Toxic Comment Categories")
plt.xlabel("Categories")
plt.ylabel("Number of Comments")

plt.tight_layout()
plt.savefig("screenshots/category_distribution.png")

print("Chart saved in screenshots folder.")

plt.show()