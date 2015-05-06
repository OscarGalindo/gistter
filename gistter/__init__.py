from flask import Flask
import mongokit

app = Flask(__name__)
app.config.from_object('config')

mongo = mongokit.Connection()

from .user.views import user
app.register_blueprint(user)


@app.errorhandler(404)
def not_found(error):
    return "<h1>%s</h1>" % error


@app.errorhandler(500)
def internal_error(exception):
    return "<h1>%s</h1>" % exception