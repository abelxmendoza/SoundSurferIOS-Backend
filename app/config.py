import os


class Config(object):
    # General configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'

class DevelopmentConfig(Config):
    # Development-specific configuration
    DEBUG = True
    MYSQL_DATABASE_USER = os.environ.get('DEV_MYSQL_USER') or 'dev_user'
    MYSQL_DATABASE_PASSWORD = os.environ.get('DEV_MYSQL_PASSWORD') or 'dev_password'
    MYSQL_DATABASE_DB = os.environ.get('DEV_MYSQL_DB') or 'dev_db'
    MYSQL_DATABASE_HOST = os.environ.get('DEV_MYSQL_HOST') or 'localhost'

class ProductionConfig(Config):
    # Production-specific configuration
    DEBUG = False
    MYSQL_DATABASE_USER = os.environ.get('PROD_MYSQL_USER') or 'prod_user'
    MYSQL_DATABASE_PASSWORD = os.environ.get('PROD_MYSQL_PASSWORD') or 'prod_password'
    MYSQL_DATABASE_DB = os.environ.get('PROD_MYSQL_DB') or 'prod_db'
    MYSQL_DATABASE_HOST = os.environ.get('PROD_MYSQL_HOST') or 'prod_host'

# You can add more configurations for different environments if necessary
