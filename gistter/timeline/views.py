from flask import Blueprint, g, jsonify
from flask.ext.jwt import jwt_required

from gistter import mongo

timeline = Blueprint('timeline', __name__)


@timeline.route('/')
@jwt_required()
def index():
    tweets = mongo.Tweet.find({
        '$or': [
            {'user.$id': {'$in': g.user.following}},
            {'user.$id': g.user._id}
        ]
    })
    data = dict(
        tweets=[x.data() for x in tweets]
    )
    return jsonify(data)

