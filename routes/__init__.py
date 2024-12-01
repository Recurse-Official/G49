# backend/routes/__init__.py
from .auth import auth_bp
from .budget import budget_bp
from .transactions import transactions_bp
from .plaid import plaid_bp
from .leaderboard import leaderboard_bp
from .categories import categories_bp

def initialize_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(budget_bp, url_prefix='/budget')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(plaid_bp, url_prefix='/plaid')
    app.register_blueprint(leaderboard_bp, url_prefix='/leaderboard')
    # Register other blueprints as needed
