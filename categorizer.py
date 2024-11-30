from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the pretrained model and tokenizer
MODEL_NAME = "moctarsmal/bank-transactions-statements-classification"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)  # Use slow tokenizer if fast tokenizer fails
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
except ValueError as e:
    print(f"Error loading tokenizer or model: {e}")
    raise

# Mapping model output to categories
LABELS = {
    0: "Utility",
    1: "Non-Utility"
}

def categorize_transaction(description):
    """
    Classify a transaction as Utility or Non-Utility based on its description.
    """
    print(f"Description: {description}")

    # Tokenize the input description
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    print(f"Tokenized Inputs: {inputs}")

    # Get predictions from the model
    with torch.no_grad():
        outputs = model(**inputs)

        print(f"Model Outputs: {outputs.logits}")
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
        print(f"Predicted Label: {predicted_label}")

    # Map the predicted label to its corresponding category
    return LABELS[predicted_label]






