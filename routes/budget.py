# backend/routes/budget.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User

budget_bp = Blueprint('budget', __name__)

@budget_bp.route('/set', methods=['POST'])
@jwt_required()
def set_budget():
    user_id = get_jwt_identity()
    data = request.get_json()
    utilities_budget = data.get('utilities_budget')
    non_utilities_budget = data.get('non_utilities_budget')

    user = User.query.get(user_id)
    user.utilities_budget = utilities_budget
    user.non_utilities_budget = non_utilities_budget
    user.remaining_utilities = utilities_budget
    user.remaining_non_utilities = non_utilities_budget

    db.session.commit()

    return jsonify({"msg": "Budget set successfully"}), 200
