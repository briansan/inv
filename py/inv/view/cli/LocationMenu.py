"""
  @file   LocationMenu.py
  @author Brian Kim
  @brief  defines the command-line interface for the location menu
:a

"""

from inv.model.Permissions import Permissions
from inv.model.Location import Location
from common import *

class LocationMenu():
  class Delegate():
    """
    a set of methods that should be defined by the using
    class in order to respond to interface events
    """
    def locationMenuCheckUserPermission( self, action ):
      """
      determine whether a user has permission
      to perform a certain action
      """
      return True

    #
    # view methods
    #
    def locationMenuListAll( self):
      """
      return: all items in the db
      """
      return []

    #
    # edit methods
    #
    def locationMenuWantsEdit( self, item ):
      """
      receives the location that has been modified
      return: 0 for success, negative num for error
      """
      return -1

    #
    # add/remove methods
    # 
    def locationMenuWantsAdd( self, item ):
      """
      receives the location that wants to be created (no id)
      """
      return -1

    def locationMenuWantsDelete( self, item ):
      """
      receives the location that has wants to be deleted 
      return: 0 for success, negative num for error
      """
      return -1

    #
    # view methods
    #
    def locationMenuLookupByBuilding( self, building ):
      """
      looking up locations by building
      return: a list of matching locations
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
    prints out the location main menu 
    """
    # set default option
    opt = 0
    # display the menu repeatedly until back is selected
    while opt != 5:
      print ""
      print "============"
      print "Location Menu"
      print "============"
      print "1. View"
      print "2. Edit"
      print "3. Add"
      print "4. Remove"
      print "5. Back"
      print ""
      opt = read_int('Select an option: ')

      # go through all the option values and check permissions
      if opt == 1 and self.delegate.locationMenuCheckUserPermission(Permissions.LocationRead):
        self.viewMenu()
      elif opt == 2 and self.delegate.locationMenuCheckUserPermission(Permissions.LocationUpdate):
        self.editMenu()
      elif opt == 3 and self.delegate.locationMenuCheckUserPermission(Permissions.LocationCreate):
        self.addMenu()
      elif opt == 4 and self.delegate.locationMenuCheckUserPermission(Permissions.LocationDelete):
        self.removeMenu()
      elif opt != 5:
        print "Invalid option (maybe insufficient permissions?), try again..."
        
  def listLocationMenu( self ):
    """
    displays a menu of possible ways to search through locations
    and then returns a list of those locations
    """
    print ""
    print "=============="
    print "List Locations "
    print "=============="
    print "0. List all"
    print "1. Lookup by Building"
    print ""
    opt = read_int('Select an option: ')
    if not opt:
      return []

    # go through the options...
    if opt == 1: # list all locations
      y = self.delegate.locationMenuListAll()
    elif opt == 1: # lookup by category
      print ""
      x = read_str("Building: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.locationMenuLookupByBuilding(x)
    else: # any other option will repeat this menu
      y = self.listLocationMenu()
    return y

  def displayLocationInfo( self, x=None ):
    """
    displays the contents of a location
    """
    # check for null obj
    if x == None: 
      return

    # display the location info until back
    print ""
    print "===================="
    print "Location Information"
    print "===================="
    print "Building: " + x.building
    print "Room: " + x.room
      
  def getLocation( self ):
    """
    convenience method to retrieve a location from a list search
    """
    loclist = self.listLocationMenu()
    if loclist == None:
      return None
    loc = select_obj_from_list(loclist)
    return loc
    
  def locationViewMenu( self, x ):
    """
    method to display a menu after viewing a location
    """
    # display the information
    self.displayLocationInfo(x)

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
        self.editLocation(x)
      elif opt == 2: # remove
        if self.removeLocation(x):
          return
      elif opt != 3: # other (not back)
        print ""
        print "invalid option, try again..."
        self.locationViewMenu(x) # try again

  def editLocationMenu( self, x ):
    """
    method to prompt the editing of the location fields
    """
    if x == None:
      return None

    print ""
    # read building
    building = read_str( 'Building: ' )
    if not building:
      return None
    x.building = building if building != '' else x.building # check empty input
    # read room
    room = read_str( 'Room: ' )
    if not room:
      return None
    x.room = room if room != '' else x.room # check empty input
    # set the fields
    return x

  def editLocation( self, x ):
    """
    method to edit the location and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # edit the location
    print ""
    print "============="
    print "Location Edit"
    print "============="
    chk = self.editLocationMenu(x)
    # check for ctrl+c
    if chk:
      loc = chk
    else:
      return
    # request the delegate to save the edit
    if self.delegate.locationMenuWantsEdit(loc) == 0:
      print "Successfully saved!"
    else:
      print "Failed to save, try again later..."

  def confirmDelete(self):
    """
    prompts a confirm delete message
    """
    print ""
    return read_bool('Are you sure you want to delete this item (y/n)? ')

  def removeLocation( self, x ):
    """
    method to edit the item and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # confirm the delete
    if self.confirmDelete() == False:
      return False
    
    # request the delegate to delete the item
    if self.delegate.locationMenuWantsDelete(x) == 0:
      print "Successfully removed!"
      return True
    else:
      print "Failed to remove, try again later..."
      return False
  
  def viewMenu( self ):
    """
    gets a location
    displays that location's information
    asks if the user wants to do anything more
    """
    item = self.getLocation()
    if item == None:
      return
    self.locationViewMenu(item)
 
  def editMenu( self ):
    """
    gets an location
    displays that location's information
    prompts the edits that are to be made
    """
    item = self.getLocation()
    if item == None:
      return
    self.displayLocationInfo(item)
    self.editLocation(item)

  def addMenu( self ):
    """
    creates an empty location
    edits that location 
    tries to save that location
    """
    item = Location()
    print ""
    print "============"
    print "Add Location"
    print "============"
    # call edit menu
    chk = self.editLocationMenu(item)
    # cancel if ctrl+c
    if chk:
      item = chk
    else:
      return
    # ask delegate to add item
    if self.delegate.locationMenuWantsAdd(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to add, try again later..."

  def removeMenu( self ):
    """
    gets an item
    displays that item's information
    removes that item
    """
    item = self.getLocation()
    if item == None:
      return
    self.displayLocationInfo(item)
    self.removeLocation(item)

if __name__=="__main__":
  LocationMenu().start()
