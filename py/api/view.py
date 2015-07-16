from flask import Response
import json
import methods

def login():
  return '''<form action="" method="post">
              <p>Username: <input type=text name=uname></p>
              <p>Password: <input type=password name=passwd></p>
              <input type=submit>
         </form>'''

def json_response(d):
  return Response(response=d, status=200, mimetype="application/json")

def success(msg):
  return json_response(json.dumps({'success':True,'msg':msg}))

def failure(msg):
  return json_response(json.dumps({'success':False,'msg':msg}))

def welcome(uname):
  return success('welcome %s!'%uname)

def all_methods():
  return success(methods.info)

def request_login():
  return failure('please log in first')

def goaway(uname):
  return failure('you don\'t even go here %s...'%uname)

def keep_away():
  return failure('insufficient permissions')

def missing_field(field):
  return failure('missing field: '+field)
 
def already_exists(entity):
  return failure(entity+' already exists')

def dne(entity):
  return failure('this ' + entity + ' does not exists')
