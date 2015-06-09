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

  def main( self ):
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
    print "1. Lookup by Category"
    print "2. Lookup by Manufacturer"
    print "3. List all"
    print ""
    opt = read_int('Select an option: ')

    # go through the options...
    if opt == 1: # lookup by category
      print ""
      x = read_str("Category: ")
      y = self.delegate.itemMenuLookupByCategory(x)
    elif opt == 2: # lookup by manufacturer
      print ""
      x = read_str("Manufacturer: ")
      y = self.delegate.itemMenuLookupByManufacturer(x)
    elif opt == 3: # list all items
      y = self.delegate.itemMenuListAll()
    else: # any other option will repeat this menu
      y = self.listItemMenu()
    return y

  def selectItemMenu( self, x=[] ):
    """
    displays a list of items 'x' and then asks the user to select
    an item, returning that item
    """
    # check list length
    n = len(x)
    # check for empty list
    if n == 0:
      print ""
      print "No Results Found..."
      return None
    # print out the list
    print ""
    print str(x) + "Results:"
    for i in len(x): 
      item = x[i]
      print str(i+1)+". "+str(item)
    # get index
    opt = -1                 # to make sure we get a valid index...
    while opt != -1:         # until opt is NOT equal to -1
      print ""
      opt = read_int("Select an item: ") 
      if opt < 1 or opt > n: # if opt falls outside the proper range, 
        opt = -1             # set it back to -1
      
    # get that item
    y = x[opt-1] 
    return y

  def displayItemInfo( self, x=None ):
    """
    displays the contents of an item
    """
    # check for null obj
    if x == None: 
      return

    # repeatedly display the item info until back
      print ""
      print "==================="
      print "Item Information"
      print "==================="
      print "Category: " + x.category
      print "Manufacturer: " + x.manufacturer
      print "Model: " + x.model
      print ""
      
  def getItem( self ):
    """
    convenience method to retrieve an item from a list search
    """
    itemlist = self.listItemMenu()
    item = self.selectItemMenu(itemlist)
    return item
    
  def itemViewMenu( self, x ):
    """
    method to display a menu after viewing an item
    """
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
    x.category = category if category != '' else x.category # check empty input
    # read category
    manufacturer = read_str( 'Manufacturer: ' )
    x.manufacturer = manufacturer if manufacturer != '' else x.manufacturer # check empty input
    # read category
    model = read_str( 'Model: ' )
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
    item = self.editItemMenu(x)
    # request the delegate to save the edit
    if self.delegate.itemMenuWantsEdit(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to save, try again later..."

  def confirmDelete():
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
      return
    
    # request the delegate to delete the item
    if self.delegate.itemMenuWantsDelete(item) == 0:
      print "Successfully removed!"
    else:
      print "Failed to remove, try again later..."
  
  def viewMenu( self ):
    """
    gets an item
    displays that item's information
    asks if the user wants to do anything more
    """
    item = self.getItem()
    if item == None:
      return
    self.displayItemInfo(item)
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
    item = self.editItemMenu(item)
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
