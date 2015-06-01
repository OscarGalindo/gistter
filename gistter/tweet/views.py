from flask import Blueprint, request, jsonify, g, make_response
from flask.ext.jwt import jwt_required

from gistter import mongo
from ..tweet.models import Tweet
from bson.objectid import ObjectId

tweet = Blueprint('tweet', __name__)


@tweet.route('/<ObjectId:tweet_id>')
def index(tweet_id):
    response = dict()
    response.update(tweet=mongo.Tweet.get_from_id(tweet_id).data())
    response.update(childs=[x.data() for x in mongo.Tweet.find({'response_to': tweet_id})])
    parents = []
    if response.get('tweet') is None:
        return make_response(jsonify({'errors': 'Tweet not found'}), 404)
    else:
        return jsonify(response)


@tweet.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    data['user'] = g.user
    tweetdata = mongo.Tweet()
    tweetdata.bind(data)
    tweetdata.validate()

    if tweetdata.validation_errors:
        errors = {}
        for field in tweetdata.validation_errors:
            errors.update({field: tweetdata.validation_errors[field][0].message})
        return jsonify({'errors': errors})

    tweetdata.save()
    return jsonify({'success': True})


@tweet.route('/<ObjectId:tweet_id>', methods=['DELETE'])
@jwt_required()
def delete(tweet_id):
    t = mongo.Tweet.get_from_id(tweet_id)
    if str(g.user._id) == str(t.user._id):
        t.delete()
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Not the user of the tweet'})
