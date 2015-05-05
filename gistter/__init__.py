from flask import Flask
from .user.user import user
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_object('config')

db = MongoEngine(app)

app.register_blueprint(user)

app.run(debug=app.config['DEBUG'])