"""
  @file   PersonMenu.py
  @author Brian Kim
  @brief  defines the command-line interface for the person menu

"""

from inv.model.Permissions import Permissions
from inv.model.Person import Person
from inv.model.PersonGroup import PersonGroup
from common import *
from getpass import getpass

class PersonMenu():
  class Delegate():
    """
    a set of methods that should be defined by the using
    class in order to respond to interface events
    """

    def currentUser(self):
      y = Person('123456790')
      y.fname = 'John'
      y.lname = 'Smith'
      return y

    def personMenuCheckUserPermission( self, action ):
      """
      determine whether a user has permission
      to perform a certain action
      """
      return True

    #
    # edit methods
    #
    def personMenuWantsEdit( self, item ):
      """
      receives the person that has been modified
      return: 0 for success, negative num for error
      """
      return -1
   
    def personMenuWantsPasswordChange( self, user, old, new ):
      """
      receives the old and new requested pw, 
      return 0 for success, -1 for wrong old
      """
      return -1

    def personMenuWantsPermissionChange( self, user, perm ):
      """
      receives the user to change permissions to
      returns 0 for success, -1 for error
      """
      return -1

    #
    # add/remove methods
    # 
    def personMenuWantsAdd( self, item ):
      """
      receives the person that wants to be created (no id)
      """
      return -1

    def personMenuWantsDelete( self, item ):
      """
      receives the person that has wants to be deleted 
      return: 0 for success, negative num for error
      """
      return -1

    #
    # view methods
    #
    def personMenuListAll( self):
      """
      return: all items in the db
      """
      return []

    def personMenuLookupByUsername( self, uname ):
      """
      looking up people by username
      return: a list of matching people
      """
      return []

    def personMenuLookupByFirstName( self, fname ):
      """
      looking up people by first name
      return: a list of matching people
      """
      return []
 
    def personMenuLookupByLastName( self, lname ):
      """
      looking up people by last name
      return: a list of matching people
      """
      return []

    def personMenuLookupByPhone( self, phone ):
      """
      looking up people by phone number
      return: a list of matching people
      """
      return []

    def personMenuLookupByEmail( self, email ):
      """
      looking up people by email
      return: a list of matching people
      """
      return []

    def personMenuLookupByGroup( self, group ):
      """
      looking up people by group 
      return: a list of matching people
      """
      return []

    def personMenuLookupByYear( self, year ):
      """
      looking up people by year
      return: a list of matching people
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
    while opt != 3:
      print ""
      print "============"
      print "Person Menu"
      print "============"
      print "1. My Profile"
      print "2. Directory"
      print "3. Back"
      print ""
      opt = read_int('Select an option: ')

      # go through all the option values and check permissions
      if opt == 1:
        self.viewProfile()
      elif opt == 2 and self.delegate.personMenuCheckUserPermission(Permissions.PersonRead):
        self.directoryMenu()
      elif opt != 3:
        print "Invalid option (maybe insufficient permissions?), try again..."
        
  def directoryMenu( self ):
    x = self.getPerson()
    self.personViewMenu(x)

  def listPersonMenu( self ):
    """
    displays a menu of possible ways to search through the people directory
    and then returns a list of those people
    """
    print ""
    print "================"
    print "People Directory "
    print "================"
    print "1. Lookup by Username"
    print "2. Lookup by First Name"
    print "3. Lookup by Last Name"
    print "4. Lookup by Phone"
    print "5. Lookup by Email"
    print "6. Lookup by Group"
    print "7. Lookup by Year"
    print "8. List all"
    print ""
    opt = read_int('Select an option: ')
    if not opt:
      return []

    # go through the options...
    if opt == 1: # lookup by username
      print ""
      x = read_str("Username: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByUsername(x)

    elif opt == 2: # lookup by first name
      print ""
      x = read_str("First Name: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByFirstName(x)

    elif opt == 3: # lookup by last name
      print ""
      x = read_str("Last Name: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByLastName(x)

    elif opt == 4: # lookup by phone
      print ""
      x = read_str("Phone Number: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByPhone(x)

    elif opt == 5: # lookup by email
      print ""
      x = read_str("Email: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByEmail(x)

    elif opt == 6: # lookup by group
      return None
      print ""
      x = read_str("Group: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByGroup(x)

    elif opt == 7: # lookup by year
      print ""
      x = read_int("Year: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.personMenuLookupByYear(x)

    elif opt == 8: # lookup all
      y = self.delegate.personMenuListAll()

    else: # any other option will repeat this menu
      y = self.listPersonMenu()
    return y

  def viewProfile( self ):
    self.personViewMenu( self.delegate.currentUser() )

  def displayPersonInfo( self, x=None ):
    """
    displays the contents of a person
    """
    # check for null obj
    if x == None: 
      return

    # display the location info until back
    print ""
    print "===================="
    print "Person Information"
    print "===================="
    print "Username: " + x.uname
    print "First Name: " + x.fname
    print "Last Name: " + x.lname
    print "Phone Number: " + x.phone
    print "Email Address: " + x.email
    print "Group: " + PersonGroup.info[x.ptype]
    if self.delegate.currentUser().permissions.check(Permissions.PersonUpdateWorld):
      print x.permissions
    print "Year: " + str(x.year)
      
  def getPerson( self ):
    """
    convenience method to retrieve a location from a list search
    """
    personlist = self.listPersonMenu()
    if personlist == None:
      return None
    person = select_obj_from_list(personlist)
    return person
    
  def personViewMenu( self, x ):
    """
    method to display a menu after viewing a person
    """
    # display the information
    self.displayPersonInfo(x)

    # actions are only available for self or for admins
    isSelf = x==self.delegate.currentUser()
    isAdmin = self.delegate.personMenuCheckUserPermission(Permissions.PersonUpdateWorld)

    if isSelf or isAdmin:
      # request action
      opt = 0
      while opt != 3:
        print ""
        print "What would you like to do?"
        print "1. edit"
        print "2. change password"
        print "3. back"
        if isAdmin:
          print "4. change permissions"
        print ""
        opt = read_int('Select an option: ')
        
        if opt == 1: # edit
          self.editPerson(x)
        elif opt == 2: # back
          self.changePassword(x)
        elif opt == 4 and isAdmin:
          self.changePermissions(x)
        elif opt != 3:
          print ""
          print "invalid option, try again..."

  def editPersonMenu( self, x ):
    """
    method to prompt the editing of the person fields
    """
    if x == None:
      return None

    # read first name
    fname = read_str( 'First Name: ' )
    if fname == None:
      return None
    x.fname = fname if fname != '' else x.fname # check empty input
    # read last name
    lname = read_str( 'Last Name: ' )
    if lname == None:
      return None
    x.lname = lname if lname != '' else x.lname # check empty input
    # read phone number
    phone = read_str( 'Phone Number: ' )
    if phone == None:
      return None
    x.phone = phone if phone != '' else x.phone # check empty input
    # read email
    email = read_str( 'Email: ' )
    if email == None:
      return None
    x.email = email if email != '' else x.email # check empty input
    # read grad year
    year = read_str( 'Graduation Year: ' )
    if year == None:
      return None
    x.year = year if year != '' else x.year # check empty input
    # set the fields
    return x

  def changePassword( self, x ):
    """
    changes the password of the select user (only admin should
    be able to change world passwords
    """
    print ""
    print "===================="
    print "change password"
    print "===================="
    # confirm old password
    oldpw = getpass('Old Password: ')
    newpw = getpass('New Password: ')
    newpw_chk = getpass('Confirm New Password: ')
    print ""
    
    if newpw != newpw_chk:
      print "Passwords don't match!"
      return
   
    if self.delegate.personMenuWantsPasswordChange( x, oldpw, newpw ) == 0:
      print "Success!"
    else:
      print "Incorret password..."
    
  def changePermissions( self, user ):
    
    # header
    print "=========================="
    print "Modify Permissions"
    print "  enter a number to toggle"
    print "  0 to save changes"
    print "  ctrl+c to cancel"
    print "=========================="

    # edit loop
    i = -1
    while i != 0:
      # print out perms
      print repr(user.permissions)
      # input perm to toggle
      i = read_int('Select a permission: ')
   
      # 0 = save&quit, ctrl+c = cancel&quit
      if i == 0:
        self.delegate.personMenuWantsEdit(user)
        return
      elif i == None:
        return

      # toggle perm
      perm = 2**(i-1)
      exists = user.permissions.check(perm)
      user.permissions.value = user.permissions.value ^ perm

  def editPerson( self, x ):
    """
    method to edit the person and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # edit the person
    print ""
    print "======================="
    print "Person edit"
    print "enter fields to modify"
    print "(blank entry skips)"
    print "======================="
    chk = self.editPersonMenu(x)
    # check for ctrl+c
    if chk:
      loc = chk
    else:
      return
    # request the delegate to save the edit
    if self.delegate.personMenuWantsEdit(loc) == 0:
      print "Successfully saved!"
    else:
      print "Failed to save, try again later..."

  def confirmDelete(self):
    """
    prompts a confirm delete message
    """
    print ""
    return read_bool('Are you sure you want to delete this item (y/n)? ')

  def removePerson( self, x ):
    """
    method to edit the item and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # confirm the delete
    if self.confirmDelete() == False:
      return False
    
    # request the delegate to delete the item
    if self.delegate.personMenuWantsDelete(x) == 0:
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
    item = self.getPerson()
    if item == None:
      return
    self.displayPersonInfo(item)
    self.personViewMenu(item)
 
  def editMenu( self ):
    """
    gets an location
    displays that location's information
    prompts the edits that are to be made
    """
    item = self.getPerson()
    if item == None:
      return
    self.displayPersonInfo(item)
    self.editPerson(item)

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
    item = self.getPerson()
    if item == None:
      return
    self.displayPersonInfo(item)
    self.removePerson(item)

if __name__=="__main__":
  PersonMenu().start()
