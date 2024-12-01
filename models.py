from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from enum import Enum

db = SQLAlchemy()

# Enum for predefined categories (optional)
class CategoryType(Enum):
    GROCERY = "Groceries"
    TRANSPORT = "Transport"
    ENTERTAINMENT = "Entertainment"
    MISC = "Miscellaneous"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    utilities_budget = db.Column(db.Float, default=0.0)
    non_utilities_budget = db.Column(db.Float, default=0.0)
    remaining_utilities = db.Column(db.Float, default=0.0)
    remaining_non_utilities = db.Column(db.Float, default=0.0)
    categories = db.relationship('Category', backref='user', lazy=True, cascade="all, delete-orphan")
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade="all, delete-orphan")
    rewards = db.relationship('Reward', backref='user', lazy=True, cascade="all, delete-orphan")
    offers = db.relationship('Offer', back_populates='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'utility' or 'non-utility'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transactions = db.relationship('Transaction', backref='category', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Category {self.name}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)  # Reference to Category
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_utilities = db.Column(db.Boolean, nullable=True)  # Determined by backend logic
    category_name = db.Column(db.String(100), nullable=True)  # Store category name (e.g., from ML model)

    category = db.relationship('Category', backref='transactions', lazy=True)

    def __repr__(self):
        return f'<Transaction {self.id}, {self.category_name}>'

class Reward(db.Model):
    __tablename__ = 'rewards'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Reward {self.user_id}, {self.month} {self.year}>'

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
User.offers = db.relationship('Offer', back_populates='user', lazy=True)


