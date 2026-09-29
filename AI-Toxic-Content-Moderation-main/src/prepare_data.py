import pandas as pd

# Load cleaned dataset
df = pd.read_csv("dataset/clean_train.csv")

print("=" * 60)
print("Original Dataset Shape")
print(df.shape)

# Keep only required columns
final_df = df[[
    "clean_comment",
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
]]

# Remove duplicate comments
final_df = final_df.drop_duplicates(subset=["clean_comment"])

# Save final dataset
final_df.to_csv("dataset/final_dataset.csv", index=False)

print("\nFinal Dataset Shape")
print(final_df.shape)

print("\nColumns")
print(final_df.columns)

print("\nFirst Five Rows")
print(final_df.head())

print("\nDataset saved successfully!")