from flask import Flask, request, jsonify
from categorizer import categorize_transaction, update_feedback

app = Flask(__name__)

# User budgets
user_budgets = {"utilities": 0, "non-utilities": 0}
user_spending = {"utilities": 0, "non-utilities": 0}

@app.route("/set_budget", methods=["POST"])
def set_budget():
    data = request.get_json()
    user_budgets["utilities"] = data.get("utilities", 0)
    user_budgets["non-utilities"] = data.get("non_utilities", 0)
    return jsonify({"message": "Budgets set successfully"}), 200

@app.route("/categorize", methods=["POST"])
def categorize():
    data = request.get_json()
    description = data.get("description", "")
    amount = data.get("amount", 0)

    if not description:
        return jsonify({"error": "No description provided"}), 400

    category, sub_category = categorize_transaction(description)
    user_spending[category] += amount

    # Check for budget warnings
    if user_spending[category] > user_budgets[category]:
        warning = f"Warning: You have exceeded your budget for {category}!"
    else:
        warning = f"You are within your budget for {category}."

    return jsonify({"category": category, "sub_category": sub_category, "warning": warning})

@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json()
    description = data.get("description", "")
    category = data.get("category", "")
    sub_category = data.get("sub_category", "")

    if not description or not category:
        return jsonify({"error": "Incomplete feedback provided"}), 400

    update_feedback(description, category, sub_category)
    return jsonify({"message": "Feedback received and model updated"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
