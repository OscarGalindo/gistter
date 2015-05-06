from flask import Blueprint, request, jsonify
from gistter import mongo
from ..models import User

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
    return 'Form to edit %s profile' % username


@user.route('/', methods=['POST'])
def create():
    userdata = request.get_json()
    return str(userdata)


@user.route('/', methods=['PUT'])
def update():
    return 'Updated'


@user.route('/<username>', methods=['DELETE'])
def delete(username):
    return 'Deleted %s' % username