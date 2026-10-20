import os

class Config():
    SECRET_KEY = 'your_secret_key_here'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///mad2_project_db.sqlite3'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///mad2_project_tma_db.sqlite3'


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt_here'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Tells Flask-Security to use bcrypt algorithm

    SECURITY_TOKEN_AUTHENTICATION_ENABLED = True


    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

    CELERY_TIMEZONE = "Asia/Kolkata"
    CELERY_ENABLE_UTC = True