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

def parse_item():
  y = {}
  try:
    y['category'] = request.form['category']
    y['manufacturer'] = request.form['manufacturer']
    y['model'] = request.form['model']
  except KeyError as k:
    raise Exception(k.args[0])
  return y

def parse_asset():
  y = {}
  try:
    # get means optional field, [] means required field
    y['tag_ece'] = request.form['tag_ece'] #
    y['tag_vu'] = request.form.get('tag_vu')
    y['tag_unit'] = request.form.get('tag_unit')
    y['tag_svc'] = request.form.get('tag_svc')
    y['tag_serial'] = request.form.get('tag_serial')
    y['status'] = int(request.form['status']) #
    y['item'] = int(request.form['item']) #
    y['purchased'] = int(request.form.get('purchased'))
    y['img'] = request.form.get('img')
    y['owner'] = int(request.form.get('owner'))
    y['holder'] = int(request.form.get('holder'))
    y['price'] = float(request.form.get('price'))
    y['receipt'] = request.form.get('receipt')
    y['ip'] = request.form.get('ip')
    y['comments'] = request.form.get('comments')
    y['home'] = int(request.form.get('home'))
    y['current'] = int(request.form.get('current'))
  except KeyError as k:
    raise Exception(k.args[0])
  return y

def parse_inv():
  y = {}
  try:
    y['who'] = int(request.form['who'])
    y['what'] = int(request.form['who'])
    y['when'] = int(request.form['who'])
    y['where'] = int(request.form['who'])
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
      import traceback
      print traceback.format_exc()
      return view.failure('invalid entity '+k.message)
  else:
    return view.request_login()

def add_location():
  if check_auth(methods.LocationCreate):
    # get the fields
    try:
      location = parse_location()
    except Exception as k:
      return view.missing_field(k.message)
    # add the location
    x = methods.create_location(location)
    return view.success(dict(x)) if x else view.already_exists('location')
  else:
    return view.keep_away()

def add_item():
  if check_auth(methods.ItemCreate):
    try:
      item = parse_item()
    except Exception as k:
      return view.missing_field(k.message)
    # add the item
    x = methods.create_item(item)
    return view.success(dict(x)) if x else view.already_exists('item')
  else:
    return view.keep_away()

def add_asset():
  if check_auth(methods.AssetCreate):
    try:
      asset = parse_asset()
    except Exception as k:
      return view.missing_field(k.message)
    # add the asset
    x = methods.create_asset(asset)
    return view.success(dict(x)) if x else view.already_exists('asset')
  else:
    return view.keep_away()

def add_inv():
  if check_auth(methods.InvCreate):
    try:
      inv = parse_inv()
    except Exception as k:
      return view.missing_field(k.message)
    # add the inv
    x = methods.create_inv(inv)
    return view.success(dict(x)) if x else view.already_exists('inventory')
  else:
    return view.keep_away()

def add_building():
  if check_auth(methods.LocBuildEdit):
    try:
      man = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    # add the building
    x = methods.create_building(man)
    return view.success(dict(x)) if x else view.already_exists('building')
  else:
    return view.keep_away()

def add_category():
  if check_auth(methods.ItemCatEdit):
    try:
      man = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    # add the category
    x = methods.create_category(man)
    return view.success(dict(x)) if x else view.already_exists('category')
  else:
    return view.keep_away()

def add_manufacturer():
  if check_auth(methods.ItemManEdit):
    try:
      man = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    # add the manufacturer
    x = methods.create_manufacturer(man)
    return view.success(dict(x)) if x else view.already_exists('manufacturer')
  else:
    return view.keep_away()

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

def vw(entity,id=0):
  if logged_in():
    try:
      return vw_methods[entity](id)
    except KeyError as k:
      return view.failure('invalid entity '+k.message)
  else:
    return view.request_login()

def filter(x):
  """
    filters through the list x with the values from the request arguments
  """
  y = []
  for el in x:
    good = True
    for key in request.args:
      # get the element and query values
      el_val = el.get(key)
      q_val = request.args.get(key)
      # do a little type checking
      try:
        # if the element value is a dictionary
        if type(el_val) == dict:
          el_val = el_val['id']
        # check for mismatched types
        elif type(el_val) != type(q_val):
          q_val = type(el_val)(q_val)
      except:
        pass
      # check to see if the element passes the filter
      if el_val != q_val:
        good = False
        break
    if good: y.append(el)
  return y

def view_self():
  if check_auth(methods.UserReadSelf):
    return view.success(session['uname'])
  else:
    return view.keep_away()

def view_user(id=0):
  if check_auth(methods.UserReadWorld):
    if id is 0:
      x = methods.read_user_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = dict(methods.read_user(id))
    return view.success(y)
  else:
    return view.keep_away()
  
def view_location(id=0):
  if check_auth(methods.LocationRead):
    if id is 0:
      x = methods.read_location_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = dict(methods.read_location(id))
    return view.success(y)
  else:
    return view.keep_away()

def view_item(id=0):
  if check_auth(methods.ItemRead):
    if id is 0:
      x = methods.read_item_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = dict(methods.read_item(id))
    return view.success(y)
  else:
    return view.keep_away()

def view_asset(id=0):
  if check_auth(methods.AssetRead):
    if id is 0:
      x = methods.read_asset_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = dict(methods.read_asset(id))
    return view.success(y)
  else:
    return view.keep_away()

def view_inv(id=0):
  if check_auth(methods.InvRead):
    if id is 0:
      x = methods.read_inv_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = dict(methods.read_inv(id))
    return view.success(y)
  else:
    return view.keep_away()

def view_building(id=0):
  if check_auth(methods.LocBuildView):
    y = methods.read_building_all()
    return view.success(y)
  else:
    return view.keep_away()

def view_category(id=0):
  if check_auth(methods.ItemCatView):
    y = methods.read_category_all()
    return view.success(y)
  else:
    return view.keep_away()

def view_manufacturer(id=0):
  if check_auth(methods.ItemManView):
    y = methods.read_manufacturer_all()
    return view.success(y)
  else:
    return view.keep_away()

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

def edit_user_self(id):
  return view.success('edit user')

def edit_location(id):
  if check_auth(methods.LocationUpdate):
    try:
      x = parse_location()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_location(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('location')
  else: return view.keep_away()

def edit_item(id):
  if check_auth(methods.ItemUpdate):
    try:
      x = parse_item()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_item(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('item')
  else: return view.keep_away()

def edit_asset(id):
  if check_auth(methods.AssetUpdate):
    try:
      x = parse_asset()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_asset(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('asset')
  else: return view.keep_away()

def edit_inv(id):
  if check_auth(methods.InvUpdate):
    try:
      x = parse_inv()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_inv(id,x)
    # check the results
    if y: return view.success(dict(y))
    else: return view.dne('inventory')
  else: return view.keep_away()

def edit_building(id):
  if check_auth(methods.LocBuildEdit):
    try:
      x = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    y = methods.update_building(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('building')
  else:return view.keep_away()

def edit_category(id):
  if check_auth(methods.ItemCatEdit):
    try:
      x = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    y = methods.update_category(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('category')
  else:return view.keep_away()

def edit_manufacturer(id):
  if check_auth(methods.ItemManEdit):
    try:
      x = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    y = methods.update_manufacturer(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('manufacturer')
  else:return view.keep_away()

edit_methods = {
  'user': edit_user_self,
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
  if check_auth(methods.UserDelete):
    man = model.User.query.filter_by(id=id).first()
    if man:
      model.db.session.delete(man)
      model.db.session.commit()
      return view.success('user removed')
    else:
      return view.dne('user')
  else:
    return view.keep_away()

def rm_location(id):
  if check_auth(methods.LocationDelete):
    man = model.Location.query.filter_by(id=id).first()
    if man:
      model.db.session.delete(man)
      model.db.session.commit()
      return view.success('location removed')
    else:
      return view.dne('location')
  else:
    return view.keep_away()

def rm_item(id):
  if check_auth(methods.ItemDelete):
    man = model.Item.query.filter_by(id=id).first()
    if man:
      model.db.session.delete(man)
      model.db.session.commit()
      return view.success('item removed')
    else:
      return view.dne('location')
  else:
    return view.keep_away()

def rm_asset(id):
  if check_auth(methods.AssetDelete):
    man = model.Asset.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('asset removed')
  else:
    return view.keep_away()

def rm_inv(id):
  if check_auth(methods.InvDelete):
    man = model.Inventory.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('inventory removed')
  else:
    return view.keep_away()

def rm_building(id):
  if check_auth(methods.LocBuildEdit):
    man = model.LocationBuilding.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('building removed')
  else:
    return view.keep_away()

def rm_category(id):
  if check_auth(methods.ItemCatEdit):
    man = model.ItemCategory.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('category removed')
  else:
    return view.keep_away()

def rm_manufacturer(id):
  if check_auth(methods.ItemManEdit):
    man = model.ItemManufacturer.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('manufacturer removed')
  else:
    return view.keep_away()


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
