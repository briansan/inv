"""
  @file   inv/api/methods.py
  @author Brian Kim
  @brief  this module defines the list of api methods supported by inv
          as well as the authorization scheme of user groups
"""

from model import *
from datetime import datetime

# definition of methods as bits
LogInOut = 0
UserReadSelf  = 1 << 0
UserReadWorld = 1 << 1
UserUpdateSelf  = 1 << 2
UserUpdateWorld = 1 << 3
UserDelete = 1 << 4
ItemCreate = 1 << 5
ItemRead   = 1 << 6
ItemUpdate = 1 << 7
ItemDelete = 1 << 8
LocationCreate = 1 << 9
LocationRead   = 1 << 10
LocationUpdate = 1 << 11
LocationDelete = 1 << 12
AssetCreate = 1 << 13
AssetRead   = 1 << 14
AssetUpdate = 1 << 15
AssetDelete = 1 << 16
InvCreate   = 1 << 17
InvRead     = 1 << 18
InvUpdate   = 1 << 19
InvDelete   = 1 << 20
LocBuildView = 1 << 21
LocBuildEdit = 1 << 22
ItemCatView  = 1 << 23
ItemCatEdit  = 1 << 24
ItemManView  = 1 << 25
ItemManEdit  = 1 << 26

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

def read_user(id):
  """
   @param id int the id of the user
  """
  return User.query.filter_by(id=id).first()

def read_user_all():
  return list_obj2dict(User.query.filter_by().all())

def update_user_self(x):
  u = User.query.filter_by(id=id).first()
  if not u: return False
  u.fname = x.get('fname')
  u.lname = x.get('lname')
  save()
  return u

def update_user(id,x):
  u = User.query.filter_by(id=id).first()
  if not u: return False
  u.fname = x.get('fname')
  u.lname = x.get('lname')
  u.grp = x.get('grp')
  u.perm = x.get('perm')
  u.start = x.get('start')
  save()
  return u

def delete_user(id):
  u = User.query.filter_by(id=id).first()
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
  manufacturer = Item.category.has(name=x['manufacturer'])
  model = Item.category.is_(x['model'])
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
  return Asset.query.filter(Asset.tag.has(ece=x['tag_ece'])).first()

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
    serial = x['tag_serial']
    status = x['status']
    item_id = x['item'] #
    purchased_since1970 = x['purchased']
    purchased = datetime.fromtimestamp(purchased_since1970) if purchased_since1970 else None
    img = x['img']
    owner_id = x['owner'] #
    holder_id = x['holder'] #
    price = x['price']
    receipt = x['receipt']
    ip = x['ip']
    comments = x['comments']
    home_id = x['home'] #
    current_id = x['current'] #
    # convert id's into objects
    tag = AssetInfo(ece,vu,unit,svc,serial)
    item = Item.query.filter_by(id=item_id).first()
    owner = User.query.filter_by(id=owner_id).first()
    holder = User.query.filter_by(id=holder_id).first()
    home = Location.query.filter_by(id=home_id).first()
    current = Location.query.filter_by(id=current_id).first()
    # create the asset
    y = Asset(tag,status,item,purchased,img,owner,holder,price,receipt,ip,comments,home,current)
    # insert into db
    db.session.add(y)
    save()
  return y

def read_asset_all():
  return list_obj2dict(Asset.query.filter_by().all())

def read_asset(id):
  return Asset.query.filter_by(id=id).first()

def update_asset(id,x):
  """
   @param id int the id of the asset to update
   @param x dict key/value pairs of the updated values
   @return a Asset or None
  """
  a = read_asset(id)
  if not a: return None
  a.tag.ece = x['tag_ece']
  a.tag.vu = x['tag_vu']
  a.tag.unit = x['tag_unit']
  a.tag.svc = x['tag_svc']
  a.tag.serial = x['tag_serial']
  a.status = x['status']
  a.item = Item.query.filter_by(id=x['item']).first()
  a.purchased = date.fromtimestamp(x['purchased']) if x['purchased'] else None
  a.img = x['img']
  a.owner = User.query.filter_by(id=x['owner'])
  a.holder = User.query.filter_by(id=x['holder'])
  a.price = x['price']
  a.receipt = x['receipt']
  a.ip = x['ip']
  a.comments = x['comments']
  a.home = User.query.filter_by(id=x['home'])
  a.current = User.query.filter_by(id=x['current'])
  save()
  return a

def delete_asset(id):
  """
   @param id int the id of the asset to delete
  """
  a = read_asset(id)
  if not a: return False
  db.session.delete(a.tag)
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
  inv = Inventory(who,what,when,where)
  db.session.add(inv)
  save()
  return inv

def read_inv(id):
  return Inventory.query.filter_by(id=id).first()

def read_inv_all():
  return list_obj2dict(Inventory.query.filter_by().all())

def read_inv_by_user(id):
  return list_obj2dict(Inventory.query.filter(Inventory.who.has(id=id)).all())

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
  inv.who = User.query.filter_by(id=x['who'])
  inv.what = Asset.query.filter_by(id=x['what'])
  inv.when = datetime.fromtimestamp(x['when'])
  inv.where = Location.query.filter_by(id=x['where'])
  save()
  return inv

def delete_inv(id):
  inv = read_inv(id)
  if not inv: return False
  db.session.delete(inv)
  save()

# dictionary of information about the methods
def method_desc(name,desc,usage,supports,more=None):
  return {'name':name,'desc':desc,'supports':supports,'usage':usage,'more':more}

info = {
LogInOut: method_desc('Login',
                      'authenticate into inv',
                      'POST',
                      '/login',
                      {'uname':'username','passwd':'password'}),
UserReadSelf: method_desc('View Self',
                          'read user information about yourself',
                          'GET',
                          '/view/user'),
UserReadWorld: method_desc('View World',
                            'read user information about other people',
                            'GET',
                            '/view/user?{query}',
                            User.info()),
UserUpdateSelf: method_desc('Edit Self',
                             'update user information about yourself',
                             'POST',
                             '/edit/user',
                             {'fname':'first name','lname':'last name'}),
UserUpdateWorld: method_desc('Edit World',
                             'update user information about other people',
                             'POST',
                             '/edit/user/{id}',
                             User.info()),
UserDelete: method_desc('Remove World',
                        'delete a user from inv',
                        'DELETE',
                        '/remove/user/{id}'),
ItemCreate: method_desc('Add Item',
                        'create an item',
                        'POST',
                        '/add/item',
                        Item.info()),
ItemRead: method_desc('View Item',
                      'read information about an item',
                      'GET',
                      '/view/item?{query}',
                      Item.info()),
ItemUpdate: method_desc('Edit Item',
                        'update information of an item',
                        'POST',
                        '/edit/item/{id}',
                        Item.info()),
ItemDelete: method_desc('Remove Item',
                        'delete an item from inv',
                        'DELETE',
                        '/remove/item/{id}'),
LocationCreate: method_desc('Add Location',
                            'create a location',
                            'POST',
                            '/add/location',
                            Location.info()),
LocationRead: method_desc('View Location',
                          'read information about a location',
                          'GET',
                          '/view/location?{query}',
                          Location.info()),
LocationUpdate: method_desc('Edit Location',
                            'update information about a location',
                            'POST',
                            '/edit/location/{id}',
                            Location.info()),
LocationDelete: method_desc('Remove Location',
                            'delete a location from inv',
                            'DELETE',
                            '/remove/location/{id}'),
AssetCreate: method_desc('Add Asset',
                         'creates an asset',
                         'POST',
                         '/add/asset',
                         Asset.info()),
AssetRead: method_desc('View Asset',
                       'read information about an asset',
                       'GET',
                       '/view/asset?{query}',
                       Asset.info()),
AssetUpdate: method_desc('Edit Asset',
                         'update information about an asset',
                         'POST',
                         '/edit/asset/{id}',
                         Asset.info()),
AssetDelete: method_desc('Remove Asset',
                         'delete an asset from inv',
                         'DELETE',
                         '/remove/asset/{id}'),
InvCreate: method_desc('Add Inventory',
                       'create an inventory record',
                       'POST',
                       '/add/inv',
                       Inventory.info()),
InvRead: method_desc('View Inventory',
                     'read the inventory log',
                     'GET',
                     '/view/inv?{query}',
                     Inventory.info()),
InvUpdate: method_desc('Edit Inventory',
                       'update an inventory record',
                       'POST',
                       '/edit/inv/{id}',
                       Inventory.info()),
InvDelete: method_desc('Remove Inventory',
                       'deletes an inventory record from inv',
                       'DELETE',
                       '/remove/inv/{id}'),
LocBuildView: method_desc('View Location Building',
                          'read the list of buildings',
                          'GET',  
                          '/view/building?{query}'),
LocBuildEdit: method_desc('Edit Location Building',
                          'add, modify, or remove a building',
                          'POST', 
                          '/add/building OR /edit/building/{id} OR /rm/building/{id}',
                          LocationBuilding.info()),
ItemCatView: method_desc('View Item Category',
                          'read the list of item categories',
                          'GET',  
                          '/view/category?{query}'),
ItemCatEdit: method_desc('Edit Item Category',
                          'add, modify, or remove an item category',
                          'POST', 
                          '/add/category OR /edit/category/{id} OR /rm/category/{id}',
                          ItemCategory.info()),
ItemManView: method_desc('View Item Manufacturer',
                          'read the list of item manufacturers',
                          'GET',  
                          '/view/manufacturer?{query}'),
ItemManEdit: method_desc('Edit Item Manufacturer',
                         'add, modify, or remove an item manufacturer',
                         'POST',
                         '/add/manufacturer OR /edit/manufacturer/{id} OR /rm/manufacturer/{id}',
                         ItemManufacturer.info()),
}

