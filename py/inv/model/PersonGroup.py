"""
  @file   PersonGroup.py
  @author Brian Kim
  @brief  definition of the PersonGroup class  
          including the default permissions
          associated with each
"""

from Permissions import *

class PersonGroup():
  NoneType  = 0
  Guest    = 1
  Student  = 2 
  Staff    = 3
  Faculty  = 4 
  Admin    = 5
  info = {
    NoneType  : 'Anonymous',
    Guest     : 'Guest',
    Student   : 'Student',
    Staff     : 'Staff',
    Faculty   : 'Faculty',
    Admin     : 'Admin',
  }
  permissions = {
    NoneType  : Permissions.PersonCreate,
    Guest     : Permissions.ItemRead | 
                Permissions.LocationRead | 
                Permissions.PersonRead | 
                Permissions.PersonUpdateUser | 
                Permissions.PersonDeleteUser | 
                Permissions.AssetRead | 
                Permissions.LoanCreate | 
                Permissions.LoanRead | 
                Permissions.LoanUpdateUser | 
                Permissions.LoanDeleteUser,
    Student   : Permissions.ItemRead | 
                Permissions.LocationRead | 
                Permissions.PersonRead | 
                Permissions.PersonUpdateUser | 
                Permissions.PersonDeleteUser | 
                Permissions.AssetRead | 
                Permissions.LoanCreate | 
                Permissions.LoanRead | 
                Permissions.LoanUpdateUser | 
                Permissions.LoanDeleteUser,
    Staff     : Permissions.ItemCreate | 
                Permissions.ItemRead | 
                Permissions.ItemUpdate | 
                Permissions.ItemDelete | 
                Permissions.LocationCreate | 
                Permissions.LocationRead | 
                Permissions.LocationUpdate | 
                Permissions.LocationDelete |
                Permissions.PersonRead | 
                Permissions.PersonUpdateUser | 
                Permissions.PersonDeleteUser | 
                Permissions.AssetCreate | 
                Permissions.AssetRead | 
                Permissions.AssetUpdate | 
                Permissions.AssetDelete |
                Permissions.LoanCreate | 
                Permissions.LoanRead | 
                Permissions.LoanUpdateUser | 
                Permissions.LoanDeleteUser,
    Faculty   : Permissions.ItemCreate | 
                Permissions.ItemRead | 
                Permissions.ItemUpdate | 
                Permissions.ItemDelete | 
                Permissions.LocationCreate | 
                Permissions.LocationRead | 
                Permissions.LocationUpdate | 
                Permissions.LocationDelete |
                Permissions.PersonRead | 
                Permissions.PersonUpdateUser | 
                Permissions.PersonDeleteUser | 
                Permissions.AssetCreate | 
                Permissions.AssetRead | 
                Permissions.AssetUpdate | 
                Permissions.AssetDelete |
                Permissions.LoanCreate | 
                Permissions.LoanRead | 
                Permissions.LoanUpdateUser | 
                Permissions.LoanDeleteUser,
    Admin     : Permissions.ItemCreate | 
                Permissions.ItemRead | 
                Permissions.ItemUpdate | 
                Permissions.ItemDelete | 
                Permissions.LocationCreate | 
                Permissions.LocationRead | 
                Permissions.LocationUpdate | 
                Permissions.LocationDelete |
                Permissions.PersonCreate | 
                Permissions.PersonRead | 
                Permissions.PersonUpdateUser | 
                Permissions.PersonUpdateWorld | 
                Permissions.PersonDeleteUser | 
                Permissions.PersonDeleteWorld | 
                Permissions.AssetCreate | 
                Permissions.AssetRead | 
                Permissions.AssetUpdate | 
                Permissions.AssetDelete | 
                Permissions.LoanCreate | 
                Permissions.LoanRead | 
                Permissions.LoanUpdateUser | 
                Permissions.LoanUpdateWorld | 
                Permissions.LoanDeleteUser | 
                Permissions.LoanDeleteWorld,
  }

