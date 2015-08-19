"""
  @file   inv/api/controller.py
  @author Brian Kim
  @brief  this module defines the functionality of 
          the methods described by inv/api/methods.py
"""

from flask import request, session, g, jsonify, current_app, abort
from werkzeug import secure_filename
from PIL import Image

import auth, methods, model, view, util
import base64, datetime, os

"""
  authentication methods
"""

def root():
  expire = None
  if util.is_create():
    expire = request.form.get('expire')
  token = g.user.generate_auth_token(expire)
  return jsonify({'token':token.decode('ascii')})

"""
  authorization methods
"""
def check_auth(method):
  try:
    p = g.user.perm
  except:
    return False
  a = auth.Authorization(p)
  return a.chk(method)

"""
  location methods
"""

def parse_location():
  y = {}
  try:
    y['building'] = request.form['building']
    y['room'] = request.form['room']
  except KeyError as k:
    raise Exception(k.args[0])
  return y

def add_location():
  if check_auth(auth.SubentityModify):
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

def view_location(id=0):
  if check_auth(auth.SubentityView):
    if id is 0:
      x = methods.read_location_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = methods.read_location(id)
      if not y: return view.dne('location')
      y = dict(y)
    return view.success(y)
  else:
    return view.keep_away()

def edit_location(id):
  if check_auth(auth.SubentityModify):
    try:
      x = parse_location()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_location(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('location')
  else: return view.keep_away()

def rm_location(id):
  if check_auth(auth.SubentityModify):
    man = model.Location.query.filter_by(id=id).first()
    if man:
      model.db.session.delete(man)
      model.db.session.commit()
      return view.success('location removed')
    else:
      return view.dne('location')
  else:
    return view.keep_away()

"""
  building methods
"""

def add_building():
  if check_auth(auth.LabelModify):
    try:
      man = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    # add the building
    x = methods.create_building(man)
    return view.success(dict(x)) if x else view.already_exists('building')
  else:
    return view.keep_away()

def view_building(id=0):
  if check_auth(auth.LabelView):
    y = methods.read_building_all()
    return view.success(y)
  else:
    return view.keep_away()

def edit_building(id):
  if check_auth(auth.LabelModify):
    try:
      x = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    y = methods.update_building(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('building')
  else:return view.keep_away()

def rm_building(id):
  if check_auth(auth.LabelModify):
    man = model.LocationBuilding.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('building removed')
  else:
    return view.keep_away()

"""
  item methods
"""

def parse_item():
  y = {}
  try:
    y['category'] = request.form['category']
    y['manufacturer'] = request.form['manufacturer']
    y['model'] = request.form['model']
  except KeyError as k:
    raise Exception(k.args[0])
  return y

def add_item():
  if check_auth(auth.SubentityModify):
    try:
      item = parse_item()
    except Exception as k:
      return view.missing_field(k.message)
    # add the item
    x = methods.create_item(item)
    return view.success(dict(x)) if x else view.already_exists('item')
  else:
    return view.keep_away()

def view_item(id=0):
  if check_auth(auth.SubentityView):
    if id is 0:
      x = methods.read_item_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = methods.read_item(id)
      if not y: return view.dne('item')
      y = dict(y)
    return view.success(y)
  else:
    return view.keep_away()

def edit_item(id):
  if check_auth(auth.SubentityModify):
    try:
      x = parse_item()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_item(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('item')
  else: return view.keep_away()

def rm_item(id):
  if check_auth(auth.SubentityModify):
    man = model.Item.query.filter_by(id=id).first()
    if man:
      model.db.session.delete(man)
      model.db.session.commit()
      return view.success('item removed')
    else:
      return view.dne('location')
  else:
    return view.keep_away()


"""
  category methods
"""

def add_category():
  if check_auth(auth.LabelModify):
    try:
      man = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    # add the category
    x = methods.create_category(man)
    return view.success(dict(x)) if x else view.already_exists('category')
  else:
    return view.keep_away()

def view_category(id=0):
  if check_auth(auth.LabelView):
    y = methods.read_category_all()
    return view.success(y)
  else:
    return view.keep_away()

def edit_category(id):
  if check_auth(auth.LabelModify):
    try:
      x = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    y = methods.update_category(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('category')
  else:return view.keep_away()

def rm_category(id):
  if check_auth(auth.LabelModify):
    man = model.ItemCategory.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('category removed')
  else:
    return view.keep_away()

"""
  manufacturer methods
"""

def add_manufacturer():
  if check_auth(auth.LabelModify):
    try:
      man = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    # add the manufacturer
    x = methods.create_manufacturer(man)
    return view.success(dict(x)) if x else view.already_exists('manufacturer')
  else:
    return view.keep_away()

def view_manufacturer(id=0):
  if check_auth(auth.LabelView):
    y = methods.read_manufacturer_all()
    return view.success(y)
  else:
    return view.keep_away()

def edit_manufacturer(id):
  if check_auth(auth.LabelModify):
    try:
      x = request.form['name']
    except KeyError as k:
      return view.missing_field(k.args[0])
    y = methods.update_manufacturer(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('manufacturer')
  else:return view.keep_away()

def rm_manufacturer(id):
  if check_auth(auth.LabelModify):
    man = model.ItemManufacturer.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('manufacturer removed')
  else:
    return view.keep_away()

"""
  asset img
"""
ALLOWED_EXTENSIONS = set(['png','jpeg','jpg'])

def allowed_file(fname):
  return '.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

def get_asset_img(id):
  if check_auth(auth.EntityView):
    try:
      fname = util.img_path(id.upper())
      return view.send_img(fname)
    except:
      return view.dne('image for '+id)
  else:
    return view.keep_away()

def get_asset_thumbnail(id):
  if check_auth(auth.EntityView):
    try:
      fname = util.thumbnail_path(id.upper())
      return view.send_img(fname)
    except:
      return view.dne('image thumbnail for '+id)
  else:
    return view.keep_away()

def get_asset_receipt(id):
  if check_auth(auth.EntityView):
    try:
      fname = util.receipt_path(id.upper())
      return view.send_img(fname)
    except:
      return view.dne('receipt image for '+id)
  else:
    return view.keep_away()

def set_asset_img(id): 
  if check_auth(auth.EntityModify):
    asset = methods.read_asset(id.upper())
    if asset is None:
      return view.dne('asset')
    # asset exists so set the img
    fs = request.files['file']
    if fs and allowed_file(fs.filename):
      try:
        # save it to the tmp directory
        filename = secure_filename(fs.filename)
        tmp = '/tmp/'+filename
        fs.save(tmp)
        # process it using pil
        img = Image.open(tmp)
        # do some size processing
        norm = 1024
        w,h = img.size
        v = h > w
        ar = float(h)/w if v else float(w)/h
        size = (ar*norm,norm) if v else (norm,ar*norm)
        # resize to norm
        img.thumbnail(size,Image.ANTIALIAS)
        img.save(util.img_path(asset.tag_ece),'png')
        # process for thumbnail
        sm = 64
        size = (ar*sm,sm) if v else (sm,ar*sm)
        img.thumbnail(size,Image.ANTIALIAS)
        img.save(util.thumbnail_path(asset.tag_ece),'png')
        return view.success(dict(asset))
      except:
        abort(500)
    else:
      return view.missing_field('img')
  else: return view.keep_away()

def set_asset_receipt(id):
  if check_auth(auth.EntityModify):
    asset = methods.read_asset(id.upper())
    if asset is None:
      return view.dne('asset '+id)
    # asset exists so set the receipt img
    fs = request.files['file']
    if fs and allowed_file(fs.filename):
      try:
        # save it to the tmp directory
        filename = secure_filename(fs.filename)
        tmp = '/tmp/'+filename
        fs.save(tmp)
        # process it
        img = Image.open(tmp)
        # do some size processing
        norm = 1024
        w,h = img.size
        v = h>w
        ar = float(h)/w if v else float(w)/h
        size = (ar*norm,norm) if v else (norm,ar*norm)
        # resize to norm
        img.thumbnail(size,Image.ANTIALIAS)
        img.save(util.receipt_path(asset.tag_ece),'png')
        return view.success(dict(asset))
      except:
        abort(500)
    else: return view.missing_field('receipt')
  else: view.keep_away()

"""
  asset methods
"""

def add_asset():
  if check_auth(auth.EntityModify):
    try:
      asset = parse_asset()
    except Exception as k:
      return view.missing_field(k.message)
    # add the asset
    x = methods.create_asset(asset)
    # add an initial inv (if requested)
    if (request.form.get('doinv') in ["true","True"]) and x:
      inv = {'who':x.owner_id,'what':x.tag_ece,'when':int(datetime.datetime.now().strftime("%s")),'where':x.home_id,'how':x.status}
      y = methods.create_inv(inv)
      update_asset(y)
    return view.success(dict(x)) if x else view.already_exists('asset')
  else:
    return view.keep_away()

def view_asset(id=0):
  if check_auth(auth.EntityView):
    if id is 0:
      x = methods.read_asset_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = methods.read_asset(id.upper())
      if not y: return view.dne('asset')
      y = dict(y)
    return view.success(y)
  else:
    return view.keep_away()

def edit_asset(id):
  x = methods.read_asset(id.upper())
  own_item = check_auth(auth.EntityModify) and x.owner == g.user.uid
  operator = check_auth(auth.EntityModifyWorld)
  if own_item or operator:
    try:
      x = parse_asset()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_asset(id,x)
    if y: return view.success(dict(y))
    else: return view.dne('asset')
  else: return view.keep_away()

def rm_asset(id):
  if check_auth(auth.EntityModify):
    man = model.Asset.query.filter_by(tag_ece=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('asset removed')
  else:
    return view.keep_away()

def update_asset(inv):
  asset = inv.what
  asset.holder = inv.who
  asset.inventoried = inv.when
  asset.current = inv.where
  asset.status = inv.how

  methods.save()

def parse_asset():
  y = {}
  try:
    # get means optional field, [] means required field
    y['tag_ece'] = request.form['tag_ece'] #
    y['status'] = int(request.form['status']) #
    y['item'] = int(request.form['item']) #
    y['owner'] = str(request.form['owner'].lower())
    y['home'] = int(request.form['home']) #

    y['tag_vu'] = request.form.get('tag_vu')
    y['tag_unit'] = request.form.get('tag_unit')
    y['tag_svc'] = request.form.get('tag_svc')
    y['serial'] = request.form.get('serial')

    y['price'] = request.form.get('price')
    y['price'] = float(y['price']) if y['price'] else None
    y['ip'] = request.form.get('ip')
    y['comments'] = request.form.get('comments')

    y['purchased'] = request.form.get('purchased')
    y['purchased'] = int(y['purchased']) if y['purchased'] else None

    
  except KeyError as k:
    raise Exception(k.args[0])
  return y

"""
  inventory methods
"""

def add_inv():
  if check_auth(auth.EntityModify):
    try:
      inv = parse_inv()
    except Exception as k:
      return view.missing_field(k.message)
    # add the inv
    x = methods.create_inv(inv)
    if x:
      update_asset(x)
    return view.success(dict(x)) if x else view.already_exists('inventory')
  else:
    return view.keep_away()

def view_inv(id=0):
  if check_auth(auth.EntityView):
    if id is 0:
      x = methods.read_inv_all()
      y = filter(x) if len(request.args) > 0 else x
    else:
      y = methods.read_inv(id)
      if not y: return view.dne('inventory')
      y = dict(y)
    return view.success(y)
  else:
    return view.keep_away()

def edit_inv(id):
  x = methods.read_inv(id)
  own_item = check_auth(auth.EntityModify) and x.who == g.user.uid
  operator = check_auth(auth.EntityModifyWorld)
  if own_item or operator:
    try:
      x = parse_inv()
    except Exception as k:
      return view.missing_field(k.message)
    y = methods.update_inv(id,x)
    # check the results
    if y: return view.success(dict(y))
    else: return view.dne('inventory')
  else: return view.keep_away()

def rm_inv(id):
  if check_auth(auth.EntityModify):
    man = model.Inventory.query.filter_by(id=id).first()
    model.db.session.delete(man)
    model.db.session.commit()
    return view.success('inventory removed')
  else:
    return view.keep_away()

def parse_inv():
  y = {}
  try:
    y['who'] = str(request.form['who']).lower()
    y['what'] = request.form['what']
    y['when'] = int(request.form['when'])
    y['where'] = int(request.form['where'])
    y['how'] = int(request.form['how'])
  except KeyError as k:
    raise Exception(k.args[0])
  return y

"""
  user methods
"""

def view_self():
  if check_auth(auth.SubentityView):
    return view.success(dict(g.user))
  else:
    return view.keep_away()

def view_user(uid="bkim11"):
  if check_auth(auth.SubentityView):
    x = methods.read_user(uid)
    if x is None: return view.dne('user '+uid)
    x = check_annon(x)
    y = dict(x)
    return view.success(y)
  else:
    return view.keep_away()

def check_annon(user):
  if not (type(user) is dict):
    user = dict(user)
  if user['annon'] and g.user.grp < 2:
    return User('Annoymous','Missing','No',0,0,"","",True)
  else:
    return user

def view_user_all():
  if check_auth(auth.SubentityView):
    y = methods.read_user_all()
    y = [check_annon(x) for x in y]
    return view.success(y)
  else:
    return view.keep_away()
  
def edit_self():
  if g.user:
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    annon = request.form.get('annon')
    annon = bool(annon) if annon else None
    g.user.fname = fname if fname else g.user.fname
    g.user.lname = lname if lname else g.user.lname
    g.user.phone = phone if phone else g.user.phone
    g.user.email = email if email else g.user.email
    g.user.annon = annon if annon else g.user.annon
    methods.save()
  return view.success(dict(g.user))

def edit_user(id):
  if check_auth(auth.UserModifyWorld):
    user = model.User.query.filter_by(uid=id).first()
    if user:
      grp = request.form.get('grp')
      grp = int(grp) if grp else grp
      user.grp = grp if grp else user.grp
      perm = request.form.get('perm')
      perm = int(perm) if perm else perm
      user.perm = perm if perm else user.perm
      methods.save()
      return view.success(dict(user))
    else:
      return view.dne('user')
  else:
    return view.keep_away()

def rm_user(id):
  if check_auth(auth.UserModifyWorld):
    man = model.User.query.filter_by(uid=uid).first()
    if man:
      model.db.session.delete(man)
      model.db.session.commit()
      return view.success('user removed')
    else:
      return view.dne('user')
  else:
    return view.keep_away()

"""
  filter method
"""

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


