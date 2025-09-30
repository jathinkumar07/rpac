#!/usr/bin/env python3
"""
Research Paper Analysis API - Main Application

This is the main entry point for the Research Paper Analysis API.
It uses the restructured modular architecture with proper authentication,
database integration, and service separation.
"""

import os
import logging
from flask import Flask
from src import create_app
from src.extensions import db
from src.models import user, document, analysis, citation

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    # Create Flask app using application factory
    app = create_app()
    
    # Create database tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
    
    # Get configuration
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    logger.info(f"Starting Research Paper Analysis API")
    logger.info(f"Server: http://{host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'development')}")
    
    # Start the server
    try:
        app.run(
            host=host,
            port=port,
            debug=debug,
            threaded=True
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == '__main__':
    main()
