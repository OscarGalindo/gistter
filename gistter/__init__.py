from flask import Flask
import mongokit

app = Flask(__name__)
app.config.from_object('config')

from .user.user import user
app.register_blueprint(user)
mongo = mongokit.Connection()