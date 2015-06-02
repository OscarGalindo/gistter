import re
from flask import Blueprint, jsonify
from flask.ext.jwt import jwt_required
from gistter import mongo
from ..user.models import User

search = Blueprint('search', __name__)


@search.route('/<string:text>')
def searcher(text):
    users = mongo.User.find({"username": {"$regex": re.compile(text, re.IGNORECASE)}})
    data = dict(
        users=[x.data() for x in users]
    )
    return jsonify(data)

