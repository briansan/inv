"""
  @file   MainController.py
  @author Brian Kim
  @brief  controller for handling the login/registering of users
"""

from inv.view.cli.MainMenu import MainMenu
from inv.model.Person import Person
import sqlite3 
from os.path import expanduser

class MainController( MainMenu.Delegate ):
  def init( self ):
    home = expanduser('~')
    db_path = home + '/.inv.db'
    self.db = sqlite3.connect(db_path)

  def __init__( self ):
    self.interface = MainMenu()

  def start( self ):
    self.interface.main()

if __name__ == "__main__":
  MainController().start()
