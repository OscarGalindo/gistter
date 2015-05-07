from flask import Flask
import mongokit

app = Flask(__name__)
app.config.from_object('config')

connection = mongokit.Connection()
mongo = connection[app.config['MONGODB_DATABASE']]


from .user.models import User
from .user.views import user
connection.register([User])
app.register_blueprint(user)


@app.errorhandler(404)
def not_found(error):
    return "<h1>%s</h1>" % error


@app.errorhandler(500)
def internal_error(exception):
    return "<h1>%s</h1>" % exception