# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    utilities_budget = db.Column(db.Float, default=0.0)
    non_utilities_budget = db.Column(db.Float, default=0.0)
    remaining_utilities = db.Column(db.Float, default=0.0)
    remaining_non_utilities = db.Column(db.Float, default=0.0)
    # Additional fields as needed

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'utility' or 'non-utility'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_utilities = db.Column(db.Boolean, nullable=True)  # Determined by backend logic

class Reward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=0)
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    discount = db.Column(db.Float, nullable=False)
    expiration_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key to User

    user = db.relationship('User', back_populates='offers')  # Establishing the relationship with User

    def __repr__(self):
        return f'<Offer {self.title}>'

# Add a back reference in User model to establish the reverse relationship
User.offers = db.relationship('Offer', back_populates='user', lazy=True
