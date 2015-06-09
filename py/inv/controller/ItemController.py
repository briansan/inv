"""
  @file   ItemController.py
  @author BrianKim
  @brief  the controller that manages the item interface with the model
"""

from inv.view.cli.ItemMenu import ItemMenu
from inv.model.Item import Item
from inv.model.Person import Person

class ItemController( ItemMenu.Delegate ):
  #
  # ItemMenu delegate methods
  # 
  def itemMenuCheckUserPermission( self, action ):
    return self.user.permissions.check( action )

  def itemMenuListAll( self ):
    return Item.DBHelper.get_all( self.db )

  def itemMenuWantsEdit( self, item ):
    if Item.DBHelper.set( self.db, item ) == 1:
      return 0
    else:
      return -1

  def itemMenuWantsAdd( self, item ):
    if Item.DBHelper.add( self.db, item ) > 0:
      return 0
    else:
      return -1

  def itemMenuWantsDelete( self, item ):
    Item.DBHelper.delete( self.db, item )
    return 0

  def itemMenuLookupByManufacturer( self, mfc ):
    Item.DBHelper.get_by_manufacturer( self.db, item )

  def itemMenuLookupByCategory( self, cat ):
    Item.DBHelper.get_by_category( self.db, cat )

  #
  # lifecycle methods
  #
  def __init__( self, db, user ):
    self.db = db
    self.user = user
    self.interface = ItemMenu( self )

  def start( self ):
    self.interface.main()
    
