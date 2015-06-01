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

    mongo.init_app(app)  # Iniciamos la base de datos
    jwt.init_app(app)  # Iniciamos el servicio que nos ayudara a tratar los JWT
    cors.init_app(app)  # Iniciamos el servicio para controlar el CORS

    from .util import HashtagConverter  # Importamos URL Converter para Hashtag
    app.url_map.converters['hashtag'] = HashtagConverter  # Definimos el URL Converter para que Flask lo conozca

    # Importamos y registramos todos los blueprints de la aplicacion
    from .user.views import user as user_blueprint
    from .tweet.views import tweet as tweet_blueprint
    from .auth.views import auth as auth_blueprint
    from .timeline.views import timeline as timeline_blueprint
    from .tag.views import tag as tag_blueprint
    from .search.views import search as search_blueprint

    app.register_blueprint(user_blueprint, url_prefix="/user")
    app.register_blueprint(tweet_blueprint, url_prefix="/tweet")
    app.register_blueprint(timeline_blueprint, url_prefix="/timeline")
    app.register_blueprint(tag_blueprint, url_prefix="/tag")
    app.register_blueprint(search_blueprint, url_prefix="/search")
    app.register_blueprint(auth_blueprint)

    @app.errorhandler(404)
    def not_found(error):
        return "<h1>%s</h1>" % error, 404

    @app.errorhandler(500)
    def internal_error(exception):
        return "<h1>%s</h1>" % exception, 500

    return app
