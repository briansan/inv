"""
  @file   ItemMenu.py
  @author Brian Kim
  @brief  definition of the command-line interface
          of the item menus
"""

from inv.model.Permissions import Permissions

class ItemMenu():
  class Delegate():
    def UserHasItemMenuPermission( self, action ):
      """
      delegate method to determine whether a user has permission
      to perform a certain action
      """
      return False

    #
    # view methods
    #

    def ItemMenuLookupByManufacturer( self, manufacturer ):
      """
      """
      return []

    def ItemMenuLookupByCategory( self, category ):
      """
      """
      return False

  def main( self ):
    pass
