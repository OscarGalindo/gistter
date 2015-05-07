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
        'updated_at': datetime,
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
        'created_at': datetime.utcnow,
        'updated_at': datetime.utcnow
    }

    validators = {
        'email': email_validator,
        'birth': lambda x: type(x) == datetime
    }

    required_fields = ['username', 'email', 'password']
    use_dot_notation = True
    raise_validation_errors = False

    def get_absolute_url(self):
        return url_for('user.index', kwargs={"username": self.username})

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(User, self).save(*args, **kwargs)
