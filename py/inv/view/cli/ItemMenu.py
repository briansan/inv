"""
  @file   ItemMenu.py
  @author Brian Kim
  @brief  defines the command-line interface for the item menu
"""

from inv.model.Permissions import Permissions

class ItemMenu():
  class Delegate():
    """
    a set of methods that should be defined by the using
    class in order to respond to interface events
    """
    def itemMenuCheckUserPermission( self, action ):
      """
      determine whether a user has permission
      to perform a certain action
      """
      return False

    #
    # view methods
    #
    def itemMenuListAll( self, menu ):
      """
      return: all items in the db
      """
      return []

    #
    # edit methods
    #
    def itemMenuWantsEdit( self, item ):
      """
      receives the item that has been modified
      return: 0 for success, negative num for error
      """
      pass

    #
    # add/remove methods
    # 
    def itemMenuWantsAdd( self, item ):
      """
      receives the item that wants to be created (no id)
      """
      pass

    def itemMenuWantsDelete( self, item ):
      """
      receives the item that has wants to be deleted 
      return: 0 for success, negative num for error
      """
      pass

    #
    # view methods
    #
    def itemMenuLookupByManufacturer( self, manufacturer ):
      """
      looking up items by manufacturer
      return: a list of matching items
      """
      return []

    def itemMenuLookupByCategory( self, category ):
      """
      looking up items by manufacturer
      return: a list of matching items
      """
      return []

  """
  Menu class definition
  """

  def main( self, delegate=Delegate() ):
    # set the delegate
    self.delegate = delegate
    # set default option
    opt = 0
    while opt != 5:
      print "============"
      print "Item Menu"
      print "============"
      print "1. View"
      print "2. Edit"
      print "3. Add"
      print "4. Remove"
      print "5. Back"
      opt = read_int('Select an option: ')

      if opt == 1 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemRead):
        self.viewMenu()
      elif opt == 2 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemUpdate):
        self.editMenu()
      elif opt == 3 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemCreate):
        self.addMenu()
      elif opt == 4 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemRemove):
        self.deleteMenu()
      elif opt != 5:
        print "Invalid option, try again..."
        
 
  def selectItem( self ):
    print "============"
    print "List Items "
    print "============"
    print "1. Lookup by Category"
    print "2. Lookup by Manufacturer"
    print "3. List all"

    opt = read_int('Select an option: ')
    if opt == 1:
      self.delegate.itemMenuLookupByManufacturer()
    elif opt == 2:
      self.delegate.itemMenuLookupByCategory()
    elif opt == 3:
      self.delegate.itemMenuListAll()
    else:
      y = self.selectItem()
    return y

  def viewMenu( self ):
    pass
 
  def editMenu( self ):
    self.default()

  def addMenu( self ):
    self.default()

  def deleteMenu( self ):
    self.default()
