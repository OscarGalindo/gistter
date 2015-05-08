from datetime import datetime, timedelta
from flask import Blueprint, request, session, g, jsonify
from bson import ObjectId
from flask.ext.jwt import jwt_required
from werkzeug.security import check_password_hash
from .models import User
from gistter import mongo, jwt, app


user = Blueprint('user', __name__, url_prefix='/user')


@jwt.payload_handler
def make_payload(userdata):
    return {
        'username': userdata.username,
        'email': userdata.email
    }


@jwt.user_handler
def load_user(payload):
    if payload['username']:
        return mongo.User.find_one({"username": payload['username']})


@jwt.authentication_handler
def authenticate(username, password):
    userdata = mongo.User.find_one({"username": username})
    if userdata is not None and check_password_hash(userdata.password, password):
        return userdata



# @user.route('/protected')
# @jwt_required()
# def protected():
#     return 'Success!'


@user.before_request
def before_request():
    """
    Guarda el usuario en el objeto g si es que existe en session
    """
    g.user = None
    if 'user_id' in session:
        g.user = mongo.User.find_one({'_id': ObjectId(session['user_id'])})


@user.route('/<username>')
@user.route('/')
def index(username=None):
    if username is None:
        return 'Profile'
    else:
        userobject = mongo.User.find_one({'username': username})
        if userobject is None:
            return 'User %s not found' % username, 404
        else:
            return userobject.to_json()


@user.route('/<username>/edit')
def edit(username):
    userobject = mongo.User.find_one({'username': username})
    if userobject is None:
        return 'User %s not found' % username, 404
    else:
        return userobject.to_json()


@user.route('/', methods=['POST'])
def create():
    data = request.get_json()
    userdata = mongo.User()
    userdata.username = data.get('username')
    userdata.password = data.get('password')
    userdata.email = data.get('email')

    if data.get('birth') is not None:
        birth = datetime.strptime(data.get('birth'), '%Y-%m-%dT%H:%M:%S.%fZ')
        userdata.birth = birth

    userdata.validate()

    if userdata.validation_errors:
        return str(userdata.validation_errors)

    userdata.save()
    return jsonify({'username': userdata.username})


@user.route('/', methods=['PUT'])
def update():
    return 'Updated'


@user.route('/<username>', methods=['DELETE'])
def delete(username):
    return 'Deleted %s' % username