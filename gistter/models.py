from datetime import datetime
from flask import url_for
from flask.ext.mongokit import Document
from gistter import mongo


class User(Document):
    __collection__ = 'users'
    structure = {
        'username': unicode,
        'birth': datetime,
        'email': unicode,
        'password': unicode,
        'description': unicode,
        'tweets_count': int,
        'created_at': datetime
    }

    required_fields = ['username', 'email', 'password']
    default_values = {'tweets_count': 0, 'created_at': datetime.utcnow}

    def get_absolute_url(self):
        return url_for('user.index', kwargs={"username": self.username})


mongo.register([User])