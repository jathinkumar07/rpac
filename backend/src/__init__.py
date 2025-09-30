from flask import Flask
import os
import logging
from config import Config
from src.extensions import init_extensions
from src.routes import register_blueprints

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)
    os.makedirs(app.config['REPORT_DIR'], exist_ok=True)
    os.makedirs(app.config['CORPUS_DIR'], exist_ok=True)
    
    # Initialize extensions
    init_extensions(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Add error handlers
    @app.errorhandler(413)
    def too_large(e):
        from flask import jsonify
        return jsonify({"error": "File too large. Maximum size is 25MB."}), 413
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {e}")
        from flask import jsonify
        return jsonify({"error": "Internal server error occurred"}), 500
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        from flask import jsonify
        return jsonify({
            "status": "success",
            "message": "Research Paper Analysis API is running"
        }), 200
    
    @app.route('/', methods=['GET'])
    def root():
        from flask import jsonify
        return jsonify({
            "status": "success",
            "message": "Research Paper Analysis API",
            "version": "2.0.0"
        }), 200
    
    logger.info("Flask application created successfully")
    return app