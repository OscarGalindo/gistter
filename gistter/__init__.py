from flask import Flask
from flask.ext.mongokit import MongoKit

app = Flask(__name__)
app.config.from_object('config')

from .user.user import user
app.register_blueprint(user)
mongo = MongoKit(app)

app.run(debug=app.config['DEBUG'])