import re
import uuid
from flask import url_for
from gistter import mongo
from gistter.coremodel import Core
from gistter.user.models import User


@mongo.register
class Tweet(Core):
    __collection__ = 'users'
    structure = {
        'user': User,
        'user_rt': User,
        'reply_to': uuid.UUID,
        'body': basestring,
        'retweet': bool,
        'favorites_count': int,
        'retweet_count': int,
        'hashtags': [basestring],
    }

    default_values = {
        'favorites_count': 0,
        'retweet_count': 0,
        'hashtags': [],
        'retweet': False,
    }

    validators = {
        'body': lambda x: len(x) >= 1
    }

    required_fields = ['user', 'body']
    use_autorefs = True

    def bind(self, data):
        self.user = mongo.User.find_one({'username': data.get('username')})
        self.body = data.get('body')
        self.body_html = data.get('body')
        self.hashtags = set([re.sub(r"#+", "#", k) for k in set(
            [re.sub(r"(\W+)$", "", j, flags=re.UNICODE) for j in
             set([i for i in data.get('body').split() if i.startswith("#")])])])

    def get_absolute_url(self):
        return url_for('tweet.index', kwargs={"id": self.username})