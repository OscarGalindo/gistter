from flask import Flask
from flask.ext.jwt import JWT
from flask.ext.mongokit import MongoKit

app = Flask(__name__)
app.config.from_object('config')

mongo = MongoKit(app)
jwt = JWT(app)

from .user.views import user
from .auth.views import auth
app.register_blueprint(user)
app.register_blueprint(auth)

from .user.models import User
mongo.register([User])


@app.errorhandler(404)
def not_found(error):
    return "<h1>%s</h1>" % error


@app.errorhandler(500)
def internal_error(exception):
    return "<h1>%s</h1>" % exception