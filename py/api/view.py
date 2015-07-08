import json

def request_login():
  return 'please log in first'

def method_desc(name,desc,supports):
  return {'name':name,'desc':desc,'supports':supports}

def all_methods():
  m = [method_desc('add', 'inserts an entity', 'POST'),
       method_desc('view', 'selects an entity', 'GET'),
       method_desc('edit', 'updates an entity', 'POST'),
       method_desc('remove', 'deletes an entity', 'GET')]
  e = ['user','item','inventory','asset','location']
  n = ['/{method}/{entity}/{description or id}',
       '/{utility}']
  u = ['login','logout','register','help']
  d = {'methods':m,'entities':e,'navigation':n, 'utility':u}
  return json.dumps(d,indent=4,separators=(',',': '))

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
