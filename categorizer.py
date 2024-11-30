from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json

MODEL_NAME = "moctarsmal/bank-transactions-statements-classification"
VOCAB_PATH = "C:/Users/K TEJASWI/Downloads/corrected_tokenizer/vocab.json"

# Load the corrected vocab.json
with open(VOCAB_PATH, "r", encoding="utf-8") as f:
    vocab = json.load(f)

# Load the tokenizer and set special tokens
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=False
)

# Explicitly add special tokens
special_tokens = {
    "bos_token": "<s>",
    "eos_token": "</s>",
    "pad_token": "<pad>",
    "unk_token": "<unk>",
    "additional_special_tokens": ["<special0>", "<special1>", "<special2>", "<special3>", "<special4>"]
}
tokenizer.add_special_tokens(special_tokens)

# Load the model and resize embeddings to match the updated tokenizer
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.resize_token_embeddings(len(tokenizer))

# Mapping model output to categories
LABELS = {0: "Utility", 1: "Non-Utility"}

def categorize_transaction(description):
    """
    Classify a transaction as Utility or Non-Utility based on its description.
    """
    inputs = tokenizer(description, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_label = torch.argmax(outputs.logits, dim=1).item()
    return LABELS[predicted_label]





