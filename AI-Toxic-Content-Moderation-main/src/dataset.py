import pandas as pd
import torch
from torch.utils.data import Dataset
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer

from src.config import (
    MODEL_NAME,
    MAX_LENGTH,
    RANDOM_STATE,
    TRAIN_SIZE
)

# Load Tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


class ToxicDataset(Dataset):

    def __init__(self, texts, labels):

        self.texts = list(texts)
        self.labels = labels.values

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):

        encoding = tokenizer(
            str(self.texts[idx]),
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(
                self.labels[idx],
                dtype=torch.float
            )
        }


def load_dataset():

    print("=" * 60)
    print("Loading Dataset...")

    df = pd.read_csv("dataset/final_dataset.csv")

    # Development Mode
    df = df.sample(
        n=TRAIN_SIZE,
        random_state=RANDOM_STATE
    )

    df["clean_comment"] = (
        df["clean_comment"]
        .fillna("")
        .astype(str)
    )

    X = df["clean_comment"]

    y = df[
        [
            "toxic",
            "severe_toxic",
            "obscene",
            "threat",
            "insult",
            "identity_hate"
        ]
    ]

    X_train, X_val, y_train, y_val = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE
    )

    train_dataset = ToxicDataset(X_train, y_train)
    val_dataset = ToxicDataset(X_val, y_val)

    print("Dataset Loaded Successfully")
    print(f"Training Samples : {len(train_dataset)}")
    print(f"Validation Samples : {len(val_dataset)}")

    return train_dataset, val_dataset


if __name__ == "__main__":

    train_dataset, val_dataset = load_dataset()