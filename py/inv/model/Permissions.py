"""
  @file   Permissions.py
  @author Brian Kim
  @brief  definition of the Permissions class and 
          the methods necessary to persist 
          it into a database
"""

class Permissions():
  ItemCreate     = 1 << 0
  LocationCreate = 1 << 1
  AssetCreate    = 1 << 2
  PersonCreate   = 1 << 3
  LoanCreate     = 1 << 4
  ItemRead       = 1 << 5
  LocationRead   = 1 << 6
  AssetRead      = 1 << 7
  PersonRead     = 1 << 8
  LoanRead       = 1 << 9
  ItemUpdate     = 1 << 10
  LocationUpdate = 1 << 11
  AssetUpdate    = 1 << 12
  PersonUpdateUser  = 1 << 13
  PersonUpdateWorld = 1 << 14
  LoanUpdateUser  = 1 << 15
  LoanUpdateWorld = 1 << 16
  ItemDelete      = 1 << 17
  LocationDelete  = 1 << 18
  AssetDelete     = 1 << 19
  PersonDeleteUser  = 1 << 20
  PersonDeleteWorld = 1 << 21
  LoanDeleteUser    = 1 << 22
  LoanDeleteWorld   = 1 << 23
  info = {
    ItemCreate : 'add items',
    ItemRead   : 'lookup items',
    ItemUpdate : 'modify items',
    ItemDelete : 'remove items',
    LocationCreate : 'add locations',
    LocationRead   : 'lookup locations',
    LocationUpdate : 'modify locations',
    LocationDelete : 'remove locations',
    AssetCreate : 'add assets',
    AssetRead   : 'lookup assets',
    AssetUpdate : 'modify assets',
    AssetDelete : 'remove assets',
    PersonCreate : 'add person',
    PersonRead   : 'lookup people',
    PersonUpdateUser  : 'modify self',
    PersonUpdateWorld : 'modify others',
    PersonDeleteUser  : 'remove self',
    PersonDeleteWorld : 'remove others',
    LoanCreate : 'add loans',
    LoanRead   : 'lookup loans',
    LoanUpdateUser  : 'modify own loans',
    LoanUpdateWorld : 'modify other loans',
    LoanDeleteUser  : 'remove own loans',
    LoanDeleteWorld : 'remove other loans',
  }

  def __init__( self, value ):
    self.value = value

  def add( self, value ):
    self.value |= value

  def check( self, value ):
    return not (self.value & value == 0)

  def remove( self, value ):
    self.value &= ~value

  def __str__( self ):
    y = "permissions:\n"
    perms = [2**i for i in range(24)]
    for i in perms:
      y += '\t' + Permissions.info[i] + '\n' if self.check(i) else ''
    return y
  
