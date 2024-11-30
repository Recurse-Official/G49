from flask import Flask, request, jsonify
from categorizer import categorize_transaction

app = Flask(__name__)

# Budget and spending tracking
user_budgets = {"Utility": 0, "Non-Utility": 0}
user_spending = {"Utility": 0, "Non-Utility": 0}

@app.route("/set_budget", methods=["POST"])
def set_budget():
    """
    Set user budgets for utilities and non-utilities.
    """
    try:
        data = request.get_json()
        user_budgets["Utility"] = data.get("utility", 0)
        user_budgets["Non-Utility"] = data.get("non_utility", 0)

        return jsonify({"message": "Budgets set successfully", "budgets": user_budgets}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/categorize", methods=["POST"])
def categorize():
    """
    Categorize a transaction description and check budget.
    """
    try:
        # Parse incoming JSON data
        data = request.get_json()
        description = data.get("description", "")
        amount = data.get("amount", 0)

        if not description:
            return jsonify({"error": "Description is required"}), 400
        if amount <= 0:
            return jsonify({"error": "Transaction amount must be greater than zero"}), 400
        print(f"received description : {description}, amount :{amount}")

        # Get the category of the transaction
        category = categorize_transaction(description)

        # Update spending and check budget
        user_spending[category] += amount
        warning = None

        if user_spending[category] > user_budgets[category]:
            warning = f"Warning: You have exceeded your budget for {category}!"

        # Response
        response = {
            "description": description,
            "category": category,
            "amount": amount,
            "current_spending": user_spending[category],
            "budget": user_budgets[category],
            "warning": warning
        }
        print(f"Response; {response}")
        return jsonify(response), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

