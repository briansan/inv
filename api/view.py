from flask import Response
import json
import methods

def login():
  return '''<form action="" method="post">
              <p>Username: <input type=text name=uname></p>
              <p>Password: <input type=password name=passwd></p>
              <input type=submit>
         </form>'''

def json_response(d,code=200):
  return Response(response=d, status=code, mimetype="application/json")

def success(msg):
  return json_response(json.dumps({'success':True,'msg':msg}))

def failure(msg,code=400):
  return json_response(json.dumps({'success':False,'msg':msg}), code)

def welcome(uname):
  return success('welcome %s!'%uname)

def all_methods():
  return success(methods.info)

def request_login():
  return failure('please log in first', 401)

def goaway(uname):
  return failure('you don\'t even go here %s...'%uname, 401)

def keep_away():
  return failure('insufficient permissions', 403)

def missing_field(field):
  return failure('missing field: '+field, 406)
 
def already_exists(entity):
  return failure(entity+' already exists', 409)

def dne(entity):
  return failure('this ' + entity + ' does not exists', 404)

def invalid_method(x=None):
  return failure('invalid method', 405)
