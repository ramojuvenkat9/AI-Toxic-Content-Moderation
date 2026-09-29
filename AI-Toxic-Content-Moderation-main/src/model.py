from transformers import AutoModelForSequenceClassification

from src.config import (
    MODEL_NAME,
    NUM_LABELS
)


def get_model():

    print("=" * 60)
    print("Loading DistilBERT Model...")

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=NUM_LABELS,
        problem_type="multi_label_classification"
    )

    print("Model Loaded Successfully!")

    return model


if __name__ == "__main__":

    model = get_model()

    print("=" * 60)
    print(model.config)