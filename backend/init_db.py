#!/usr/bin/env python3
"""
Database initialization script for Research Critic application.
This script creates all database tables and can optionally create a sample admin user.
"""

import os
import sys
from getpass import getpass

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import create_app
from src.extensions import db
from src.models import User, Document, Analysis


def init_database():
    """Initialize the database with all tables."""
    app = create_app()
    
    # Print configuration info
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    with app.app_context():
        print("Creating database tables...")
        try:
            # Ensure the directory exists
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            db.create_all()
            print("✓ Database tables created successfully!")
            
            # Check if any users exist
            user_count = User.query.count()
            print(f"Current user count: {user_count}")
            
            if user_count == 0:
                create_admin = input("No users found. Would you like to create an admin user? (y/N): ").lower().strip()
                if create_admin == 'y':
                    create_admin_user()
        except Exception as e:
            print(f"Error creating database: {e}")
            return False
        
        return True


def create_admin_user():
    """Create an admin user interactively."""
    print("\n--- Creating Admin User ---")
    
    name = input("Enter admin name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return False
    
    email = input("Enter admin email: ").strip()
    if not email:
        print("Email cannot be empty!")
        return False
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        print(f"User with email {email} already exists!")
        return False
    
    password = getpass("Enter admin password: ")
    if len(password) < 6:
        print("Password must be at least 6 characters!")
        return False
    
    confirm_password = getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords don't match!")
        return False
    
    try:
        # Create admin user
        admin_user = User(name=name, email=email, role='admin')
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"✓ Admin user '{name}' created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.session.rollback()
        return False


def reset_database():
    """Reset the database by dropping and recreating all tables."""
    app = create_app()
    
    with app.app_context():
        print("WARNING: This will delete all existing data!")
        confirm = input("Are you sure you want to reset the database? (y/N): ").lower().strip()
        
        if confirm == 'y':
            print("Dropping all tables...")
            db.drop_all()
            print("Creating new tables...")
            db.create_all()
            print("✓ Database reset successfully!")
            
            create_admin = input("Would you like to create an admin user? (y/N): ").lower().strip()
            if create_admin == 'y':
                create_admin_user()
        else:
            print("Database reset cancelled.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()