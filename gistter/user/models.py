from datetime import datetime
from flask import url_for
import re
from mongokit import ValidationError
from werkzeug.security import generate_password_hash
from gistter import mongo
from gistter.coremodel import Core


def email_validator(value):
    email = re.compile(r'(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)', re.IGNORECASE)
    if not bool(email.match(value)):
        raise ValidationError("%s is not a valid email.".format(email))
    return True


def unique_email(email):
    user = mongo.User.find_one({"email": email})
    if bool(user):
        raise ValidationError("%s already exists.".format(email))
    return True


def unique_username(username):
    user = mongo.User.find_one({"username": username})
    if bool(user):
        raise ValidationError("%s already exists.".format(username))
    return True


@mongo.register
class User(Core):
    __collection__ = 'users'
    structure = {
        'username': basestring,
        'birth': datetime,
        'name': basestring,
        'lastname': basestring,
        'city': basestring,
        'email': basestring,
        'password': basestring,
        'description': basestring,
        'tweets_count': int,
        'following_count': int,
        'followers_count': int,
        'following_users': list,
        'followers_users': list,
        'favorites': list
    }

    default_values = {
        'tweets_count': 0,
        'followers_count': 0,
        'following_count': 0,
        'following_users': [],
        'followers_users': [],
        'favorites': []
    }

    validators = {
        'email': [email_validator, unique_email],
        'birth': lambda x: type(x) == datetime,
        'password': lambda x: len(x) >= 3,
        'name': lambda x: len(x) >= 1,
        'lastname': lambda x: len(x) >= 1,
        'username': unique_username
    }

    indexes = [
        {
            'fields': ['username', 'email'],
            'unique': True
        }
    ]

    required_fields = ['username', 'email', 'password']

    def bind(self, data):
        self.username = data.get('username')
        self.password = generate_password_hash(data.get('password'))
        self.email = data.get('email')
        self.name = data.get('name')
        self.lastname = data.get('lastname')
        self.fullname = '{name} {lastname}'.format(name=self.name, lastname=self.lastname)

    def get_absolute_url(self):
        return url_for('user.index', kwargs={"username": self.username})

    def find_by_username(self, username):
        return self.find_one({username: username})

    def data(self):
        user = self
        user['_id'] = str(user['_id'])
        del user['password']
        return user
