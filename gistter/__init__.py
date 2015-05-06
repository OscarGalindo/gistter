from flask import Flask
from flask.ext.pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')
mongo = MongoClient()

from .user.user import user
app.register_blueprint(user)


app.run(debug=app.config['DEBUG'])