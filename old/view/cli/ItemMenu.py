"""
  @file   ItemMenu.py
  @author Brian Kim
  @brief  defines the command-line interface for the item menu
"""

from inv.model.Permissions import Permissions
from inv.model.Item import Item
from common import *

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
      return True

    #
    # view methods
    #
    def itemMenuListAll( self):
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
      return -1

    #
    # add/remove methods
    # 
    def itemMenuWantsAdd( self, item ):
      """
      receives the item that wants to be created (no id)
      """
      return -1

    def itemMenuWantsDelete( self, item ):
      """
      receives the item that has wants to be deleted 
      return: 0 for success, negative num for error
      """
      return -1

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
  def __init__( self, delegate=Delegate() ):
    """
    just looking to set the delegate
    """
    self.delegate=delegate

  def start( self ):
    """
    prints out the item main menu 
    """
    # set default option
    opt = 0
    # display the menu repeatedly until back is selected
    while opt != 5:
      print ""
      print "============"
      print "Item Menu"
      print "============"
      print "1. View"
      print "2. Edit"
      print "3. Add"
      print "4. Remove"
      print "5. Back"
      print ""
      opt = read_int('Select an option: ')

      # go through all the option values and check permissions
      if opt == 1 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemRead):
        self.viewMenu()
      elif opt == 2 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemUpdate):
        self.editMenu()
      elif opt == 3 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemCreate):
        self.addMenu()
      elif opt == 4 and self.delegate.itemMenuCheckUserPermission(Permissions.ItemDelete):
        self.removeMenu()
      elif opt != 5:
        print "Invalid option (maybe insufficient permissions?), try again..."
        
  def listItemMenu( self ):
    """
    displays a menu of possible ways to search through items
    and then returns a list of those items
    """
    print ""
    print "============"
    print "List Items "
    print "============"
    print "1. List all"
    print "2. Lookup by Category"
    print "3. Lookup by Manufacturer"
    print ""
    opt = read_int('Select an option: ')
    if not opt:
      return []

    # go through the options...
    if opt == 1: # list all items
      y = self.delegate.itemMenuListAll()
    elif opt == 2: # lookup by category
      print ""
      x = read_str("Category: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.itemMenuLookupByCategory(x)
    elif opt == 3: # lookup by manufacturer
      print ""
      x = read_str("Manufacturer: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.itemMenuLookupByManufacturer(x)
    else: # any other option will repeat this menu
      y = self.listItemMenu()
    return y

  def displayItemInfo( self, x=None ):
    """
    displays the contents of an item
    """
    # check for null obj
    if x == None: 
      return

    # display the item info until back
    print ""
    print "==================="
    print "Item Information"
    print "==================="
    print "Category: " + x.category
    print "Manufacturer: " + x.manufacturer
    print "Model: " + x.model
      
  def getItem( self ):
    """
    convenience method to retrieve an item from a list search
    """
    itemlist = self.listItemMenu()
    if itemlist == None:
      return None
    item = select_obj_from_list(itemlist)
    return item
    
  def itemViewMenu( self, x ):
    """
    method to display a menu after viewing an item
    """
    # display the information
    self.displayItemInfo(x)

    # request action
    opt = 0
    while opt != 3:
      print ""
      print "What would you like to do?"
      print "1. edit"
      print "2. remove"
      print "3. back"
      print ""
      opt = read_int('Select an option: ')
      
      if opt == 1: # edit
        self.editItem(x)
      elif opt == 2: # remove
        if self.removeItem(x):
          return
      elif opt != 3: # other (not back)
        print ""
        print "invalid option, try again..."
        self.itemViewMenu(x) # try again

  def editItemMenu( self, x ):
    """
    method to prompt the editing of the item fields
    """
    if x == None:
      return None

    print ""
    # read category
    category = read_str( 'Category: ' )
    if not category:
      return None
    x.category = category if category != '' else x.category # check empty input
    # read category
    manufacturer = read_str( 'Manufacturer: ' )
    if not manufacturer:
      return None
    x.manufacturer = manufacturer if manufacturer != '' else x.manufacturer # check empty input
    # read category
    model = read_str( 'Model: ' )
    if not model:
      return None
    x.model = model if model != '' else x.model # check empty input
    # set the fields
    return x

  def editItem( self, x ):
    """
    method to edit the item and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # edit the item
    print ""
    print "============"
    print "Item Edit"
    print "============"
    chk = self.editItemMenu(x)
    # check for ctrl+c
    if chk:
      item = chk
    else:
      return
    # request the delegate to save the edit
    if self.delegate.itemMenuWantsEdit(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to save, try again later..."

  def confirmDelete(self):
    """
    prompts a confirm delete message
    """
    print ""
    return read_bool('Are you sure you want to delete this item (y/n)? ')

  def removeItem( self, x ):
    """
    method to edit the item and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # confirm the delete
    if self.confirmDelete() == False:
      return False
    
    # request the delegate to delete the item
    if self.delegate.itemMenuWantsDelete(x) == 0:
      print "Successfully removed!"
      return True
    else:
      print "Failed to remove, try again later..."
      return False
  
  def viewMenu( self ):
    """
    gets an item
    displays that item's information
    asks if the user wants to do anything more
    """
    item = self.getItem()
    if item == None:
      return
    self.itemViewMenu(item)
 
  def editMenu( self ):
    """
    gets an item
    displays that item's information
    prompts the edits that are to be made
    """
    item = self.getItem()
    if item == None:
      return
    self.displayItemInfo(item)
    self.editItem(item)

  def addMenu( self ):
    """
    creates an empty item
    edits that item 
    tries to save that item
    """
    item = Item()
    print ""
    print "============"
    print "Add Item"
    print "============"
    # call edit menu
    chk = self.editItemMenu(item)
    # cancel if ctrl+c
    if chk:
      item = chk
    else:
      return
    # ask delegate to add item
    if self.delegate.itemMenuWantsAdd(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to add, try again later..."

  def removeMenu( self ):
    """
    gets an item
    displays that item's information
    removes that item
    """
    item = self.getItem()
    if item == None:
      return
    self.displayItemInfo(item)
    self.removeItem(item)

if __name__=="__main__":
  ItemMenu().start()
