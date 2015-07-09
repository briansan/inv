import json
import methods

def request_login():
  return 'please log in first'

def method_desc(name,desc,supports):
  return {'name':name,'desc':desc,'supports':supports}

def all_methods():
  return json.dumps(methods.info,indent=4,separators=(',',': '))

def login():
  return '''<form action="" method="post">
              <p>Username: <input type=text name=uname></p>
              <p>Password: <input type=password name=passwd></p>
              <input type=submit>
         </form>'''

def success(msg):
  return json.dumps({'success':True,'msg':msg})

def failure(msg):
  return json.dumps({'success':False,'msg':msg})

def welcome(uname):
  return success('welcome %s!'%uname)

def goaway(uname):
  return failure('you don\'t even go here %s...'%uname)
