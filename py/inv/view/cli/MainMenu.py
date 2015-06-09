"""
  @file   MainMenu.py
  @author Brian Kim
  @brief  the command-line interface for the main menu of inv  
"""

from common import *
from getpass import getpass

from inv.model.Person import Person
from ItemMenu import ItemMenu

class MainMenu():
  class Delegate( ):
    def init( self ):
      print "initializing"
    def login( self, uname, pw ):
      return 0
    def register( self, uname,pw,fname,lname,phone,email ):
      return 0
    def currentUser( self ):
      p = Person('1234567890')
      p.fname = 'John'
      p.lname = 'Smith'
      return p
    def mainMenuWantsAssetMenu( self ):
      pass
    def mainMenuWantsLoanMenu( self ):
      pass
    def mainMenuWantsItemMenu( self ):
      ItemMenu().start()
    def mainMenuWantsPersonMenu( self ):
      pass
    def mainMenuWantsLoanMenu( self ):
      pass

  def __init__( self, delegate=Delegate() ):
    self.delegate = delegate

  def displayHeader(self):
    print ""
    print "************************************"
    print "              inv"
    print "             by: BK"
    print "************************************"

  def authMenu(self):
    print ""
    print "==================="
    print "Authentication Menu"
    print "==================="
    print "1. Login"
    print "2. Register"
    print "3. Quit"
    print ""
    opt = read_int('Select your option: ')
    return opt

  def login(self):
    print ""
    print "=================="
    print "Login"
    print "=================="
  
    # request credentials
    uname = read_str('username: ')
    pw = getpass('password: ')
  
    # check credentials
    if self.delegate.login(uname,pw) == 0:
      self.userMainMenu()
    else:
      print "Bad Credentials..."
      return

  def register(self):
    print ""
    print "=================="
    print "Registration"
    print "=================="

    # request information
    uname = read_str("Username: ")
    pw = getpass("Password: ")
    pw_chk = getpass("Re-type Password: ")
    fname = read_str("First Name: ")
    lname = read_str("Last Name: ")
    phone = read_str("Phone Number: ")
    email = read_str("Email: ")

    # check the password
    if pw != pw_chk:
      print "Passwords don't match!"
      return self.register()

    # ask delegate to register acct into db
    if self.delegate.register(uname,pw,fname,lname,phone,email) == 0:
      self.userMainMenu() # success
    else: # fail
      print "Failed to create user account, try again later"

  def userMainMenu(self):
    # ask the delegate for the user
    user = self.delegate.currentUser()
    print ""
    print "======================================"
    print "Welcome " + user.fname + " " + user.lname + "!"
    print "======================================"
  
    opt = 0
    while opt != 6:
      print ""
      print "================="
      print "Main Menu:"
      print "================="
      print "1. Assets"
      print "2. Loans"
      print "3. Items"
      print "4. Locations"
      print "5. People"
      print "6. Quit"
      print ""
      opt = input("Please select an option: ")
  
      # request delegate to go to the next menu
      if opt >= 1 and opt <= 5:
        if opt == 1:
          self.delegate.mainMenuWantsAssetMenu()
        elif opt == 2:
          self.delegate.mainMenuWantsLoanMenu()
        elif opt == 3:
          self.delegate.mainMenuWantsItemMenu()
        elif opt == 4:
          self.delegate.mainMenuWantsLocationMenu()
        elif opt == 5:
          self.delegate.mainMenuWantsPersonMenu()

      elif opt == 6:
        print "Goodbye!"

  def start(self):
    # display the header
    self.displayHeader()
    # let the delegate do its initialization
    print "\tinitializing..."
    self.delegate.init()
    # go to the authentication menu
    opt = self.authMenu()
    # login
    if opt == 1:   
      self.login()
    # register
    elif opt == 2: 
      self.register()
    # quit
    elif opt == 3: 
      print "Goodbye!"

if __name__=="__main__":
  MainMenu().start()
