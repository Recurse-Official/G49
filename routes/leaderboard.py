# backend/routes/leaderboard.py
from flask import Blueprint, jsonify
from models import db, User, Reward
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/update_rewards', methods=['POST'])
@jwt_required()
def update_rewards():
    # This could be a scheduled task instead
    users = User.query.all()
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year

    for user in users:
        # Simple logic: if remaining budget is positive, award points
        points = 0
        if user.remaining_utilities >= 0 and user.remaining_non_utilities >= 0:
            points += 10  # Example points
        # Update or create Reward
        reward = Reward.query.filter_by(user_id=user.id, month=current_month, year=current_year).first()
        if not reward:
            reward = Reward(user_id=user.id, month=current_month, year=current_year, points=points)
            db.session.add(reward)
        else:
            reward.points += points
    db.session.commit()
    return jsonify({"msg": "Rewards updated"}), 200

@leaderboard_bp.route('/get_leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().year
    rewards = Reward.query.filter_by(month=current_month, year=current_year).order_by(Reward.points.desc()).all()
    leaderboard = []
    for reward in rewards:
        user = User.query.get(reward.user_id)
        leaderboard.append({
            "username": user.username,
            "points": reward.points
        })
    return jsonify(leaderboard), 200
