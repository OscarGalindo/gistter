from flask import Blueprint, jsonify
from werkzeug.security import check_password_hash
from gistter import mongo, jwt


auth = Blueprint('auth', __name__, url_prefix='/')


@jwt.authentication_handler
def authenticate(username, password):
    """
    Url: /auth (Generada automaticamente por flask-jwt)
    :param username:
    :param password:
    :return token:
    """
    userdata = mongo.User.find_one({"username": username})
    if userdata is not None and check_password_hash(userdata.password, password):
        return userdata


@jwt.payload_handler
def make_payload(userdata):
    """
    Payload para generar el JWT devuelto una vez logueado
    :param userdata:
    :return payload:
    """
    return {
        'username': userdata.username,
        'email': userdata.email
    }


@jwt.error_handler
def error_handler(e):
    """
    Respuesta en caso de error
    :param e:
    :return Json:
    """
    return jsonify(dict([
        ('status_code', e.status_code),
        ('description', e.description),
    ])), 200, e.headers


@jwt.user_handler
def load_user(payload):
    """
    Devuelve instancia de la clase User del payload que se devuelve
    :param payload:
    :return User:
    """
    if payload['username']:
        return mongo.User.find_one({"username": payload['username']})

