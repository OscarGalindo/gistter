from flask import Blueprint, request, jsonify, g, make_response, abort
from flask.ext.jwt import jwt_required
from .. import mongo
from .models import User

user = Blueprint('user', __name__)

@user.route('/')
@jwt_required()
def profile():
    return g.user.to_json()

@user.route('/<string:userobj>')
def index(userobj):
    user = mongo.User.find_one({'username': userobj})
    return user.to_json() if not None else abort(404)


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
        return make_response(jsonify({'errors': errors}), 409)

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
