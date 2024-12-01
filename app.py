# backend/app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes import initialize_routes
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)

    initialize_routes(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
