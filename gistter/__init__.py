from flask import Flask
from flask.ext.mongokit import MongoKit
from flask.ext.cors import CORS
from flask.ext.jwt import JWT

mongo = MongoKit()
jwt = JWT()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    mongo.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)

    from .user.views import user as user_blueprint
    from .tweet.views import tweet as tweet_blueprint
    from .auth.views import auth as auth_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(tweet_blueprint, url_prefix="/tweet")
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return "<h1>%s</h1>" % error

    @app.errorhandler(500)
    def internal_error(exception):
        return "<h1>%s</h1>" % exception

    return app
