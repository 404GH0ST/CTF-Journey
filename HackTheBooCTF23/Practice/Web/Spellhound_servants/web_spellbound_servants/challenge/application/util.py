import os, pickle, base64
from flask import jsonify, abort, session, request
from functools import wraps

generate = lambda x: os.urandom(x).hex()
key = generate(50)

def response(message):
    return jsonify({'message': message})

def isAuthenticated(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.cookies.get('auth', False)

        if not token:
            return abort(401, 'Unauthorised access detected!')
        
        try:
            user = pickle.loads(base64.urlsafe_b64decode(token))
            kwargs['user'] = user
            return f(*args, **kwargs)
        except:
            return abort(401, 'Unauthorised access detected!')

    return decorator