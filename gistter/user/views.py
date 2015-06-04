import re
import bson
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
    userdata = mongo.User.find_one_or_404({'username': {"$regex": re.compile(userobj, re.IGNORECASE)}}).data()
    tweets = mongo.Tweet.find({"user.$id": bson.objectid.ObjectId(userdata['_id'])})
    data = dict(
        profile=userdata,
        tweets=[x.data() for x in tweets]
    )
    return jsonify(data)


@user.route('/<string:userobj>/edit')
@jwt_required()
def edit(userobj):
    return jsonify(mongo.User.find_one_or_404({'username': userobj}).data())


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


@user.route('/<string:username>', methods=['DELETE'])
@jwt_required()
def delete(username):
    return 'Deleted %s' % username

@user.route('/<string:username>/unfollow')
@jwt_required()
def unfollow(username):
    if g.user.username == username:
        return jsonify({'error': 'User can\'t unfollow himself'})

    datauser = mongo.User.find_one_or_404({'username': username})
    g.user.remove_follower(datauser._id)
    datauser.remove_following(datauser._id)
    return jsonify({'success': True})

@user.route('/<string:username>/follow')
@jwt_required()
def follow(username):
    if g.user.username == username:
        return jsonify({'error': 'User can\'t follow himself'})

    datauser = mongo.User.find_one_or_404({'username': username})
    g.user.add_follower(datauser._id)
    datauser.add_following(datauser._id)
    return jsonify({'success': True})
