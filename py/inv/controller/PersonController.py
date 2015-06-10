"""
  @file   PersonController.py
  @author BrianKim
  @brief  the controller that manages the person interface with the model
"""

from inv.view.cli.PersonMenu import PersonMenu
from inv.model.Person import Person

class PersonController( PersonMenu.Delegate ):
  #
  # ItemMenu delegate methods
  # 
  def personMenuCheckUserPermission( self, action ):
    return self.user.permissions.check( action )

  def personMenuListAll( self ):
    return Person.DBHelper.get_all( self.db )

  def personMenuWantsEdit( self, item ):
    if Person.DBHelper.set( self.db, item ) == 1:
      return 0
    else:
      return -1

  def personMenuWantsAdd( self, item ):
    if Person.DBHelper.add( self.db, item ) > 0:
      return 0
    else:
      return -1

  def personMenuWantsDelete( self, item ):
    Person.DBHelper.delete( self.db, item )
    return 0

  def personMenuLookupByBuilding( self, mfc ):
    return Person.DBHelper.get_by_building( self.db, mfc )

  #
  # lifecycle methods
  #
  def __init__( self, db, user ):
    self.db = db
    self.user = user
    self.interface = PersonMenu( self )

  def start( self ):
    self.interface.start()
    
