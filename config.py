import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# General configuration
DEBUG = True
BCRYPT_LEVEL = 12
SECRET_KEY = "n1a0Ma1iHJcgb6QTi4uyj3HYCwokV2P6"


# MongoEngine Configuration
MONGODB_DB = 'gistter'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017