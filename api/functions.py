from flask import request
from flask_restful import abort

def auth_key(func):
    def dec(*args, **kwargs):

        if 'key' in request.json and request.json['key'] == 'qwerty':
            return func(*args, **kwargs)
        else:
            return abort(404, message=f"Auth error")

    return dec

