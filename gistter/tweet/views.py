from flask import Blueprint, request, jsonify
from flask.ext.jwt import jwt_required
from gistter import mongo


tweet = Blueprint('tweet', __name__)


@tweet.route('/<ObjectId:tweet_id>')
def index(tweet_id):
    tweet_data = mongo.Tweet.get_from_id(tweet_id)
    if tweet_data is None:
        return '{tweet_id} not found'.format(tweet_id=tweet_data), 404
    else:
        return tweet.to_json()


@tweet.route('/', methods=['POST'])
@jwt_required()
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


@tweet.route('/<tweet_id>', methods=['DELETE'])
def delete(tweet_id):
    return 'Deleted {tweet_id}'.format(tweet_id=tweet_id)