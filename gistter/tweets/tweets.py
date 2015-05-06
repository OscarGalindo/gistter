from flask import Blueprint, request

tweets = Blueprint('tweets', __name__, url_prefix='/tweets')


@tweets.route('/<username>')
@tweets.route('/')
def index(username=None):
    if username is None:
        return 'Timeline'
    else:
        return 'Timeline %s' % username


@tweets.route('/', methods=['POST'])
def create():
    tweetdata = request.get_json()
    return str(tweetdata)


@tweets.route('/', methods=['PUT'])
def update():
    return 'Updated'


@tweets.route('/<id>', methods=['DELETE'])
def delete(id):
    return 'Deleted %s' % id
