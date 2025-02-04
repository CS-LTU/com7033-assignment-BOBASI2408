import os
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default-jwt-secret-key')
    BCRYPT_SALT_ROUNDS = int(os.getenv('BCRYPT_SALT_ROUNDS', 12))
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100/day;10/minute')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://jacobasuquo199:4e55kZKS4Dzwz7fJ@cluster0.e2rno.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL', 'sqlite:///database/sqlite/patient.db')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://jacobasuquo199:4e55kZKS4Dzwz7fJ@cluster0.e2rno.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    MONGO_URI = 'mongodb+srv://jacobasuquo199:4e55kZKS4Dzwz7fJ@cluster0.e2rno.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLITE_DATABASE_URL', 'sqlite:///database/sqlite/patient.db')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://jacobasuquo199:4e55kZKS4Dzwz7fJ@cluster0.e2rno.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}