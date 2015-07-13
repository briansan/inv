"""
  @file   inv/api/controller.py
  @author Brian Kim
  @brief  this module defines the functionality of 
          the methods described by inv/api/methods.py
"""

from flask import request, session
import auth, methods, model, view

"""
  authentication methods
"""

def logged_in():
  return session.get('uname')

def root():
  if 'uname' in session:
    return view.all_methods()
  else:
    return view.request_login()
  
def login():
  if not logged_in():
    # get the user information if post requested
    if request.method=='POST':
      uname = request.form['uname']
      pw = request.form['passwd']
      y = auth.auth_inv(uname,pw) # authenticate
      if not (type(y) is str): # string means failure
        session['uname'] = dict(y) # success => welcome
        return view.welcome(y.fname + ' ' + y.lname)
      else: # failure => go away
        return view.failure(y)
    else: # GET, display login view
      return view.login()
  else:
    return view.failure('you\'re already logged in...')

def logout():
  if logged_in():
    session.pop('uname',None)
    return view.success('bye bye!')
  else:
    return view.failure('you didn\'t login...')

"""
  authorization methods
"""
def check_auth(method):
  p = session['uname']['perm']
  a = auth.Authorization(p)
  return a.chk(method)

"""
  parsing methods from the posted form
"""
def parse_location():
  y = {}
  try:
    y['building'] = request.form['building']
    y['room'] = request.form['room']
  except KeyError as k:
    raise Exception(k.args[0])
  return y

"""
  create methods
"""
def add(entity):
  if logged_in():
    try:
      return add_methods[entity]()
    except KeyError as k:
      return view.failure('invalid entity '+k.message)
  else:
    return view.request_login()

def add_location():
  if check_auth(methods.LocationCreate):
    # get the fields
    try:
      location = parse_location()
    except Exception as k:
      return view.failure('missing field: '+k.message)
    # add the location
    # model.db.session.add(location)
    # model.db.session.commit()

    return view.success(location)
  else:
    return view.keep_away()

def add_item():
  return view.success('add item')

def add_asset():
  return view.success('add asset')

def add_inv():
  return view.success('add inv')

def add_building():
  return view.success('add building')

def add_category():
  return view.success('add category')

def add_manufacturer():
  return view.success('add manufacturer')

add_methods = {
  'location': add_location,
  'item': add_item,
  'asset': add_asset,
  'inv': add_inv,
  'building': add_building,
  'category': add_category,
  'manufacturer': add_manufacturer
}

"""
  read methods
"""

def vw(entity):
  if logged_in():
    try:
      return vw_methods[entity]()
    except KeyError as k:
      return view.failure('invalid entity '+k.message)
  else:
    return view.request_login()

def view_user():
  return view.success('view user')

def view_location():
  return view.success('view location')

def view_item():
  return view.success('view item')

def view_asset():
  return view.success('view asset')

def view_inv():
  return view.success('view inv')

def view_building():
  return view.success('view building')

def view_category():
  return view.success('view category')

def view_manufacturer():
  return view.success('view manufacturer')

vw_methods = {
  'user': view_user,
  'location': view_location,
  'item': view_item,
  'asset': view_asset,
  'inv': view_inv,
  'building': view_building,
  'category': view_category,
  'manufacturer': view_manufacturer
}

"""
  update methods
"""

def edit(entity,id):
  if logged_in():
    try:
      return edit_methods[entity](id)
    except KeyError as k:
      return view.failure('invalid entity '+k.message)
  else:
    return view.request_login()

def edit_user(id):
  return view.success('edit user')

def edit_location(id):
  return view.success('edit location')

def edit_item(id):
  return view.success('edit item')

def edit_asset(id):
  return view.success('edit asset')

def edit_inv(id):
  return view.success('edit inv')

def edit_building(id):
  return view.success('edit building')

def edit_category(id):
  return view.success('edit category')

def edit_manufacturer(id):
  return view.success('edit manufacturer')

edit_methods = {
  'user': edit_user,
  'location': edit_location,
  'item': edit_item,
  'asset': edit_asset,
  'inv': edit_inv,
  'building': edit_building,
  'category': edit_category,
  'manufacturer': edit_manufacturer
}

"""
  delete methods
"""

def rm(entity,id):
  if logged_in():
    try:
      return rm_methods[entity](id)
    except KeyError as k:
      return view.failure('invalid entity '+k.message)
  else:
    return view.request_login()

def rm_user(id):
  return view.success('remove user')

def rm_location(id):
  return view.success('remove location')

def rm_item(id):
  return view.success('remove item')

def rm_asset(id):
  return view.success('remove asset')

def rm_inv(id):
  return view.success('remove inv')

def rm_building(id):
  return view.success('remove building')

def rm_category(id):
  return view.success('remove category')

def rm_manufacturer(id):
  return view.success('remove manufacturer')


rm_methods = {
  'user': rm_user,
  'location': rm_user,
  'item': rm_user,
  'asset': rm_user,
  'inv': rm_user,
  'building': rm_building,
  'category': rm_category,
  'manufacturer': rm_manufacturer
}
