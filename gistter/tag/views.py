from flask import Blueprint, jsonify, g, make_response

from gistter import mongo
from ..tweet.models import Tweet

tag = Blueprint('tag', __name__)


@tag.route('/<hashtag:hashtag>')
def index(hashtag):
    tweets = mongo.Tweet.find({"hashtags": hashtag})
    if tweets is None:
        return make_response(jsonify({'errors': 'No tweets with that tag.'}), 404)
    else:
        data = dict(
            tweets=[x.data() for x in tweets],
            hashtag=hashtag
        )
        return jsonify(data)
