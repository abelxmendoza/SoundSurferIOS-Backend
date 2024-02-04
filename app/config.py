import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

class DevelopmentConfig(Config):
    DEBUG = True
    # Add other development specific settings

class ProductionConfig(Config):
    DEBUG = False
    # Add other production specific settings

# Add other configuration classes if needed
