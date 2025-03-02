import os
from dotenv import load_dotenv

# added security patches

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
    BCRYPT_SALT_ROUNDS = int(os.getenv('BCRYPT_SALT_ROUNDS'))
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT')
    MONGO_URI = os.getenv('MONGO_URI')
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL')
    MONGO_URI = os.getenv('MONGO_URI')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    MONGO_URI = os.getenv('MONGO_URI')
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL')
    MONGO_URI = os.getenv('MONGO_URI')
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}