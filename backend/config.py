import os

class Config():
    SECRET_KEY = 'your_secret_key_here'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///mad2_project_db.sqlite3'
    SQLALCHEMY_DATABASE_URI = (
        'sqlite:///' + os.path.join(
            BASE_DIR, 'instance', 'mad2_project_tma_db.sqlite3')
        )


    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'your_password_salt_here'

    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    SECURITY_PASSWORD_HASH = 'bcrypt'  # Tells Flask-Security to use bcrypt algorithm

    SECURITY_TOKEN_AUTHENTICATION_ENABLED = True

    CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/1"

    CELERY_TIMEZONE = "Asia/Kolkata"
    CELERY_ENABLE_UTC = True

    # Email configuration for trek reminders
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = os.getenv("TMS_MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("TMS_MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("TMS_MAIL_USERNAME")

    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_HOST = '127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 2
    CACHE_DEFAULT_TIMEOUT = 300 # 5 MIN


