from flask import Flask
from flask.ext.jwt import JWT
from .user.models import User
from flask.ext.mongokit import MongoKit

app = Flask(__name__)
app.config.from_object('config')

mongo = MongoKit(app)
jwt = JWT(app)
mongo.register([User])

from .user.views import user
app.register_blueprint(user)


@app.errorhandler(404)
def not_found(error):
    return "<h1>%s</h1>" % error


@app.errorhandler(500)
def internal_error(exception):
    return "<h1>%s</h1>" % exception