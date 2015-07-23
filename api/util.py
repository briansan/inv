"""
 @file   inv/api/util.py
 @author Brian Kim
 @brief  a script that defines utility methods for the server
"""

from auth import auth_inv
from datetime import timedelta
from functools import update_wrapper, wraps
from flask import current_app, make_response, request, Response

"""
 convenience methods to determine the http method used
"""

def is_create():
  return request.method == 'POST'

def is_read():
  return request.method == 'GET'

def is_update():
  return request.method == 'PUT'
  
def is_delete():
  return request.method == 'DELETE'

"""
 authentication decorator
"""

def authenticate():
  """sends a 401 resposne that enables basic auth"""
  msg = 'Could not verify your access level for that URL.\n'
  msg += 'You have to login with proper credentials'
  header = {'WWW-Authenticate': 'Basic realm="Login Required"'}
  return Response( msg, 401, header )

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not auth_inv(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

"""
 cross-origin resource sharing decorator
"""
def crossdomain(origin='*', methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
  if methods is not None:
    methods = ', '.join(sorted(x.upper() for x in methods))
  if headers is not None and not isinstance(headers, basestring):
    headers = ', '.join(x.upper() for x in headers)
  if not isinstance(origin, basestring):
    print origin
    origin = ', '.join(origin)
  if isinstance(max_age, timedelta):
    max_age = max_age.total_seconds()

  def get_methods():
    if methods is not None:
      return methods

    options_resp = current_app.make_default_options_response()
    return options_resp.headers['allow']

  def decorator(f):
    def wrapped_function(*args, **kwargs):
      if automatic_options and request.method == 'OPTIONS':
        resp = current_app.make_default_options_response()
      else:
        resp = make_response(f(*args, **kwargs))
      if not attach_to_all and request.method != 'OPTIONS':
        return resp

      h = resp.headers

      h['Access-Control-Allow-Origin'] = origin
      h['Access-Control-Allow-Methods'] = get_methods()
      h['Access-Control-Max-Age'] = str(max_age)
      h['Access-Control-Allow-Credentials'] = 'true'
      h['Access-Control-Allow-Headers'] = 'X-Requested-With'
      if headers is not None:
        h['Access-Control-Allow-Headers'] = headers
      return resp

    f.provide_automatic_options = False
    return update_wrapper(wrapped_function, f)
  return decorator
