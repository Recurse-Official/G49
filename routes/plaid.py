# backend/routes/plaid.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.plaid_client import get_plaid_client

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
    # e.g., save to User model
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
