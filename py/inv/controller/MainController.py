"""
  @file   MainController.py
  @author Brian Kim
  @brief  controller for handling the login/registering of users
"""

from inv.controller.ItemController import ItemController
from inv.controller.LocationController import LocationController
from inv.controller.PersonController import PersonController
from inv.controller.AssetController import AssetController

from inv.view.cli.MainMenu import MainMenu

from inv.model.Person import Person
from inv.model.Asset import Asset
from inv.model.Item import Item
from inv.model.Location import Location
from inv.model.PersonGroup import PersonGroup

import sqlite3 
from os.path import expanduser

class MainController( MainMenu.Delegate ):
  def init( self ):
    # init db
    print "\tinitializing database"
    home = expanduser('~')
    db_path = home + '/.inv.db'
    self.db = sqlite3.connect(db_path)

    # create tables
    print "\tcreating tables..."
    Person.DBHelper.create_table(self.db)
    Asset.DBHelper.create_table(self.db)
    Item.DBHelper.create_table(self.db)
    Location.DBHelper.create_table(self.db)

    # checking admin acct
    chk = Person.DBHelper.create_admin(self.db)
    if not chk:
      print "\tadmin account already exists..."
    else:
      print "\tadmin account successfully created!"

  def login( self, uname, pw ):
    userlist = Person.DBHelper.get_by_uname( self.db, uname )
    if len( userlist ) == 0:
      return -1 # user does not exist
    if Person.DBHelper.auth( self.db, userlist[0], pw ):
      self.user = userlist[0]
      return 0  # successful login
    else:
      return -2 # incorrect password

  def register( self, uname, pw, fname, lname, phone, email, group=PersonGroup.Guest, year=2015 ):
    # create a user object
    user = Person(uname,fname,lname,phone,email)
    # try to create user into db
    uid = Person.DBHelper.add(self.db,user,pw)
    # check for success
    if uid == -1:
      print "User with that name already exists! Try again"
      return None
    else:
      print "Thank you for registering with inv!"
      self.user = user
    return user

  def currentUser( self ):
    return self.user

  def mainMenuWantsAssetMenu( self ):
    AssetController(self.db,self.user).start() 
  def mainMenuWantsLoanMenu( self ):
    pass 
  def mainMenuWantsItemMenu( self ):
    ItemController(self.db,self.user).start() 
  def mainMenuWantsPersonMenu( self ):
    PersonController(self.db,self.user).start() 
  def mainMenuWantsLocationMenu( self ):
    LocationController(self.db,self.user).start() 

  def __init__( self ):
    self.interface = MainMenu(self)
    self.user = None

  def start( self ):
    self.interface.start()

if __name__ == "__main__":
  MainController().start()
