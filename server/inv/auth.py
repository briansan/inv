"""
  @file   inv/api/auth.py
  @author Brian Kim
  @brief  a script that handles the authentication and authorization of a user
          for inv
"""

#
# definition methods as bits
# Label: Category, Manufacturer, Building
# Subentity: User, Location, Item
# Entity: Asset, Inventory
LabelView         = 1 << 0
SubentityView     = 1 << 1
EntityView        = 1 << 2
EntityModify      = 1 << 3
EntityModifyWorld = 1 << 4
SubentityModify   = 1 << 5
LabelModify       = 1 << 6
UserModifyWorld   = 1 << 7

# definition of default permissions
DefaultStudentPermissions = LabelView | SubentityView | EntityView
DefaultFacultyPermissions = DefaultStudentPermissions | EntityModify
DefaultOperatorPermissions = DefaultFacultyPermissions | EntityModifyWorld | SubentityModify | LabelModify
DefaultAdminPermissions = DefaultOperatorPermissions | UserModifyWorld

from model import User
DefaultPermissions = {
  User.Groups.NoGroup: LabelView | SubentityView,
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

  return get_ldap_info( uid, passwd, uid, ['givenname','sn','ou','mail','employeecampusphone','mobile'] )


def get_ldap_info( uid, passwd, who="cbannan", keys=["dn"] ):
  # get ldap info
  import base64, getpass, requests
  filt = {'filter':'uid=%s'%who} # url encode the data
  url = 'https://vecr.ece.villanova.edu/cgi/auth/ldapsearch/'
  r = requests.post(url,auth=(uid,passwd),data=filt)
  res = r.text
  # parse through response
  y = {}
  for line in res.splitlines():
    for key in keys:
      if key in line:
        kv = line.split(':')
        # preventing index out of range errors
        if len(kv) > 1:
          key = kv[0]
          val = kv[1].strip(' ')
          # already existing values should be put into a list
          if y.get(key):
            # if it's already a list then we can skip the next line
            if not (type(y.get(key)) == list):
              y[key] = [ y[key] ]
            # add it to the list
            y[key].append(val)
          else:
            y[key] = val
  return y



def auth_inv(uid_or_token,passwd_or_method):
  """
   inv authentication 
  """
  from model import User

  # try token
  u = User.verify_auth_token(uid_or_token)

  if not u:
    # try ldap
    y = auth_ldap(uid_or_token,passwd_or_method)
    # success
    if 'givenname' in y:
      # search for user in db
      u = User.query.filter_by(uid=uid_or_token).first()
      if not u: # user does not exist...
        # get the name
        fname = y['givenname'][0] if type(y['givenname']) == list else y['givenname'] 
        lname = y['sn']
        # get the group type
        ou = y['ou'] # ou = organizational unit
        grp = User.Groups.NoGroup
        if 'Students' in ou:
          grp = User.Groups.Student
        elif 'Employees' in ou:
          grp = User.Groups.Employee

        admins = ['bkim11','cbannan','psingh']
        operators = ['rkarrant','hcook']
        # check admins
        uid = uid_or_token
        if uid in admins:
          grp = User.Groups.Admin
        # check operators
        if uid in operators:
          grp = User.Groups.Operator

        # set permissions
        perm = DefaultPermissions[grp]

        # get email
        email = y.get('mail')
        phone = y.get('employeecampusphone')
        if phone is None:
          phone = y.get('mobile')
        # create the user
        u = User(uid_or_token,fname,lname,grp,perm,email,phone)
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
