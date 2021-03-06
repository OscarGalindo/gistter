from datetime import timedelta
import os

_basedir = os.path.abspath(os.path.dirname(__file__))

# General configuration
DEBUG = True
BCRYPT_LEVEL = 12
SECRET_KEY = "n1a0Ma1iHJcgb6QTi4uyj3HYCwokV2P6"

JWT_EXPIRATION_DELTA = timedelta(minutes=60)

# MongoEngine Configuration
MONGODB_DATABASE = 'gistter'
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
