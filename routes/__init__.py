# backend/routes/__init__.py
from .auth import auth_bp
from .budget import budget_bp
from .transaction import transaction_bp
from .categories import categories_bp

def initialize_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(budget_bp, url_prefix='/budget')
    app.register_blueprint(transaction_bp, url_prefix='/transactions')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    # Register other blueprints as needed
