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
                       '/remove/inv/{id}')
}

# definition of default permissions
DefaultStudentPermissions = UserReadSelf | UserUpdateSelf | ItemRead | LocationRead | AssetRead | InvRead
DefaultFacultyPermissions = DefaultStudentPermissions | UserReadWorld | InvCreate 
DefaultOperatorPermissions = DefaultFacultyPermissions | ItemCreate | ItemUpdate |  \
                             LocationCreate | LocationUpdate |  \
                             AssetCreate | AssetUpdate
DefaultAdminPermissions = DefaultOperatorPermissions | UserUpdateWorld | UserDelete | ItemDelete |  \
                          LocationDelete | AssetDelete | InvUpdate | InvDelete
DefaultPermissions = {
  User.Groups.NoGroup: LogInOut,
  User.Groups.Student: DefaultStudentPermissions,
  User.Groups.Faculty: DefaultFacultyPermissions,
  User.Groups.Operator: DefaultOperatorPermissions,
  User.Groups.Admin: DefaultAdminPermissions,
}

# definition of authorization object
class Authorization():
  """
   use this class to pass in a permission integer value
   and parse out the permissions of all the methods
  """
  def __init__(self,val):
    """
     initialize the authorization obj with
     some value equal to the bit string
     of values from above
    """
    self.val = val
  def add(self,val):
    """
     adds a method permission to the value
     variable using a bitwise-or
    """
    self.val |= val
  def chk(self,val):
    """
     checks the presence of a permission
     by doing a bitwise-and and testing for non 0
    """
    return not (self.val & val == 0)
  def rmv(self,val):
    """
     removes a method permission from the value
     by doing a bitwise-and with the permission's bit value
    """
    self.val &= ~val

