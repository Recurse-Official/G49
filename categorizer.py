from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the pretrained model and tokenizer
MODEL_NAME = "moctarsmal/bank-transactions-statements-classification"

# Initialize tokenizer with explicitly defined special tokens
tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=False,
    bos_token="<s>",
    eos_token="</s>",
    pad_token="<pad>",
    unk_token="<unk>"
)

# Add additional special tokens explicitly (if needed)
additional_special_tokens = ["<special0>", "<special1>", "<special2>", "<special3>", "<special4>"]
tokenizer.add_special_tokens({"additional_special_tokens": additional_special_tokens})

# Load the model and resize embeddings to accommodate the added tokens
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.resize_token_embeddings(len(tokenizer))

# Mapping model output to categories
LABELS = {
    0: "Utility",
    1: "Non-Utility"
}

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



