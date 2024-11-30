# backend/routes/categories.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Category
from sqlalchemy.exc import IntegrityError

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
@jwt_required()
def get_categories():
    """
    Retrieve all categories for the authenticated user.
    """
    user_id = get_jwt_identity()
    categories = Category.query.filter_by(user_id=user_id).all()
    categories_list = [
        {
            "id": category.id,
            "name": category.name,
            "type": category.type
        } for category in categories
    ]
    return jsonify(categories_list), 200

@categories_bp.route('/', methods=['POST'])
@jwt_required()
def add_category():
    """
    Add a new category for the authenticated user.
    Expected JSON payload:
    {
        "name": "Electricity Bill",
        "type": "utility"
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    name = data.get('name')
    type_ = data.get('type')

    # Validate input
    if not name or not type_:
        return jsonify({"msg": "Name and type are required"}), 400

    if type_ not in ['utility', 'non-utility']:
        return jsonify({"msg": "Type must be 'utility' or 'non-utility'"}), 400

    # Check for duplicate category
    existing_category = Category.query.filter_by(name=name, user_id=user_id).first()
    if existing_category:
        return jsonify({"msg": "Category already exists"}), 409

    # Create and add new category
    new_category = Category(name=name, type=type_, user_id=user_id)
    db.session.add(new_category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error adding category"}), 500

    return jsonify({
        "msg": "Category added successfully",
        "category": {
            "id": new_category.id,
            "name": new_category.name,
            "type": new_category.type
        }
    }), 201

@categories_bp.route('/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """
    Update an existing category.
    Expected JSON payload can include 'name' and/or 'type'.
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if not category:
        return jsonify({"msg": "Category not found"}), 404

    name = data.get('name')
    type_ = data.get('type')

    # Update fields if provided
    if name:
        category.name = name
    if type_:
        if type_ not in ['utility', 'non-utility']:
            return jsonify({"msg": "Type must be 'utility' or 'non-utility'"}), 400
        category.type = type_

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error updating category"}), 500

    return jsonify({
        "msg": "Category updated successfully",
        "category": {
            "id": category.id,
            "name": category.name,
            "type": category.type
        }
    }), 200

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """
    Delete a category.
    """
    user_id = get_jwt_identity()
    category = Category.query.filter_by(id=category_id, user_id=user_id).first()
    if not category:
        return jsonify({"msg": "Category not found"}), 404

    db.session.delete(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Error deleting category"}), 500

    return jsonify({"msg": "Category deleted successfully"}), 200
