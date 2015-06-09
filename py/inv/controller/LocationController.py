"""
  @file   LocationController.py
  @author BrianKim
  @brief  the controller that manages the location interface with the model
"""

from inv.view.cli.LocationMenu import LocationMenu
from inv.model.Location import Location
from inv.model.Person import Person

class LocationController( LocationMenu.Delegate ):
  #
  # ItemMenu delegate methods
  # 
  def locationMenuCheckUserPermission( self, action ):
    return self.user.permissions.check( action )

  def locationMenuListAll( self ):
    return Location.DBHelper.get_all( self.db )

  def locationMenuWantsEdit( self, item ):
    if Location.DBHelper.set( self.db, item ) == 1:
      return 0
    else:
      return -1

  def locationMenuWantsAdd( self, item ):
    if Location.DBHelper.add( self.db, item ) > 0:
      return 0
    else:
      return -1

  def locationMenuWantsDelete( self, item ):
    Location.DBHelper.delete( self.db, item )
    return 0

  def locationMenuLookupByBuilding( self, mfc ):
    return Location.DBHelper.get_by_building( self.db, mfc )

  #
  # lifecycle methods
  #
  def __init__( self, db, user ):
    self.db = db
    self.user = user
    self.interface = LocationMenu( self )

  def start( self ):
    self.interface.start()
    
