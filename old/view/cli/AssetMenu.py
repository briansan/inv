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

    def assetMenuLookupByHolder( self, loaner ):
      """
      looking up asset by holder
      return: a list of matching items
      """
      return []

    def assetMenuLookupByHome( self, home ):
      """
      looking up asset by home
      return: a list of matching items
      """
      return []

    def assetMenuLookupByDest( self, dest ):
      """
      looking up asset by dest
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
    print "List Assets "
    print "============" 
    print "1. List all"
    print "2. Lookup by ECE Tag"
    print "3. Lookup by VU Tag"
    print "4. Lookup by Service Tag"
    print "5. Lookup by Item"
    print "6. Lookup by Status"
    print "7. Lookup by Owner"
    print "8. Lookup by Loaner"
    print "9. Lookup by Home Location"
    print "10. Lookup by Destination"
    print ""
    opt = read_int('Select an option: ')
    if not opt:
      return []

    # go through the options...
    if opt == 1: # list all items
      y = self.delegate.assetMenuListAll()
    elif opt == 2: # lookup by ece tag
      print ""
      x = read_str("ECE Tag: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByECETag(x)
    elif opt == 3: # lookup by vu tag
      print ""
      x = read_str("VU Tag: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByVUTag(x)
    elif opt == 4: # lookup by svc tag
      print ""
      x = read_str("Service Tag: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByServiceTag(x)
    elif opt == 5: # lookup by item
      print ""
      x = read_str("Item: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByItem(x)
    elif opt == 6: # lookup by status
      print ""
      x = read_str("Status: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByStatus(x)
    elif opt == 7: # lookup by owner
      print ""
      x = read_str("Owner: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByOwner(x)
    elif opt == 8: # lookup by loaner
      print ""
      x = read_str("Loaner: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByHolder(x)
    elif opt == 9: # lookup by loaner
      print ""
      x = read_str("Home: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByHome(x)
    elif opt == 10: # lookup by loaner
      print ""
      x = read_str("Destination: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.assetMenuLookupByDest(x)
    else: # any other option will repeat this menu
      y = self.listAssetMenu()
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
    print "VU Tag: " + x.vu_tag
    print "Service Tag: " + x.service_tag
    print "Serial Number: " + x.serial_number
    print "Item: " + str(x.item)
    print "Value ($): " + str(x.price)
    print "Purchase Date: " + str(x.purchased.date())
    print "Deploy Date: " + str(x.deployed.date())
    print "Last Inventory: " + str(x.inventoried.date())
    print "Image Path: " + x.img
    print "Status: " + str(x.status)
    print "Disposal Date: " + str(x.disposed.date())
    print "Home: " + str(x.home)
    print "Destination: " + str(x.dest)
    print "Loanable: " + str(x.loanable)
    print "Owner: " + str(x.owner)
    print "Holder: " + str(x.holder)
      
  def getAsset( self ):
    """
    convenience method to retrieve an item from a list search
    """
    assetlist = self.listAssetMenu()
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
    if ece_tag==None:
      return None
    x.ece_tag = ece_tag if ece_tag != '' else x.ece_tag # check empty input
    # read vu_tag
    vu_tag = read_str( 'VU Tag: ' )
    if vu_tag==None:
      return None
    x.vu_tag = vu_tag if vu_tag != '' else x.vu_tag # check empty input
    # read service tag
    svc_tag = read_str( 'Service Tag: ' )
    if svc_tag==None:
      return None
    x.service_tag = svc_tag if svc_tag != '' else x.service_tag # check empty input
    # read serial_number
    serial_number = read_str( 'Serial Number: ' )
    if serial_number==None:
      return None
    x.serial_number = serial_number if serial_number != '' else x.serial_number # check empty input
    # read item
    print ''
    print 'Item: ' 
    item = self.delegate.assetMenuWantsItem()
    x.item = item if item != None else x.item # check empty input
    # read value
    price = read_float( 'Value ($): ' )
    if price==None:
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
    print ''
    print 'Home Location: ' 
    home = self.delegate.assetMenuWantsLocation()
    x.home = home if home != None else x.home # check empty input
    # read dest
    print ''
    print 'Destination: ' 
    dest = self.delegate.assetMenuWantsLocation()
    x.dest = dest if dest != None else x.dest # check empty input
    # read loan
    loanable = read_bool( 'Loanable? (y/n): ' )
    x.loanable = loanable if loanable != None else x.loanable 
    # read owner
    print ''
    print 'Owner: ' 
    owner = self.delegate.assetMenuWantsPerson()
    x.owner = owner if owner !=  None else x.owner
    # read holder
    print ''
    print 'Current Holder: ' 
    holder = self.delegate.assetMenuWantsPerson()
    x.holder = holder if holder != None else x.holder
    # set the fields
    return x

  def editAsset( self, x ):
    """
    method to edit the asset and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # edit the item
    print ""
    print "============"
    print "Asset Edit"
    print "============"
    chk = self.editAssetMenu(x)
    # check for ctrl+c
    if chk:
      item = chk
    else:
      return
    # request the delegate to save the edit
    if self.delegate.assetMenuWantsEdit(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to save, try again later..."

  def confirmDelete(self):
    """
    prompts a confirm delete message
    """
    print ""
    return read_bool('Are you sure you want to delete this asset (y/n)? ')

  def removeAsset( self, x ):
    """
    method to edit the item and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # confirm the delete
    if self.confirmDelete() == False:
      return False
    
    # request the delegate to delete the item
    if self.delegate.assetMenuWantsDelete(x) == 0:
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
    item = self.getAsset()
    if item == None:
      return
    self.assetViewMenu(item)
 
  def editMenu( self ):
    """
    gets an item
    displays that item's information
    prompts the edits that are to be made
    """
    item = self.getAsset()
    if item == None:
      return
    self.displayAssetInfo(item)
    self.editAsset(item)

  def addMenu( self ):
    """
    creates an empty item
    edits that item 
    tries to save that item
    """
    item = Asset()
    print ""
    print "============"
    print "Add Asset"
    print "============"
    # call edit menu
    chk = self.editAssetMenu(item)
    # cancel if ctrl+c
    if chk:
      item = chk
    else:
      return
    # ask delegate to add item
    if self.delegate.assetMenuWantsAdd(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to add, try again later..."

  def removeMenu( self ):
    """
    gets an item
    displays that item's information
    removes that item
    """
    item = self.getAsset()
    if item == None:
      return
    self.displayAssetInfo(item)
    self.removeAsset(item)

if __name__=="__main__":
  AssetMenu().start()
