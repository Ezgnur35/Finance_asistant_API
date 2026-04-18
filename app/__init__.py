from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.transactions import transactions_bp
    from app.routes.categories import categories_bp
    from app.routes.reports import reports_bp
    from app.routes.limits import limits_bp
    from app.routes.goals import goals_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(limits_bp)
    app.register_blueprint(goals_bp)

    return app