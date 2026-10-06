import os

class Config():
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mad2_project_db.sqlite3'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt_here'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Tells Flask-Security to use bcrypt algorithm

    SECURITY_TOKEN_AUTHENTICATION_ENABLED = True