# backend/routes/transaction.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Transaction, Category, User
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Retrieve all transactions for the authenticated user.
    Supports optional filtering by category, start_date, and end_date.
    """
    user_id = get_jwt_identity()
    category_id = request.args.get('category_id')
    start_date = request.args.get('start_date')  # Format: YYYY-MM-DD
    end_date = request.args.get('end_date')      # Format: YYYY-MM-DD

    query = Transaction.query.filter_by(user_id=user_id)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if start_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Transaction.date >= start)
        except ValueError:
            return jsonify({"msg": "Invalid start_date format. Use YYYY-MM-DD"}), 400

    if end_date:
        try:
            end = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Transaction.date <= end)
        except ValueError:
            return jsonify({"msg": "Invalid end_date format. Use YYYY-MM-DD"}), 400

    transactions = query.order_by(Transaction.date.desc()).all()
    transactions_list = [
        {
            "id": txn.id,
            "amount": txn.amount,
            "category_id": txn.category_id,
            "date": txn.date.strftime('%Y-%m-%d'),
            "is_utilities": txn.is_utilities
        } for txn in transactions
    ]
    return jsonify(transactions_list), 200

@transactions_bp.route('/', methods=['POST'])
@jwt_required()
def add_transaction():
    """
    Add a new transaction for the authenticated user.
    Expected JSON payload:
    {
        "amount": 50.0,
        "category_id": 1,  # Must exist
        "date": "2024-12-01"  # Optional; defaults to current date
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    amount = data.get('amount')
    category_id = data.get('category_id')
    date_str = data.get('date')

    # Validate amount
    if amount is None:
        return jsonify({"msg": "Amount is required"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"msg": "Amount must be positive"}), 400
    except ValueError:
        return jsonify({"msg": "Invalid amount format"}), 400

    # Validate category
    if category_id:
        category = Category.query.filter_by(id=category_id, user_id=user_id).first()
        if not category:
            return jsonify({"msg": "Category not found"}), 404
        is_utilities = True if category.type == 'utility' else False
    else:
        return jsonify({"msg": "Category ID is required"}), 400

    # Validate date
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400
    else:
        date = datetime.utcnow()

    # Fetch user to update budget
    user = User.query.get(user_id)
    if is_utilities:
        if user.remaining_utilities < amount:
            warning = "This payment is crossing your utilities budget!"
        else:
            warning = ""
        user.remaining_utilities -= amount
    else:
        if user.remaining_non_utilities < amount:
            warning = "This payment is crossing your non-utilities budget!"
        else:
            warning = ""
        user.remaining_non_utilities -= amount

    # Create and add new transaction
    new_transaction = Transaction(
        amount=amount,
        category_id=category_id,
        date=date,
        user_id=user_id,
        is_utilities=is_utilities
    )

    db.session.add(new_transaction)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error adding transaction"}), 500

    return jsonify({
        "msg": "Transaction added successfully",
        "transaction": {
            "id": new_transaction.id,
            "amount": new_transaction.amount,
            "category_id": new_transaction.category_id,
            "date": new_transaction.date.strftime('%Y-%m-%d'),
            "is_utilities": new_transaction.is_utilities
        },
        "warning": warning
    }), 201

@transactions_bp.route('/<int:transaction_id>', methods=['PUT'])
@jwt_required()
def update_transaction(transaction_id):
    """
    Update an existing transaction.
    Expected JSON payload can include 'amount', 'category_id', and/or 'date'.
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({"msg": "Transaction not found"}), 404

    original_amount = transaction.amount
    original_is_utilities = transaction.is_utilities

    # Update fields if provided
    amount = data.get('amount')
    category_id = data.get('category_id')
    date_str = data.get('date')

    if amount is not None:
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({"msg": "Amount must be positive"}), 400
        except ValueError:
            return jsonify({"msg": "Invalid amount format"}), 400
        transaction.amount = amount

    if category_id is not None:
        category = Category.query.filter_by(id=category_id, user_id=user_id).first()
        if not category:
            return jsonify({"msg": "Category not found"}), 404
        transaction.category_id = category_id
        transaction.is_utilities = True if category.type == 'utility' else False

    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            transaction.date = date
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Fetch user to update budget
    user = User.query.get(user_id)

    # Revert original budget
    if original_is_utilities:
        user.remaining_utilities += original_amount
    else:
        user.remaining_non_utilities += original_amount

    # Apply new budget
    if transaction.is_utilities:
        if user.remaining_utilities < transaction.amount:
            warning = "This payment is crossing your utilities budget!"
        else:
            warning = ""
        user.remaining_utilities -= transaction.amount
    else:
        if user.remaining_non_utilities < transaction.amount:
            warning = "This payment is crossing your non-utilities budget!"
        else:
            warning = ""
        user.remaining_non_utilities -= transaction.amount

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error updating transaction"}), 500

    return jsonify({
        "msg": "Transaction updated successfully",
        "transaction": {
            "id": transaction.id,
            "amount": transaction.amount,
            "category_id": transaction.category_id,
            "date": transaction.date.strftime('%Y-%m-%d'),
            "is_utilities": transaction.is_utilities
        },
        "warning": warning
    }), 200

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
@jwt_required()
def delete_transaction(transaction_id):
    """
    Delete a transaction.
    """
    user_id = get_jwt_identity()
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    if not transaction:
        return jsonify({"msg": "Transaction not found"}), 404

    # Fetch user to update budget
    user = User.query.get(user_id)
    if transaction.is_utilities:
        user.remaining_utilities += transaction.amount
    else:
        user.remaining_non_utilities += transaction.amount

    db.session.delete(transaction)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error deleting transaction"}), 500

    return jsonify({"msg": "Transaction deleted successfully"}), 200

@transactions_bp.route('/scan', methods=['POST'])
@jwt_required()
def scan_transaction():
    """
    Handle scanned transaction data.
    Expected JSON payload:
    {
        "scanned_data": "{\"amount\": 50.0, \"category\": \"Electricity Bill\"}"
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    scanned_data = data.get('scanned_data')

    if not scanned_data:
        return jsonify({"msg": "No scanned data provided"}), 400

    try:
        # Assuming scanned_data is a JSON string with 'amount' and 'category'
        transaction_info = json.loads(scanned_data)
        amount = transaction_info.get('amount')
        category_name = transaction_info.get('category')
    except json.JSONDecodeError:
        return jsonify({"msg": "Invalid scanned data format"}), 400

    if amount is None or category_name is None:
        return jsonify({"msg": "Scanned data must include 'amount' and 'category'"}), 400

    try:
        amount = float(amount)
        if amount <= 0:
            return jsonify({"msg": "Amount must be positive"}), 400
    except ValueError:
        return jsonify({"msg": "Invalid amount format"}), 400

    # Retrieve category by name
    category = Category.query.filter_by(name=category_name, user_id=user_id).first()
    if not category:
        return jsonify({"msg": "Category not found"}), 404

    is_utilities = True if category.type == 'utility' else False

    # Fetch user to update budget
    user = User.query.get(user_id)
    if is_utilities:
        if user.remaining_utilities < amount:
            warning = "This payment is crossing your utilities budget!"
        else:
            warning = ""
        user.remaining_utilities -= amount
    else:
        if user.remaining_non_utilities < amount:
            warning = "This payment is crossing your non-utilities budget!"
        else:
            warning = ""
        user.remaining_non_utilities -= amount

    # Create and add new transaction
    new_transaction = Transaction(
        amount=amount,
        category_id=category.id,
        date=datetime.utcnow(),
        user_id=user_id,
        is_utilities=is_utilities
    )

    db.session.add(new_transaction)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error processing transaction"}), 500

    return jsonify({
        "msg": "Transaction recorded",
        "transaction": {
            "id": new_transaction.id,
            "amount": new_transaction.amount,
            "category_id": new_transaction.category_id,
            "date": new_transaction.date.strftime('%Y-%m-%d'),
            "is_utilities": new_transaction.is_utilities
        },
        "warning": warning
    }), 201
