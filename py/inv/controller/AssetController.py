"""
  @file   AssetController.py
  @author BrianKim
  @brief  the controller that manages the asset interface with the model
"""

from PersonController import PersonController
from ItemController import ItemController
from LocationController import LocationController

from inv.view.cli.AssetMenu import AssetMenu
from inv.model.Asset import Asset
from inv.model.Person import Person

class AssetController( AssetMenu.Delegate ):
  #
  # AssetMenu delegate methods
  # 
  def assetMenuCheckUserPermission( self, action ):
    return self.user.permissions.check( action )

  def assetMenuListAll( self ):
    return Asset.DBHelper.get_all( self.db )

  def assetMenuWantsEdit( self, asset ):
    if Asset.DBHelper.set( self.db, asset ) == 1:
      return 0
    else:
      return -1

  def assetMenuWantsAdd( self, asset ):
    if Asset.DBHelper.add( self.db, asset ) > 0:
      return 0
    else:
      return -1

  def assetMenuWantsDelete( self, asset ):
    Asset.DBHelper.delete( self.db, asset )
    return 0

  #
  # other data types
  #
  def assetMenuWantsItem( self ):
    return self.item.interface.getItem()

  def assetMenuWantsPerson( self ):
    return self.person.interface.getPerson()

  def assetMenuWantsLocation( self ):
    return self.location.interface.getLocation()

  #
  # fetch
  #
  def assetMenuLookupByECETag( self, tag ):
    return Asset.DBHelper.get_by_tag( self.db, tag, 'ece' )

  def assetMenuLookupByVUTag( self, cat ):
    return Asset.DBHelper.get_by_tag( self.db, cat, 'vu' )

  def assetMenuLookupByServiceTag( self, cat ):
    return Asset.DBHelper.get_by_tag( self.db, cat, 'service' )

  def assetMenuLookupByItem( self, cat ):
    return Asset.DBHelper.get_by_item( self.db, cat )

  def assetMenuLookupByStatus( self, cat ):
    return Asset.DBHelper.get_by_status( self.db, cat )

  def assetMenuLookupByOwner( self, cat ):
    return Asset.DBHelper.get_by_owner( self.db, cat )

  def assetMenuLookupByHolder( self, cat ):
    return Asset.DBHelper.get_by_category( self.db, cat )

  def assetMenuLookupByHome( self, cat ):
    return Asset.DBHelper.get_by_home( self.db, cat )

  def assetMenuLookupByDest( self, cat ):
    return Asset.DBHelper.get_by_dest( self.db, cat )

  #
  # lifecycle methods
  #
  def __init__( self, db, user ):
    self.db = db
    self.user = user
    self.interface = AssetMenu( self )
  
    # other controllers for interfacing with other types
    self.person = PersonController(db,user)
    self.location = LocationController(db,user)
    self.item = ItemController(db,user)

  def start( self ):
    self.interface.start()
    
