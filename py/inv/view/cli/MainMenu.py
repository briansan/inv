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
      ItemMenu().main()
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

  def mainMenu(self):
    print ""
    print "Main Menu"
    print "1. Login"
    print "2. Register"
    print "3. Quit"
    print ""
    opt = read_int('Select your option: ')
    return opt

  def login(self):
    print ""
    print "Login"
  
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
    print "Registration"

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
      print "Main Menu:"
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
          self.delegate.mainMenuWantsPeopleMenu()

      elif opt == 6:
        print "Goodbye!"

  def main(self):
    self.displayHeader()
    print "\tinitializing..."
    self.delegate.init()
    opt = self.mainMenu()
    if opt == 1:   # login
      self.login()
    elif opt == 2: # register
      self.register()
    elif opt == 3: # quit
      print "Goodbye!"

