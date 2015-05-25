import re
from flask import url_for
from gistter import mongo
from gistter.coremodel import Core
from gistter.user.models import User
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

@mongo.register
class Tweet(Core):
    __collection__ = 'tweets'
    structure = {
        'user': User,
        'user_rt': User,
        'body': basestring,
        'code': basestring,
        'code_html': basestring,
        'retweet': bool,
        'favorites_count': int,
        'retweet_count': int,
        'hashtags': [unicode],
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
    skip_validation = False

    def bind(self, data):
        self.user = data.get('user')
        self.body = data.get('body')
        self.code = data.get('code', '')
        self.code_html = highlight(data.get('code'), PythonLexer(), HtmlFormatter()) if len(self.code) > 0 else ''

        self.hashtags = [re.sub(r"#+", "#", k) for k in set(
            [re.sub(r"(\W+)$", "", j, flags=re.UNICODE) for j in
             [i for i in data.get('body').split() if i.startswith("#")]])]

    def get_absolute_url(self):
        return url_for('tweet.index', kwargs={"id": self.username})

    def data(self):
        tweet = self
        tweet['_id'] = str(tweet['_id'])
        tweet['user'] = self.user.data()
        return tweet
