from flask import Blueprint, request

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/<username>')
@user.route('/')
def index(username=None):
    if username is None:
        return 'Profile'
    else:
        return 'Profile %s' % username


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