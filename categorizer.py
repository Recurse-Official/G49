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
    0: "AABE-FA",
    1: "ALDI",
    2: "ALLIANZ",
    3: "AMAZON",
    4: "APPLE",
    5: "AUCHAN",
    6: "BOULANGER",
    7: "BOUYGUES TELECOM",
    8: "CARBURANT",
    9: "CARREFOUR",
    10: "CARTE BLEUE",
    11: "CASTORAMA",
    12: "COMPTOIRS OCEANIQUES",
    13: "DARTY",
    14: "DAUCHEZ ADMINISTRATEUR DE BIENS SA",
    15: "E.LECLERC",
    16: "EDENKIA",
    17: "EDENRED FRANCE",
    18: "EDF",
    19: "ENGIE",
    20: "FACEBOOK IRELAND LIMITED",
    21: "FIDUCIAIRE DU VAL D'EUROPE",
    22: "FNAC",
    23: "FOODEX",
    24: "FRAIS BANCAIRES",
    25: "FREE",
    26: "GOOGLE",
    27: "GRAND FRAIS",
    28: "HBO EXPERTISE",
    29: "HOTEL",
    30: "IKEA",
    31: "INTERMARCHE",
    32: "LA POSTE",
    33: "LA SHUNDE",
    34: "LEROY MERLIN",
    35: "LIDL",
    36: "LOYER",
    37: "LX FRANCE",
    38: "METRO",
    39: "NESPRESSO",
    40: "ORANGE",
    41: "OVH",
    42: "PARIS STORE",
    43: "PARKING",
    44: "PEAGE",
    45: "POMONA",
    46: "PROMOCASH",
    47: "RESTAURANT",
    48: "REYNAUD",
    49: "SARL B.L AUDIT",
    50: "SFR",
    51: "SNCF",
    52: "TANG FRERES",
    53: "TAXI",
    54: "TOTALENERGIES",
    55: "TRANSPORT",
    56: "UBER EATS",
    57: "WENG",
    58: "XIONG HAI"
}

CATEGORY_MAPPING = {
    "Utility": [
        "EDF", "ENGIE", "FREE", "SFR", "ORANGE", "PARKING", "TAXI", "TRANSPORT", "TOTALENERGIES",
        "PEAGE", "CARBURANT", "LOYER", "HOTEL", "E.LECLERC", "AUCHAN", "CARREFOUR", "INTERMARCHE",
        "GRAND FRAIS", "METRO", "PARIS STORE", "TANG FRERES"
    ],
    "Non-Utility": [
        "AMAZON", "IKEA", "RESTAURANT", "UBER EATS", "NESPRESSO", "APPLE", "FACEBOOK IRELAND LIMITED",
        "GOOGLE", "FNAC", "BOULANGER", "DARTY", "LEROY MERLIN", "CASTORAMA", "PROMOCASH", "FOODEX",
        "ALDI", "LIDL", "OVH", "AABE-FA", "DAUCHEZ ADMINISTRATEUR DE BIENS SA", "EDENKIA",
        "EDENRED FRANCE", "COMPTOIRS OCEANIQUES", "FIDUCIAIRE DU VAL D'EUROPE", "HBO EXPERTISE",
        "SARL B.L AUDIT", "REYNAUD", "WENG", "XIONG HAI", "LA POSTE", "LA SHUNDE", "LX FRANCE"
    ]
}

def map_to_category(label):
    """
    Map detailed label to Utility or Non-Utility.
    """
    for category, labels in CATEGORY_MAPPING.items():
        if label in labels:
            return category
    return "Unknown"

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
    detailed_label = LABELS.get(predicted_label, f"Unknown (Label: {predicted_label})")
    print(f"Predicted detailed label: {detailed_label}")
    category = map_to_category(detailed_label)

    return category






