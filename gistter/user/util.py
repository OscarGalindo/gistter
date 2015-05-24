# from functools import wraps
# from flask import abort
# from werkzeug.routing import BaseConverter
# from gistter import mongo
#
#
# class UserConverter(BaseConverter):
#     def to_python(self, username):
#         user = mongo.User.find_one({'username': username})
#         return user if not None else abort(404)
#
#     def to_url(self, username):
#         return username.username
#
# def exist_user(user=None):
#     @wraps(user)
#     def decorated_function(*args, **kwargs):
#         user = mongo.User.find_one({'username': username})
#         return user if not None else abort(404)
#
