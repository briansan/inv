"""
 @file   inv/api/app.py
 @author Brian Kim
 @brief  top level server script
"""

from flask import Flask, session, request, Blueprint, jsonify, g
from flask_sslify import SSLify

import controller, model, view
from auth import auth_ldap
from util import *

api = Blueprint('api',__name__)

@api.route('/', methods=['GET','POST'])
@requires_auth
def root():
  return controller.root()

@api.route('/user', methods=['GET'])
@requires_auth
def user():
  if is_read():
    y = controller.view_self
  else:
    y = view.invalid_method
  return y()

@api.route('/user/<id>', methods=['GET'])
@requires_auth
def user_id(id):
  if is_read():
    y = controller.view_user
  else:
    y = view.invalid_method
  return y(id)
  
@api.route('/item', methods=['GET','POST'])
@requires_auth
def item():
  if is_create():
    y = controller.add_item
  elif is_read():
    y = controller.view_item
  else:
    y = view.invalid_method
  return y()

@api.route('/item/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def item_id(id):
  if is_read():
    y = controller.view_item
  elif is_update():
    y = controller.edit_item
  elif is_delete():
    y = controller.rm_item
  else:
    y = view.invalid_method
  return y(id)

@api.route('/item/category', methods=['GET','POST'])
@requires_auth
def category():
  if is_create():
    y = controller.add_category
  elif is_read():
    y = controller.view_category
  else:
    y = view.invalid_method
  return y()

@api.route('/item/category/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def category_id(id):
  if is_read():
    y = controller.view_category
  elif is_update():
    y = controller.edit_category
  elif is_delete():
    y = controller.rm_category
  else:
    y = view.invalid_method
  return y(id)

@api.route('/item/manufacturer', methods=['GET','POST'])
@requires_auth
def manufacturer():
  if is_create():
    y = controller.add_manufacturer
  elif is_read():
    y = controller.view_manufacturer
  else:
    y = view.invalid_method
  return y()

@api.route('/item/manufacturer/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def manufacturer_id(id):
  if is_read():
    y = controller.view_manufacturer
  elif is_update():
    y = controller.edit_manufacturer
  elif is_delete():
    y = controller.rm_manufacturer
  else:
    y = view.invalid_method
  return y(id)

@api.route('/location', methods=['GET','POST'])
@requires_auth
def location():
  if is_create():
    y = controller.add_location
  elif is_read():
    y = controller.view_location
  else:
    y = view.invalid_method
  return y()

@api.route('/location/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def location_id(id):
  if is_read():
    y = controller.view_location
  elif is_update():
    y = controller.edit_location
  elif is_delete():
    y = controller.rm_location
  else:
    y = view.invalid_method
  return y(id)

@api.route('/location/building', methods=['GET','POST'])
@requires_auth
def building():
  if is_create():
    y = controller.add_building
  elif is_read():
    y = controller.view_building
  else:
    y = view.invalid_method
  return y()

@api.route('/location/building/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def building_id(id):
  if is_read():
    y = controller.view_building(id)
  elif is_update():
    y = controller.edit_building(id)
  elif is_delete():
    y = controller.rm_building(id)
  else:
    y = view.invalid_method()
  return y

@api.route('/asset', methods=['GET','POST'])
@requires_auth
def asset():
  if is_create():
    y = controller.add_asset()
  elif is_read():
    y = controller.view_asset()
  else:
    y = view.invalid_method()
  return y

@api.route('/asset/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def asset_id(id):
  if is_read():
    y = controller.view_asset(id)
  elif is_update():
    y = controller.edit_asset(id)
  elif is_delete():
    y = controller.rm_asset(id)
  else:
    y = view.invalid_method()
  return y

import os
from flask import current_app, redirect, url_for
from werkzeug import secure_filename
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

@api.route('/asset/img')
@requires_auth
def asset_img_form():
  return '''
   <!DOCTYPE html>
   <title>Upload Img</title>
   <h1>Upload new file</h1>
   <form action="/api/v1/asset/EE00382/receipt" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
   </form>
  '''

def allowed_file(filename):
  return '.' in filename and \
         filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@api.route('/asset/<id>/img', methods=['GET','POST'])
@requires_auth
def asset_img(id):
  if is_create():
    return controller.set_asset_img(id)
  elif is_read():
    return controller.get_asset_img(id)
  else:
    y = view.invalid_method()
  return y

@api.route('/asset/<id>/img/thumbnail', methods=['GET'])
@requires_auth
def asset_img_thumbnail(id):
  if is_read():
    y = controller.get_asset_thumbnail(id)
  else:
    y = view.invalid_method()
  return y
  
@api.route('/asset/<id>/receipt', methods=['GET','POST'])
@requires_auth
def asset_receipt(id):
  if is_create():
    y = controller.set_asset_receipt(id)
  elif is_read():
    y = controller.get_asset_receipt(id)
  else:
    y = view.invalid_method()
  return y

@api.route('/asset/<id>/receipt/thumbnail', methods=['GET'])
@requires_auth
def asset_receipt_thumbnail(id):
  if is_read():
    y = 'read asset img thumbnail'
  else:
    y = view.invalid_method()
  return y()
  
@api.route('/inv', methods=['GET','POST'])
@requires_auth
def inv():
  if is_create():
    y = controller.add_inv()
  elif is_read():
    y = controller.view_inv()
  else:
    y = view.invalid_method()
  return y

@api.route('/inv/<id>', methods=['GET','PUT','DELETE'])
@requires_auth
def inv_id(id):
  if is_read():
    y = controller.view_inv(id)
  elif is_update():
    y = controller.edit_inv(id)
  elif is_delete():
    y = controller.rm_inv(id)
  else:
    y = view.invalid_method()
  return y

