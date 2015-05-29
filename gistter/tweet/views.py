from flask import Blueprint, request, jsonify, g, make_response
from flask.ext.jwt import jwt_required

from gistter import mongo
from ..tweet.models import Tweet
from bson.objectid import ObjectId

tweet = Blueprint('tweet', __name__)


@tweet.route('/<ObjectId:tweet_id>')
def index(tweet_id):
    response = dict()
    response.update(tweet=mongo.Tweet.get_from_id(tweet_id))
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


@tweet.route('/<tweet_id>', methods=['DELETE'])
def delete(tweet_id):
    return 'Deleted {tweet_id}'.format(tweet_id=tweet_id)
