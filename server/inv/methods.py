"""
  @file   inv/api/methods.py
  @author Brian Kim
  @brief  this module defines the list of api methods supported by inv
          as well as the authorization scheme of user groups
"""

from model import *
from datetime import datetime

# definition of the methods
def save():
  db.session.commit()

def list_obj2dict(x):
  """
   converts a list of model objects to dictionaries
  """
  return [dict(y) for y in x]
  
"""
 User methods
"""

def read_user(uid):
  """
   @param id int the id of the user
  """
  return User.query.filter_by(uid=uid).first()

def read_user_all():
  return list_obj2dict(User.query.filter_by().all())

def delete_user(uid):
  u = User.query.filter_by(uid=uid).first()
  if not u: return False
  db.session.delete(u)
  save()
  return True

"""
 Location methods
"""

def create_building(x):
  """
   @param x str the name of the building
   @return y LocationBuilding the object that was placed into the db or None for failure
  """
  y = None
  exists = read_building(x) 
  if not exists:
    y = LocationBuilding(x)
    db.session.add(y)
    save()
  return y

def read_building(x):
  """
   @param x str the name of the building
   @return y LocationBuilding or None 
  """
  return LocationBuilding.query.filter_by(name=x).first()

def read_building_all():
  """
   @return list of dict representation of LocationBuildings
  """
  return list_obj2dict(LocationBuilding.query.filter_by().all())
  
def update_building(id,x):
  """
   @param id int the id of the building
   @param x str the new name of the building
   @return building LocationBuilding or None
  """
  building = LocationBuilding.query.filter_by(id=id).first()
  if not building: return None
  building.name = x
  save()
  return building

def delete_building(id):
  """
   @param id int the id of the building to delete
   @return bool True for success, False for failure
  """
  building = LocationBuilding.query.filter_by(id=id).first()
  if not building: return False
  db.session.delete(building)
  save()
  return True

def count_all_location(by):
  return 0
   
def count_location(by,id):
  return 0
  
def create_location(x):
  """
  @param x dict key/value pairs of the location to add
  @return y Location the object that was placed into the db or None for failure
  """
  y = None
  exists = Location.query.filter(Location.building.has(name=x['building']),Location.room.is_(x['room'])).first()
  if not exists:
    # get the values
    building = read_building(x['building'])
    room = x['room']
    # create a building entry if it doesn't exist
    if not building:
      building = create_building(x['building'])
    # create and add the location
    y = Location(building,room)
    db.session.add(y)
    save()
  return y

def read_location_all():
  x = Location.query.filter_by().all()
  return list_obj2dict(x)

def read_location(id):
  return Location.query.filter_by(id=id).first()

def update_location(id,x):
  """
   @param id int the id of the building
   @param x dict key/value pairs of the updated values
   @return loc Location or None
  """
  loc = read_location(id)
  if not loc: return None
  # building name
  new_build = x.get('building')
  if loc.building.name != new_build:
    build = read_building(new_build)
    build = create_building(new_build) if not build else build
    loc.building = build
  # room number
  loc.room = x.get('room')
  save()
  return loc

def delete_location(id):
  """
   @param id int the id of the location to delete
   @return bool True for success, False for failure
  """
  loc = Location.query.filter_by(id=id).first()
  if not loc: return False
  db.session.delete(loc)
  save()
  return True

"""
 Item methods
"""

def create_category(x):
  """
   @param x str the name of the building
   @return y ItemCategory the object that was placed into the db or None for failure
  """
  y = None
  exists = read_category(x) 
  if not exists:
    y = ItemCategory(x)
    db.session.add(y)
    save()
  return y

def read_category(x):
  """
   @param x str the name of the category
   @return y ItemCategory or None 
  """
  return ItemCategory.query.filter_by(name=x).first()

def read_category_all():
  """
   @return list of dict representation of all item categories
  """
  return list_obj2dict(ItemCategory.query.filter_by().all())

def update_category(id,x):
  """
   @param id int the id of the category
   @param x str the new name of the category
   @return cat Category or None
  """
  cat = Category.query.filter_by(id=id).first()
  if not cat: return None
  # category name
  cat.name = x.get('name')
  save()
  return cat

def delete_category(id):
  """
   @param id int the id of the category to delete
   @return bool True for success, False for failure
  """
  cat = Category.query.filter_by(id=id).first()
  if not cat: return False
  db.session.delete(cat)
  save()
  return True
  
def create_manufacturer(x):
  """
   @param x str the name of the building
   @return y LocationBuilding the object that was placed into the db or None for failure
  """
  y = None
  exists = read_manufacturer(x) 
  if not exists:
    y = ItemManufacturer(x)
    db.session.add(y)
    save()
  return y

def read_manufacturer(x):
  """
   @param x str the name of the manufacturer
   @return y ItemManufacturer or None 
  """
  return ItemManufacturer.query.filter_by(name=x).first()

def read_manufacturer_all():
  """
   @return list of dict representation of all item manufacturers
  """
  return list_obj2dict(ItemManufacturer.query.filter_by().all())

def update_manufacturer(id,x):
  """
   @param id int the id of the manufacturer
   @param x str the new name of the manufacturer
   @return man ItemManufacturer or None
  """
  man = ItemManufacturer.query.filter_by(id=id).first()
  if not man: return None
  # manufacturer name
  man.name = x.get('name')
  save()
  return man

def delete_manufacturer(id):
  """
   @param id int the id of the manufacturer to delete
   @return bool True for success, False for failure
  """
  man = ItemManufacturer.query.filter_by(id=id).first()
  if not man: return False
  db.session.delete(man)
  save()
  return True

def item_exists(x):
  category = Item.category.has(name=x['category'])
  manufacturer = Item.manufacturer.has(name=x['manufacturer'])
  model = Item.model.is_(x['model'])
  return Item.query.filter(category,manufacturer,model).first()

def create_item(x):
  """
   @param x dict key/value pairs of the item to add
  """
  y = None
  if not item_exists(x):
    # get the values
    category = read_category(x['category'])
    manufacturer = read_manufacturer(x['manufacturer'])
    model = x['model']
    # create a building entry if it doesn't exist
    if not category:
      category = create_category(x['category'])
    if not manufacturer:
      manufacturer = create_manufacturer(x['manufacturer'])
    # create and add the item
    y = Item(category,manufacturer,model)
    db.session.add(y)
    save()
  return y

def read_item_all():
  x = Item.query.filter_by().all()
  return list_obj2dict(x)

def read_item(id):
  return Item.query.filter_by(id=id).first()

def update_item(id,x):
  """
   @param id int the id of the item
   @param x dict key/value pairs of the updated values
   @return i Item or None
  """
  i = read_item(id)
  if not i: return None
  # item category
  new_cat = x.get('category')
  if i.category.name != new_cat:
    cat = read_category(new_cat)
    cat = create_category(new_cat) if not cat else cat
    i.category = cat
  # item manufacturer
  new_man = x.get('manufacturer')
  if i.manufacturer.name != new_man:
    man = read_manufacturer(new_man)
    man = create_manufacturer(new_man) if not man else man
    i.manufacturer = man
  # item model
  i.model = x.get('model')
  save()
  return i

def delete_item(id):
  """
   @param id int the id of the item to delete
   @return bool True for success, False for failure
  """
  i = read_item(id)
  if not i: return False
  db.session.delete(i)
  save()
  return True

"""
  asset methods
"""

def asset_exists(x):
  return Asset.query.filter(Asset.tag_ece.is_(x['tag_ece'])).first()

def create_asset(x):
  """
   @param x dict key/value pairs of the asset to add
  """
  y = None
  if not asset_exists(x):
    # get the values
    ece = x['tag_ece']
    vu = x['tag_vu']
    unit = x['tag_unit']
    svc = x['tag_svc']
    serial = x['serial']

    status = x['status']
    item_id = x['item'] #
    price = x['price']
    ip = x['ip']
    comments = x['comments']

    purchased_since1970 = x['purchased']
    purchased = datetime.fromtimestamp(purchased_since1970) if purchased_since1970 else None
    owner_id = x['owner'] #
    home_id = x['home'] #

    # convert id's into objects
    item = Item.query.filter_by(id=item_id).first()
    owner = User.query.filter_by(uid=owner_id).first()
    home = Location.query.filter_by(id=home_id).first()
    # create the asset
    y = Asset(ece,status,item,comments,price,ip,purchased,owner,home,vu,unit,svc,serial)
    # insert into db
    db.session.add(y)
    save()
  return y

def read_asset_all():
  return list_obj2dict(Asset.query.filter_by().all())

def read_asset(id):
  return Asset.query.filter_by(tag_ece=id).first()

def update_asset(id,x):
  """
   @param id int the id of the asset to update
   @param x dict key/value pairs of the updated values
   @return a Asset or None
  """
  a = read_asset(id)
  if not a: return None
  if x.get('tag_ece'): a.tag_ece = x.get('tag_ece')
  if x.get('tag_vu'): a.tag_vu = x.get('tag_vu')
  if x.get('tag_unit'): a.tag_unit = x.get('tag_unit')
  if x.get('tag_svc'): a.tag_svc = x.get('tag_svc')
  if x.get('serial'): a.serial = x.get('serial')
  if x.get('status'): a.status = x.get('status')
  if x.get('item'): a.item = read_item(x.get('item'))
  if x.get('price'): a.price = x['price']
  if x.get('ip'): a.ip = x['ip']
  if x.get('comments'): a.comments = x['comments']
  if x.get('purchased'): 
    a.purchased = date.fromtimestamp(x['purchased']) 
  if x.get('owner'):
    a.owner = User.query.filter_by(uid=x['owner']).first()
  if x.get('home'):
    a.home = Location.query.filter_by(id=x['home']).first()
  
  save()
  return a

def delete_asset(id):
  """
   @param id int the id of the asset to delete
  """
  a = read_asset(id)
  if not a: return False
  db.session.delete(a)
  save()
  return True

"""
 inventory methods
"""
def create_inv(x):
  who = read_user(x['who'])
  what = read_asset(x['what'])
  when = datetime.fromtimestamp(x['when'])
  where = read_location(x['where'])
  how = x['how']
  inv = Inventory(who,what,when,where,how)
  db.session.add(inv)
  save()
  return inv

def read_inv(id):
  return Inventory.query.filter_by(id=id).first()

def read_inv_all():
  return list_obj2dict(Inventory.query.filter_by().all())

def read_inv_by_user(id):
  return list_obj2dict(Inventory.query.filter(Inventory.who.has(uid=uid)).all())

def read_inv_by_asset(id):
  return list_obj2dict(Inventory.query.filter(Inventory.what.has(id=id)).all())

def read_inv_by_location(id):
  return list_obj2dict(Inventory.query.filter(Inventory.where.has(id=id)).all())

def read_inv_by_date(date):
  date = datetime.fromtimestamp(date).date()
  return list_obj2dict(Inventory.query.filter(Inventory.when.date() == date).all())

def update_inv(id,x):
  inv = read_inv(id)
  if not inv: return None
  inv.who = User.query.filter_by(uid=x['who'])
  inv.what = Asset.query.filter_by(id=x['what'])
  inv.when = datetime.fromtimestamp(x['when'])
  inv.where = Location.query.filter_by(id=x['where'])
  inv.how = x['how']
  save()
  return inv

def delete_inv(id):
  inv = read_inv(id)
  if not inv: return False
  db.session.delete(inv)
  save()

