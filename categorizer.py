import spacy
import pickle

# Load SpaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Categories for classification
categories = {
    "utilities": ["rent", "electricity", "water", "gas", "internet"],
    "non-utilities": ["shopping", "movies", "dining", "luxury", "travel"]
}

# Load or initialize a dynamic feedback store
try:
    with open("feedback.pkl", "rb") as f:
        feedback_data = pickle.load(f)
except FileNotFoundError:
    feedback_data = {}

# Categorization function
def categorize_transaction(description):
    tokens = [token.text.lower() for token in nlp(description)]
    for category, keywords in categories.items():
        if any(token in keywords for token in tokens):
            sub_category = next((token for token in tokens if token in keywords), "general")
            return category, sub_category

    # Fallback to user feedback if available
    for token in tokens:
        if token in feedback_data:
            return feedback_data[token]
    return "unknown", "unknown"

# Update feedback data and save it
def update_feedback(description, category, sub_category):
    tokens = [token.text.lower() for token in nlp(description)]
    for token in tokens:
        feedback_data[token] = (category, sub_category)
    with open("feedback.pkl", "wb") as f:
        pickle.dump(feedback_data, f)
