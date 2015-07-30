"""
 @file   inv/api/app.py
 @author Brian Kim
 @brief  top level server script
"""

from flask import Flask, session, request, Blueprint, jsonify, g

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

@api.route('/asset/<id>/img', methods=['GET','POST','PUT','DELETE'])
@requires_auth
def asset_img():
  if is_create():
    y = 'create asset img'
  elif is_read():
    y = 'read asset img'
  elif is_update():
    y = 'update asset img'
  elif is_delete():
    y = 'delete asset img'
  else:
    y = view.invalid_method()
  return y

@api.route('/asset/<id>/img/thumbnail', methods=['GET'])
@requires_auth
def asset_img_thumbnail():
  if is_read():
    y = 'read asset img thumbnail'
  else:
    y = view.invalid_method()
  return y
  
@api.route('/asset/<id>/receipt', methods=['GET','POST','PUT','DELETE'])
@requires_auth
def asset_receipt():
  if is_create():
    y = 'create asset img'
  elif is_read():
    y = 'read asset img'
  elif is_update():
    y = 'update asset img'
  elif is_delete():
    y = 'delete asset img'
  else:
    y = view.invalid_method()
  return y

@api.route('/asset/<id>/img/thumbnail', methods=['GET'])
@requires_auth
def asset_receipt_thumbnail():
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

def create_app(conf):
  """
   use this method to create and instance of the app for serving
  """
  # initialize and configure the app
  app = Flask(__name__)
  app.config.from_pyfile(conf)
  # connect the model to the app
  model.db.init_app(app)
  with app.app_context():
    model.db.create_all()
  # register blueprints
  app.register_blueprint(api, url_prefix='/api/v1')
  return app

if __name__=="__main__":
  create_app('conf/debug.cfg').run(host='0.0.0.0')
