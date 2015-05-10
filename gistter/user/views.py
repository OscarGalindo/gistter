from datetime import datetime
from flask import Blueprint, request, jsonify
from .models import User
from gistter import mongo


user = Blueprint('user', __name__, url_prefix='/user')


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