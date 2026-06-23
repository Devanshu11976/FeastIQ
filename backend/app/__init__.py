from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, jwt, migrate
from app.routes.auth import auth_bp
from app.routes.menu import menu_bp
from app.routes.orders import orders_bp
from app.routes.feedback import feedback_bp
from app.routes.analytics import analytics_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(menu_bp, url_prefix='/menu')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(feedback_bp, url_prefix='/feedback')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    
    return app
