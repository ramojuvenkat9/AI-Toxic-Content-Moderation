import pandas as pd
import re

# Load dataset
train_df = pd.read_csv("dataset/train.csv")

# Function to clean text
def clean_text(text):
    text = str(text).lower()                     # Convert to lowercase
    text = re.sub(r"http\S+|www\S+", "", text)  # Remove URLs
    text = re.sub(r"<.*?>", "", text)           # Remove HTML tags
    text = re.sub(r"[^a-zA-Z\s]", "", text)     # Remove numbers & punctuation
    text = re.sub(r"\s+", " ", text).strip()    # Remove extra spaces
    return text

# Apply preprocessing
train_df["clean_comment"] = train_df["comment_text"].apply(clean_text)

# Display original and cleaned comments
print("=" * 60)

for i in range(5):
    print(f"\nOriginal Comment {i+1}:")
    print(train_df["comment_text"][i])

    print("\nCleaned Comment:")
    print(train_df["clean_comment"][i])

    print("-" * 60)

# Save cleaned dataset
train_df.to_csv("dataset/clean_train.csv", index=False)

print("\n✅ Cleaned dataset saved as dataset/clean_train.csv")