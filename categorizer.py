from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json

MODEL_NAME = "moctarsmal/bank-transactions-statements-classification"

# Correct and reload the tokenizer
tokenizer_path = "C:/Users/K TEJASWI/Downloads/vocab.json"

with open("vocab.json", encoding="utf-8") as f:
    corrected_vocab = json.load(f)


# Define special tokens explicitly
special_tokens = {
    "bos_token": "<s>",
    "eos_token": "</s>",
    "pad_token": "<pad>",
    "unk_token": "<unk>",
    "additional_special_tokens": ["<special0>", "<special1>", "<special2>", "<special3>", "<special4>"]
}

# Load tokenizer with corrected vocab
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
tokenizer.add_tokens(list(corrected_vocab.keys()))
tokenizer.add_special_tokens(special_tokens)

# Resize the model's embeddings to match the updated tokenizer
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.resize_token_embeddings(len(tokenizer))

# Mapping model output to categories
LABELS = {0: "Utility", 1: "Non-Utility"}

def categorize_transaction(description):
    """
    Classify a transaction as Utility or Non-Utility based on its description.
    """
    # Tokenize the input description
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)

    # Get predictions from the model
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()

    # Map the predicted label to its corresponding category
    return LABELS[predicted_label]




