from datetime import datetime
from flask import url_for
from mongokit import Document, ValidationError
from gistter import mongo
import re


def email_validator(value):
    email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)', re.IGNORECASE)
    if not bool(email.match(value)):
        raise ValidationError('%s is not a valid email')


@mongo.register
class User(Document):
    __database__ = 'gistter'
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

    validators = {
        'email': email_validator,
        'birth': lambda x: type(x) == datetime
    }

    required_fields = ['username', 'email', 'password']
    default_values = {'tweets_count': 0, 'created_at': datetime.utcnow}

    def get_absolute_url(self):
        return url_for('user.index', kwargs={"username": self.username})
