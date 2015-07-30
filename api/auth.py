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
  """
  OLD 
  - pip installing the ldap is a pain in the butt
  - connecting to the ldap server requires passing an ip filter
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
  """
  print uid

  return get_ldap_info( uid, passwd, uid, ['givenname','sn','ou'] )


def get_ldap_info( uname, passwd, uid="bkim11", keys=["dn"] ):
  # get ldap info
  import base64, getpass, requests
  filt = {'filter':'uid=%s'%uid} # url encode the data
  url = 'https://vecr.ece.villanova.edu/cgi/auth/ldapsearch/'
  r = requests.post(url,auth=(uname,passwd),data=filt)
  res = r.text
  # parse through response
  y = {}
  for line in res.splitlines():
    for key in keys:
      if key in line:
        print line
        kv = line.split(':')
        # preventing index out of range errors
        if len(kv) > 1:
          # already existing values should be put into a list
          if y.get(kv[0]):
            # if it's already a list then we can skip the next line
            if not (type(y.get(kv[0])) == list):
              y[kv[0]] = [ y[kv[0]] ]
            # add it to the list
            y[kv[0]].append(kv[1])
          else:
            y[kv[0]] = kv[1]
  print y
  return y



def auth_inv(uname_or_token,passwd_or_method):
  """
   inv authentication 
  """
  from model import User

  # try token
  u = User.verify_auth_token(uname_or_token)

  if not u:
    # try ldap
    y = auth_ldap(uname_or_token,passwd_or_method)
    # success
    if 'givenname' in y:
      # search for user in db
      u = User.query.filter_by(uname=uname_or_token).first()
      if not u: # user does not exist...
        # get the name
        fname = y['givenname']
        lname = y['sn']
        # get the group type
        ou = y['ou'] # ou = organizational unit
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
  else:
    return False


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
