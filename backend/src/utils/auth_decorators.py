"""
Authentication decorators and middleware
"""

from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import logging

logger = logging.getLogger(__name__)

def token_required(f):
    """
    Decorator to require valid JWT token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Token verification failed: {e}")
            return jsonify({"error": "Invalid or missing token"}), 401
    return decorated

def admin_required(f):
    """
    Decorator to require admin role
    """
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        try:
            current_user_id = get_jwt_identity()
            from src.models.user import User
            user = User.query.get(current_user_id)
            
            if not user or user.role != 'admin':
                return jsonify({"error": "Admin access required"}), 403
            
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Admin check failed: {e}")
            return jsonify({"error": "Access denied"}), 403
    return decorated

def optional_auth(f):
    """
    Decorator for endpoints that work with or without authentication
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request(optional=True)
        except Exception:
            pass  # Continue without authentication
        return f(*args, **kwargs)
    return decorated

def rate_limit(requests_per_minute=60):
    """
    Simple rate limiting decorator
    Note: This is a basic implementation. For production, use Flask-Limiter
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Basic rate limiting logic could be implemented here
            # For now, just pass through
            return f(*args, **kwargs)
        return decorated
    return decorator

def validate_file_upload(f):
    """
    Decorator to validate file uploads
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Check file extension
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', ['.pdf'])
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            return jsonify({"error": f"Only {', '.join(allowed_extensions)} files are allowed"}), 400
        
        # Check file size
        max_size = current_app.config.get('MAX_CONTENT_LENGTH', 25 * 1024 * 1024)  # 25MB default
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > max_size:
            return jsonify({"error": f"File too large. Maximum size is {max_size // (1024*1024)}MB"}), 413
        
        return f(*args, **kwargs)
    return decorated