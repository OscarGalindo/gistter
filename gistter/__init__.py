from flask import Flask
from .user.user import user

app = Flask(__name__)
app.config.from_object('config')

app.register_blueprint(user)