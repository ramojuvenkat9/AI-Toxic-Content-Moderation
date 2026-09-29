import os
import torch
from torch.utils.data import DataLoader
from torch.optim import AdamW
from tqdm import tqdm
from transformers import AutoTokenizer

from src.dataset import load_dataset
from src.model import get_model
from src.config import (
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE
)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("=" * 60)
print("Device :", DEVICE)
print("=" * 60)


# Load Dataset
train_dataset, val_dataset = load_dataset()

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

print(f"Training Batches : {len(train_loader)}")
print(f"Validation Batches : {len(val_loader)}")


# Load Model
model = get_model()

model.to(DEVICE)

optimizer = AdamW(
    model.parameters(),
    lr=LEARNING_RATE
)

print("=" * 60)
print("Starting Model Training...")
print("=" * 60)

for epoch in range(EPOCHS):

    print(f"\nEpoch {epoch + 1}/{EPOCHS}")

    model.train()

    total_loss = 0

    progress_bar = tqdm(train_loader)

    for batch in progress_bar:

        # Move batch to CPU
        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["labels"].to(DEVICE)

        # Clear previous gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss

        # Backpropagation
        loss.backward()

        # Update weights
        optimizer.step()

        total_loss += loss.item()

        progress_bar.set_postfix(
            loss=loss.item()
        )

    avg_loss = total_loss / len(train_loader)

    print(f"Average Training Loss : {avg_loss:.4f}")

print("\nTraining Completed Successfully!")

# Save Model
save_path = "model/trained_model"

model.save_pretrained(save_path)

print("Model Saved Successfully!")
# Save Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
tokenizer.save_pretrained(save_path)

print("Tokenizer Saved Successfully!")