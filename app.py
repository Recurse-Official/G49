# backend/app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes import initialize_routes
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)
    
    initialize_routes(app)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
