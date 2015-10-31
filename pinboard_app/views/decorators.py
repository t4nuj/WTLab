from functools import wraps
from flask import session, abort


def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if not session['logged_in']:
                return abort(403)
            else:
                return f(*args, **kwargs)
        except KeyError:
            session['logged_in'] = False
            return abort(403)

    return decorated_function
