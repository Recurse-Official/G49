from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.plaid_client import get_plaid_client
from models import User, db  # Ensure User and db are imported
from my_ml_model import categorize_transaction  # Import your ML model's function

plaid_bp = Blueprint('plaid', __name__)

@plaid_bp.route('/create_link_token', methods=['POST'])
@jwt_required()
def create_link_token():
    user_id = get_jwt_identity()
    client = get_plaid_client()
    response = client.LinkToken.create({
        'user': {'client_user_id': str(user_id)},
        'client_name': 'Budget App',
        'products': ['transactions'],
        'country_codes': ['US'],
        'language': 'en',
    })
    return jsonify(response), 200

@plaid_bp.route('/exchange_public_token', methods=['POST'])
@jwt_required()
def exchange_public_token():
    user_id = get_jwt_identity()
    client = get_plaid_client()
    data = request.get_json()
    public_token = data.get('public_token')
    exchange_response = client.Item.public_token.exchange(public_token)
    access_token = exchange_response['access_token']
    # Store access_token securely associated with the user
    user = User.query.get(user_id)
    user.plaid_access_token = access_token
    db.session.commit()
    return jsonify({"msg": "Access token stored"}), 200

@plaid_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    client = get_plaid_client()
    user = User.query.get(user_id)
    access_token = user.plaid_access_token
    response = client.Transactions.get(
        access_token,
        start_date='2023-01-01',
        end_date='2023-12-31'
    )
    return jsonify(response), 200

@plaid_bp.route('/categorize_transactions', methods=['POST'])
@jwt_required()
def categorize_transactions():
    """
    Fetch transactions from Plaid, categorize them using the ML model, and return the results.
    """
    user_id = get_jwt_identity()
    client = get_plaid_client()
    user = User.query.get(user_id)
    access_token = user.plaid_access_token

    try:
        # Fetch transactions from Plaid
        response = client.Transactions.get(
            access_token,
            start_date='2023-01-01',
            end_date='2023-12-31'
        )
        transactions = response['transactions']

        # Process and categorize transactions
        categorized_transactions = []
        for txn in transactions:
            description = txn.get('name', '')
            amount = txn.get('amount', 0)

            # Call your ML model to categorize the transaction
            category = categorize_transaction(description)  # Your ML model's function

            categorized_transactions.append({
                "description": description,
                "amount": amount,
                "category": category
            })

        return jsonify(categorized_transactions), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

