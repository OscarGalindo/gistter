import datetime
from flask import url_for
from gistter import db


class User(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    username = db.StringField(max_length=255, required=True)
    birth = db.StringField(max_length=255)
    email = db.StringField(max_length=255, required=True)
    password = db.StringField(max_length=255, required=True)
    description = db.StringField(max_length=255)
    tweets_count = db.IntField()

    def get_absolute_url(self):
        return url_for('user.index', kwargs={"username": self.username})

    meta = {
        'collection': 'users',
        'allow_inheritance': True,
        'indexes': ['-created_at', 'username'],
        'ordering': ['-created_at']
    }