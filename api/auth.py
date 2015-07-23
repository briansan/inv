"""
  @file   inv/api/auth.py
  @author Brian Kim
  @brief  a script that handles the authentication and authorization of a user
          for inv
"""

from methods import *

# definition of default permissions
DefaultStudentPermissions = UserReadSelf | UserUpdateSelf | ItemRead | LocationRead | AssetRead | InvRead | \
                            LocBuildView | ItemCatView | ItemManView
DefaultFacultyPermissions = DefaultStudentPermissions | UserReadWorld | InvCreate
DefaultOperatorPermissions = DefaultFacultyPermissions | ItemCreate | ItemUpdate | \
                             LocationCreate | LocationUpdate | AssetCreate | AssetUpdate
DefaultAdminPermissions = DefaultOperatorPermissions | UserUpdateWorld | UserDelete | ItemDelete | \
                          LocationDelete | AssetDelete | InvUpdate | InvDelete | \
                          LocBuildEdit | ItemCatEdit | ItemManEdit

from model import User
DefaultPermissions = {
  User.Groups.NoGroup: LogInOut,
  User.Groups.Student: DefaultStudentPermissions,
  User.Groups.Faculty: DefaultFacultyPermissions,
  User.Groups.Operator: DefaultOperatorPermissions,
  User.Groups.Admin: DefaultAdminPermissions
}

# definition of authorization object
class Authorization():
  """
   use this class to pass in a permission integer value
   and parse out the permissions of all the methods
  """
  def __init__(self,val):
    """
     initialize the authorization obj with
     some value equal to the bit string
     of values from above
    """
    self.val = val
  def add(self,val):
    """
     adds a method permission to the value
     varaible using a bitwise-or
    """
    self.val |= val
  def chk(self,val):
    """
     checks the presence of a permission
     by doing a bitwise-and and testing for non 0
    """
    return not (self.val & val == 0)
  def rm(self,val):
    """
     removes a method permission from the value
     by doing a bitwise-and with the permission's bit value
    """
    self.val &= ~val

def auth_ldap(uid,passwd):
  """
   using ldap to authenticate the user
  """
  import ldap
  if not passwd or len(passwd) is 0:
    return 'Bad Password'

  conn = ldap.initialize('ldaps://ldaps.villanova.edu')
  results = conn.search_s('o=villanova.edu',ldap.SCOPE_SUBTREE,'uid='+uid)
  if len(results) != 1:
    return 'Invalid Username'
  else:
    info = results[0]
    dn = info[0]
    try:
      chk = conn.bind_s(dn,passwd)
    except:
      return 'Wrong Password'
  return info

def auth_inv(uname_or_token,passwd_or_method):
  """
   inv authentication 
  """
  from model import User

  # try token
  u = User.verify_auth_token(uname_or_token)
  if u:
    return u

  else:
    # try ldap
    y = auth_ldap(uname_or_token,passwd_or_method)
    # success
    if type(y) is tuple:
      # search for user in db
      u = User.query.filter_by(uname=uname_or_token).first()
      if not u: # user does not exist...
        # get the name
        fname = y[1]['givenname'][0]
        lname = y[1]['sn'][0]
        # get the group type
        ou = y[1]['ou'] # ou = organizational unit
        grp = User.Groups.NoGroup
        if 'Students' in ou:
          grp = User.Groups.Student
        elif 'Employees' in ou:
          grp = User.Groups.Employee
        # set permissions
        perm = DefaultPermissions[grp]
        # create the user
        u = User(uname_or_token,fname,lname,grp,perm)
        # add user to db
        from model import db
        db.session.add(u)
        db.session.commit()

  if u:
    from flask import g
    g.user = u
    return u
      
  # failure
  if type(y) is str: 
    return False

  # other?
  else:
    raise Exception('The impossible has happened')

def auth_io(inv=False):
  """
   an interactive authentication
  """
  from getpass import getpass
  uid = raw_input('Username: ')
  passwd = getpass('Password: ')
  if inv:
    print dict(auth_inv(uid,passwd))
  else:
    print auth_ldap(uid,passwd)
  
if __name__=="__main__":
  import sys
  if len(sys.argv) == 2 and sys.argv[1]=='inv':
    from app import create_app
    app = create_app('conf/debug.cfg')
    with app.app_context():
      auth_io(True)
  else:
    auth_io()
