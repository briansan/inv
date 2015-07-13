"""
  @file   inv/api/methods.py
  @author Brian Kim
  @brief  this module defines the list of api methods supported by inv
          as well as the authorization scheme of user groups
"""

from model import *

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

def create_location(x):
  """
  @param x dict key/value pairs of the location to add
  """
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

def read_location_by_building(x):
  x = Location.query.filter(Location.building.has(name=x)).all()
  return list_obj2dict(x)

def read_location_all():
  x = Location.query.filter_by().all()
  return list_obj2dict(x)

"""
 Item methods
"""

def create_category(x):
  """
   @param x str the name of the building
   @return y LocationBuilding the object that was placed into the db or None for failure
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

def read_category_all():
  """
   @return list of dict representation of all item manufacturers
  """
  return list_obj2dict(ItemManufacturer.query.filter_by().all())

def create_item(x):
  """
   @param x dict key/value pairs of the item to add
  """
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

def read_item_by_category(x):
  x = Item.query.filter(Item.category.has(name=x)).all()
  return list_obj2dict(x)

def read_item_by_manufacturer(x):
  x = Item.query.filter(Item.manufacturer.has(name=x)).all()
  return list_obj2dict(x)

def read_item_by_model(x):
  x = Item.query.filter_by(model=x).all()
  return list_obj2dict(x)

def read_item_all():
  x = Item.query.filter_by().all()
  return list_obj2dict(x)

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

