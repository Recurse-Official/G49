# backend/routes/offers.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Offer, User  # Make sure to have Offer model in models.py

# Define the blueprint for offers
offers_bp = Blueprint('offers', __name__)

@offers_bp.route('/', methods=['GET'])
@jwt_required()
def get_offers():
    """
    Retrieve all offers for the authenticated user.
    """
    user_id = get_jwt_identity()
    
    # Fetch the user's offers from the database
    offers = Offer.query.filter_by(user_id=user_id).all()

    offers_list = [
        {
            "id": offer.id,
            "title": offer.title,
            "description": offer.description,
            "discount": offer.discount,
            "expiration_date": offer.expiration_date.strftime('%Y-%m-%d') if offer.expiration_date else None
        } for offer in offers
    ]
    
    return jsonify(offers_list), 200


@offers_bp.route('/', methods=['POST'])
@jwt_required()
def add_offer():
    """
    Add a new offer for the authenticated user.
    Expected JSON payload:
    {
        "title": "Summer Sale",
        "description": "Get 50% off on all items",
        "discount": 50.0,
        "expiration_date": "2024-12-31"
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    title = data.get('title')
    description = data.get('description')
    discount = data.get('discount')
    expiration_date_str = data.get('expiration_date')

    # Validate inputs
    if not title or not description or discount is None:
        return jsonify({"msg": "Title, description, and discount are required"}), 400

    try:
        discount = float(discount)
        if discount <= 0:
            return jsonify({"msg": "Discount must be a positive number"}), 400
    except ValueError:
        return jsonify({"msg": "Invalid discount format"}), 400

    if expiration_date_str:
        try:
            expiration_date = datetime.strptime(expiration_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"msg": "Invalid expiration_date format. Use YYYY-MM-DD"}), 400
    else:
        expiration_date = None

    # Create and save new offer
    new_offer = Offer(
        title=title,
        description=description,
        discount=discount,
        expiration_date=expiration_date,
        user_id=user_id
    )

    db.session.add(new_offer)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error adding offer", "error": str(e)}), 500

    return jsonify({
        "msg": "Offer added successfully",
        "offer": {
            "id": new_offer.id,
            "title": new_offer.title,
            "description": new_offer.description,
            "discount": new_offer.discount,
            "expiration_date": new_offer.expiration_date.strftime('%Y-%m-%d') if new_offer.expiration_date else None
        }
    }), 201
