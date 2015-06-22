"""
  @file   LoanMenu.py
  @author Brian Kim
  @brief  defines the command-line interface for the loan menu
"""

from inv.model.Permissions import Permissions
from inv.model.Loan import Loan
from common import *

class LoanMenu():
  class Delegate():
    """
    a set of methods that should be defined by the using
    class in order to respond to interface events
    """
    def loanMenuCheckUserPermission( self, action ):
      """
      determine whether a user has permission
      to perform a certain action
      """
      return True

    #
    # view methods
    #
    def loanMenuListAll( self):
      """
      return: all loan in the db
      """
      return []

    #
    # edit methods
    #
    def loanMenuSetApproved( self, item ):
      """
      receives the loan that has been modified
      return: 0 for success, negative num for error
      """
      return -1

    def loanMenuSetLoaned( self, item ):
      """
      receives the loan that has been modified
      return: 0 for success, negative num for error
      """
     return -1

    def loanMenuSetReturned( self, item ):
      """
      receives the loan that has been modified
      return: 0 for success, negative num for error
      """
     return -1

    #
    # add/remove methods
    # 
    def loanMenuWantsAdd( self, item ):
      """
      receives the loan that wants to be created (no id)
      """
      return -1

    def loanMenuWantsDelete( self, item ):
      """
      receives the loan that has wants to be deleted 
      return: 0 for success, negative num for error
      """
      return -1
    
    #
    # other model fetching methods
    #
    def loanMenuWantsAsset( self ):
      """
      delegate calls the proper interface method to 
      retrieve an item
      return: an Item or None
      """
      return None

    def loanMenuWantsPerson( self ):
      """
      delegate calls the proper interface method to 
      retrieve a person
      return: a Person or None
      """
      return None

    #
    # fetch methods
    #
    def loanMenuLookupByRequester( self, who ):
      """
      looking up a loan by the person
      who requested it
      """
      return []

    def loanMenuLookupByStatus( self, ecetag ):
      """
      looking up loan by its status
      return: a list of matching items
      """
      return []

    def loanMenuLookupByCreateDate( self, date ):
      """
      looking up loan by creation date
      return: a list of matching items
      """
      return []

    def loanMenuLookupByStartDate( self, date ):
      """
      looking up loan by start date
      return: a list of matching items
      """
      return []

    def loanMenuLookupByDueDate( self, date ):
      """
      looking up loan by due date
      return: a list of matching items
      """
      return []

    def loanMenuLookupByReturnDate( self, date ):
      """
      looking up loan by return date
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
    prints out the loan main menu 
    """
    # set default option
    opt = 0
    # display the menu repeatedly until back is selected
    while opt != 5:
      print ""
      print "============"
      print "Loan Menu"
      print "============"
      print "1. View"
      print "2. Edit"
      print "3. Add"
      print "4. Remove"
      print "5. Back"
      print ""
      opt = read_int('Select an option: ')

      # go through all the option values and check permissions
      if opt == 1 and self.delegate.loanMenuCheckUserPermission(Permissions.LoanRead):
        self.viewMenu()
      elif opt == 2 and self.delegate.loanMenuCheckUserPermission(Permissions.LoanUpdate):
        self.editMenu()
      elif opt == 3 and self.delegate.loanMenuCheckUserPermission(Permissions.LoanCreate):
        self.addMenu()
      elif opt == 4 and self.delegate.loanMenuCheckUserPermission(Permissions.LoanDelete):
        self.removeMenu()
      elif opt != 5:
        print "Invalid option (maybe insufficient permissions?), try again..."
        
  def listLoanMenu( self ):
    """
    displays a menu of possible ways to search through items
    and then returns a list of those items
    """
    print ""
    print "============"
    print "List Loans "
    print "============" 
    print "0. List all"
    print "1. Lookup by ECE Tag"
    print "2. Lookup by VU Tag"
    print "3. Lookup by Service Tag"
    print "4. Lookup by Item"
    print "5. Lookup by Status"
    print "6. Lookup by Owner"
    print "7. Lookup by Loaner"
    print "8. Lookup by Home Location"
    print "9. Lookup by Destination"
    print ""
    opt = read_int('Select an option: ')
    if not opt:
      return []

    # go through the options...
    if opt == 0: # list all items
      y = self.delegate.loanMenuListAll()
    elif opt == 1: # lookup by ece tag
      print ""
      x = read_str("ECE Tag: ") # get the value
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByECETag(x)
    elif opt == 2: # lookup by vu tag
      print ""
      x = read_str("VU Tag: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByVUTag(x)
    elif opt == 3: # lookup by svc tag
      print ""
      x = read_str("Service Tag: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByServiceTag(x)
    elif opt == 4: # lookup by item
      print ""
      x = read_str("Item: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByItem(x)
    elif opt == 5: # lookup by status
      print ""
      x = read_str("Status: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByStatus(x)
    elif opt == 6: # lookup by owner
      print ""
      x = read_str("Owner: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByOwner(x)
    elif opt == 7: # lookup by loaner
      print ""
      x = read_str("Loaner: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByHolder(x)
    elif opt == 8: # lookup by loaner
      print ""
      x = read_str("Home: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByHome(x)
    elif opt == 7: # lookup by loaner
      print ""
      x = read_str("Destination: ")
      if not x: # cancel if ctrl+c
        return None
      y = self.delegate.loanMenuLookupByDest(x)
    else: # any other option will repeat this menu
      y = self.listLoanMenu()
    return y

  def displayLoanInfo( self, x=None ):
    """
    displays the contents of an loan
    """
    # check for null obj
    if x == None: 
      return

    # display the item info until back
    print ""
    print "==================="
    print "Loan Information"
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
      
  def getLoan( self ):
    """
    convenience method to retrieve an item from a list search
    """
    loanlist = self.listLoanMenu()
    if loanlist == None:
      return None
    loan = select_obj_from_list(loanlist)
    return loan
    
  def loanViewMenu( self, x ):
    """
    method to display a menu after viewing an loan
    """
    # display the information
    self.displayLoanInfo(x)

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
        self.editLoan(x)
      elif opt == 2: # remove
        if self.removeLoan(x):
          return
      elif opt != 3: # other (not back)
        print ""
        print "invalid option, try again..."
        self.loanViewMenu(x) # try again

  def editLoanMenu( self, x ):
    """
    method to prompt the editing of the loan fields
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
    item = self.delegate.loanMenuWantsItem()
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
    home = self.delegate.loanMenuWantsLocation()
    x.home = home if home != None else x.home # check empty input
    # read dest
    print ''
    print 'Destination: ' 
    dest = self.delegate.loanMenuWantsLocation()
    x.dest = dest if dest != None else x.dest # check empty input
    # read loan
    loanable = read_bool( 'Loanable? (y/n): ' )
    x.loanable = loanable if loanable != None else x.loanable 
    # read owner
    print ''
    print 'Owner: ' 
    owner = self.delegate.loanMenuWantsPerson()
    x.owner = owner if owner !=  None else x.owner
    # read holder
    print ''
    print 'Current Holder: ' 
    holder = self.delegate.loanMenuWantsPerson()
    x.holder = holder if holder != None else x.holder
    # set the fields
    return x

  def editLoan( self, x ):
    """
    method to edit the loan and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # edit the item
    print ""
    print "============"
    print "Loan Edit"
    print "============"
    chk = self.editLoanMenu(x)
    # check for ctrl+c
    if chk:
      item = chk
    else:
      return
    # request the delegate to save the edit
    if self.delegate.loanMenuWantsEdit(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to save, try again later..."

  def confirmDelete(self):
    """
    prompts a confirm delete message
    """
    print ""
    return read_bool('Are you sure you want to delete this loan (y/n)? ')

  def removeLoan( self, x ):
    """
    method to edit the item and then save the changes
    also checks for successful save and displays the proper error msg
    """
    # confirm the delete
    if self.confirmDelete() == False:
      return False
    
    # request the delegate to delete the item
    if self.delegate.loanMenuWantsDelete(x) == 0:
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
    item = self.getLoan()
    if item == None:
      return
    self.loanViewMenu(item)
 
  def editMenu( self ):
    """
    gets an item
    displays that item's information
    prompts the edits that are to be made
    """
    item = self.getLoan()
    if item == None:
      return
    self.displayLoanInfo(item)
    self.editLoan(item)

  def addMenu( self ):
    """
    creates an empty item
    edits that item 
    tries to save that item
    """
    item = Loan()
    print ""
    print "============"
    print "Add Loan"
    print "============"
    # call edit menu
    chk = self.editLoanMenu(item)
    # cancel if ctrl+c
    if chk:
      item = chk
    else:
      return
    # ask delegate to add item
    if self.delegate.loanMenuWantsAdd(item) == 0:
      print "Successfully saved!"
    else:
      print "Failed to add, try again later..."

  def removeMenu( self ):
    """
    gets an item
    displays that item's information
    removes that item
    """
    item = self.getLoan()
    if item == None:
      return
    self.displayLoanInfo(item)
    self.removeLoan(item)

if __name__=="__main__":
  LoanMenu().start()
