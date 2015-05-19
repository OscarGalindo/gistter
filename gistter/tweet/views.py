from flask import Blueprint, request, jsonify, abort
from flask.ext.jwt import jwt_required
from gistter import mongo


tweet = Blueprint('tweet', __name__)


@tweet.route('/<tweet_id>')
def index(tweet_id=None):
    if tweet_id is None:
        abort(404)
    else:
        userobject = mongo.User.find_one({'tweet_id': tweet_id})
        if userobject is None:
            return 'User {tweet_id} not found'.format(tweet_id=tweet_id), 404
        else:
            return userobject.to_json()


@tweet.route('/', methods=['POST'])
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
@jwt_required()
def delete(tweet_id):
    return 'Deleted {tweet_id}'.format(tweet_id=tweet_id)