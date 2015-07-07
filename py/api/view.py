import json

def request_login():
  return 'please log in first'

def all_methods():
  m = ['users','items','locations','assets','locations','logout']
  return json.dumps(m)

def login():
  return '<form action="" method="post"><p>Username: <input type=text name=uname></p></form>'

def success(msg):
  return json.dumps({'success':True,'msg':msg})

def failure(msg):
  return json.dumps({'success':False,'msg':msg})

def welcome(uname):
  return success('welcome %s!'%uname)

def goaway(uname):
  return failure('you don\'t even go here %s...'%uname)
