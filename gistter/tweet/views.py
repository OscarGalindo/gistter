from flask import Blueprint, request, jsonify
from flask.ext.jwt import jwt_required, current_user
from gistter import mongo


tweet = Blueprint('tweet', __name__)


@tweet.route('/<ObjectId:tweet_id>')
def index(tweet_id):
    tweet_data = mongo.Tweet.get_from_id(tweet_id)
    if tweet_data is None:
        return jsonify({'errors': 'Tweet not found'})
    else:
        return tweet_data.to_json()


@tweet.route('/', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    data['user'] = current_user._get_current_object()
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