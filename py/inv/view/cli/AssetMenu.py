"""
  @file   AssetMenu.py
  @author Brian Kim
  @brief  defines the command-line interface for the asset menu
"""

from inv.model.Permissions import Permissions
from inv.model.Asset import Asset
from common import *

class AssetMenu():
  class Delegate():
    """
    a set of methods that should be defined by the using
    class in order to respond to interface events
    """
    def assetMenuCheckUserPermission( self, action ):
      """
      determine whether a user has permission
      to perform a certain action
      """
      return True

    #
    # view methods
    #
    def assetMenuListAll( self):
      """
      return: all asset in the db
      """
      return []

    #
    # edit methods
    #
    def assetMenuWantsEdit( self, item ):
      """
      receives the asset that has been modified
      return: 0 for success, negative num for error
      """
      return -1

    #
    # add/remove methods
    # 
    def assetMenuWantsAdd( self, item ):
      """
      receives the asset that wants to be created (no id)
      """
      return -1

    def assetMenuWantsDelete( self, item ):
      """
      receives the asset that has wants to be deleted 
      return: 0 for success, negative num for error
      """
      return -1
    
    #
    # other model fetching methods
    #
    def assetMenuWantsItem( self ):
      """
      delegate calls the proper interface method to 
      retrieve an item
      return: an Item or None
      """
      return None

    def assetMenuWantsLocation( self ):
      """
      delegate calls the proper interface method to 
      retrieve a location
      return: a Location or None
      """
      return None

    def assetMenuWantsPerson( self ):
      """
      delegate calls the proper interface method to 
      retrieve a person
      return: a Person or None
      """
      return None

    #
    # fetch methods
    #
    def assetMenuLookupByECETag( self, ecetag ):
      """
      looking up asset by ece tag
      return: a list of matching items
      """
      return []

    def assetMenuLookupByVUTag( self, vutag ):
      """
      looking up asset by vutag
      return: a list of matching items
      """
      return []

    def assetMenuLookupByServiceTag( self, svctag ):
      """
      looking up asset by service tag
      return: a list of matching items
      """
      return []

    def assetMenuLookupByItem( self, item ):
      """
      looking up asset by item
      return: a list of matching items
      """
      return []

    def assetMenuLookupByStatus( self, status ):
      """
      looking up asset by status
      return: a list of matching items
      """
      return []

    def assetMenuLookupByOwner( self, owner ):
      """
      looking up asset by owner
      return: a list of matching items
      """
      return []

    def assetMenuLookupByLoaner( self, loaner ):
      """
      looking up asset by loaner
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
    prints out the asset main menu 
    """
    # set default option
    opt = 0
    # display the menu repeatedly until back is selected
    while opt != 5:
      print ""
      print "============"
      print "Asset Menu"
      print "============"
      print "1. View"
      print "2. Edit"
      print "3. Add"
      print "4. Remove"
      print "5. Back"
      print ""
      opt = read_int('Select an option: ')

      # go through all the option values and check permissions
      if opt == 1 and self.delegate.assetMenuCheckUserPermission(Permissions.AssetRead):
        self.viewMenu()
      elif opt == 2 and self.delegate.assetMenuCheckUserPermission(Permissions.AssetUpdate):
        self.editMenu()
      elif opt == 3 and self.delegate.assetMenuCheckUserPermission(Permissions.AssetCreate):
        self.addMenu()
      elif opt == 4 and self.delegate.assetMenuCheckUserPermission(Permissions.AssetDelete):
        self.removeMenu()
      elif opt != 5:
        print "Invalid option (maybe insufficient permissions?), try again..."
        
  def listAssetMenu( self ):
    """
    displays a menu of possible ways to search through items
    and then returns a list of those items
    """
    print ""
    print "============"
    print "List Items "
    print "============"
    print "1. Lookup by ECE Tag"
    print "2. Lookup by VU Tag"
    print "3. Lookup by Service Tag"
    print "4. Lookup by Item"
    print "5. Lookup by Status"
    print "6. Lookup by Owner"
    print "7. Lookup by Loaner"
    print "8. List all"
    print ""
    opt = read_int('Select an option: ')
    if not opt:
      return []

    # go through the options...
    if opt == 1: # lookup by ece tag
      print ""
      x = read_str("ECE Tag: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByECETag(x)
    elif opt == 2: # lookup by vu tag
      print ""
      x = read_str("VU Tag: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByVUTag(x)
    elif opt == 3: # lookup by svc tag
      print ""
      x = read_str("Service Tag: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByServiceTag(x)
    elif opt == 4: # lookup by item
      print ""
      x = read_str("Item: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByItem(x)
    elif opt == 5: # lookup by status
      print ""
      x = read_str("Status: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByStatus(x)
    elif opt == 6: # lookup by owner
      print ""
      x = read_str("Owner: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByOwner(x)
    elif opt == 7: # lookup by loaner
      print ""
      x = read_str("Loaner: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByLoaner(x)
    elif opt == 8: # list all items
      y = self.delegate.itemMenuListAll()
    else: # any other option will repeat this menu
      y = self.listItemMenu()
    return y

  def displayAssetInfo( self, x=None ):
    """
    displays the contents of an asset
    """
    # check for null obj
    if x == None: 
      return

    # display the item info until back
    print ""
    print "==================="
    print "Asset Information"
    print "==================="
    print "ECE Tag: " + x.ece_tag
    print " VU Tag: " + x.vu_tag
    print "  Service Tag: " + x.service_tag
    print "Serial Number: " + x.serial_number
    print "Item: " + x.item
    print "Value ($): " + x.price
    print "Purchase Date: " + x.purchased
    print "Deploy Date: " + x.deployed
    print "Last Inventory: " + x.inventoried
    print "Image Path: " + x.img
    print "Status: " + x.status
    print "Disposal Date: " + x.disposed
    print "Home: " + x.home
    print "Destination: " + x.dest
    print "Loanable: " + x.loanable
    print "Owner: " + x.owner
    print "Holder: " + x.holder
      
  def getAsset( self ):
    """
    convenience method to retrieve an item from a list search
    """
    assetlist = self.assetItemMenu()
    if assetlist == None:
      return None
    asset = select_obj_from_list(assetlist)
    return asset
    
  def assetViewMenu( self, x ):
    """
    method to display a menu after viewing an asset
    """
    # display the information
    self.displayAssetInfo(x)

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
        self.editAsset(x)
      elif opt == 2: # remove
        if self.removeAsset(x):
          return
      elif opt != 3: # other (not back)
        print ""
        print "invalid option, try again..."
        self.assetViewMenu(x) # try again

  def editAssetMenu( self, x ):
    """
    method to prompt the editing of the asset fields
    """
    if x == None:
      return None

    print ""
    # read ece tag
    ece_tag = read_str( 'ECE Tag: ' )
    if not ece_tag:
      return None
    x.ece_tag = ece_tag if ece_tag != '' else x.ece_tag # check empty input
    # read vu_tag
    vu_tag = read_str( 'VU Tag: ' )
    if not vu_tag:
      return None
    x.vu_tag = vu_tag if vu_tag != '' else x.vu_tag # check empty input
    # read service tag
    svc_tag = read_str( 'Service Tag: ' )
    if not svc_tag:
      return None
    x.service_tag = svc_tag if svc_tag != '' else x.service_tag # check empty input
    # read serial_number
    serial_number = read_str( 'Serial Number: ' )
    if not serial_number:
      return None
    x.serial_number = serial_number if serial_number != '' else x.serial_number # check empty input
    # read item
    item = self.delegate.assetMenuWantsItem()
    x.item = item if item != None else x.item # check empty input
    # read value
    price = read_float( 'Value ($): ' )
    if not price:
      return None
    x.price = price if price < 0 else x.price # check empty input
    # read purchased
    purchased = read_date( 'Purchase Date (MM/DD/YYYY): ' )
    x.purchased = purchased if purchased != None else x.purchased
    # read deploy
    deployed = read_date( 'Deploy Date (MM/DD/YYYY): ' )
    x.deployed = deployed if deployed != None else x.deployed
    # read last inventory
    inventoried = read_date( 'Last Inventory Date (MM/DD/YYYY): ' )
    x.inventoried = inventoried if inventoried != None else x.inventoried
    # read home
    home = self.delegate.assetMenuWantsLocation()
    x.home = home if home != None else x.home # check empty input
    # read dest
    dest = self.delegate.assetMenuWantsLocation()
    x.dest = dest if dest != None else x.dest # check empty input
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
