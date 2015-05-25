from flask import Blueprint, request, jsonify, g
from flask.ext.jwt import jwt_required
from gistter import mongo


timeline = Blueprint('timeline', __name__)


@timeline.route('/')
@jwt_required()
def index():

    tweets = mongo.Tweet.find({
        '$or' : [
            {'user.$id': { '$in': g.user.following_users} },
            {'user.$id': g.user._id}
        ]
    })
    return jsonify([x.data() for x in tweets])
