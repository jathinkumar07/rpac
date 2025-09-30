from flask import Blueprint
from .auth import auth_bp
from .protected_analyze import protected_analyze_bp
from .simple_analyze import simple_analyze_bp

def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(protected_analyze_bp, url_prefix='/api/protected')
    app.register_blueprint(simple_analyze_bp, url_prefix='/api')