from flask import Blueprint, request, jsonify, abort
from flask.ext.jwt import jwt_required, current_user, verify_jwt, JWTError
from gistter import mongo

user = Blueprint('user', __name__)


@user.route('/<username>')
@user.route('/')
def index(username=None):
    if username is None:
        try:
            verify_jwt()
            if current_user is not None:
                return current_user.to_json()
        except JWTError:
            abort(404)
    else:
        userobject = mongo.User.find_one({'username': username})
        if userobject is None:
            return jsonify({'errors': 'User <strong>{username}</strong> not found'.format(username=username)})
        else:
            return userobject.to_json()


@user.route('/<username>/edit')
@jwt_required()
def edit(username):
    userobject = mongo.User.find_one({'username': username})
    if userobject is None:
        return jsonify({'errors': 'User <strong>{username}</strong> not found'.format(username=username)})
    else:
        return jsonify(userobject)


@user.route('/', methods=['POST'])
def create():
    data = request.get_json()
    userdata = mongo.User()
    userdata.bind(data)
    userdata.validate()

    if userdata.validation_errors:
        errors = {}
        for field in userdata.validation_errors:
            errors.update({field: userdata.validation_errors[field][0].message})
        return jsonify({'errors': errors})

    userdata.save()
    return jsonify({'success': True})


@user.route('/', methods=['PUT'])
@jwt_required()
def update():
    return 'Updated'


@user.route('/<username>', methods=['DELETE'])
@jwt_required()
def delete(username):
    return 'Deleted %s' % username
