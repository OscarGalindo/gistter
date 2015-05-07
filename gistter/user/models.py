from datetime import datetime
from flask import url_for
from mongokit import Document, ValidationError
import re


def email_validator(value):
    email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)', re.IGNORECASE)
    if not bool(email.match(value)):
        raise ValidationError('%s is not a valid email: ' % value)
    else:
        return True


class User(Document):
    __database__ = 'gistter'
    __collection__ = 'users'
    structure = {
        'username': basestring,
        'birth': datetime,
        'email': basestring,
        'password': basestring,
        'description': basestring,
        'tweets_count': int,
        'created_at': datetime,
        'following_count': int,
        'followers_count': int,
        'following_users': list,
        'followers_users': list
    }

    default_values = {
        'tweets_count': 0,
        'followers_count': 0,
        'following_count': 0,
        'following_users': [],
        'followers_users': [],
        'created_at': datetime.utcnow
    }

    validators = {
        'email': email_validator,
        'birth': lambda x: type(x) == datetime
    }

    required_fields = ['username', 'email', 'password']
    use_dot_notation = True

    def get_absolute_url(self):
        return url_for('user.index', kwargs={"username": self.username})


"""
JSON Mongo Model User:
    {
        "_id" : ObjectId("5537cf8f3004a076b0069f0d"),
        "username" : "oscarg",
        "birth" : "15/10/1987",
        "email" : "galindero@gmail.com",
        "password" : "password",
        "description" : "Intento de informático",
        "tweets_count" : NumberInt(0),
        "followers_count" : NumberInt(0),
        "following_count" : NumberInt(0),
        "following_users" : [

        ],
        "followers_users" : [

        ]
    }
"""