from flask import Blueprint, request, session, g
from bson import ObjectId

from gistter import mongo
from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


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
    userdata = request.get_json()
    return str(userdata)


@user.route('/', methods=['PUT'])
def update():
    return 'Updated'


@user.route('/<username>', methods=['DELETE'])
def delete(username):
    return 'Deleted %s' % username