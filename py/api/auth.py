"""
  @file   VULDAPAuth.py
  @author Brian Kim
  @brief  a script that authenticates a user using 
          the Villanova LDAP server
"""

def auth_ldap(uid,passwd):
  """
   using ldap to authenticate the user
  """
  import ldap

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

def auth_inv(uname,passwd):
  """
   inv authentication 
  """
  from model import User

  # try ldap
  y = auth_ldap(uname,passwd)
  # success
  if type(y) is tuple:
    # search for user in db
    u = User.query.filter_by(uname=uname).first()
    if not u: # user does not exist...
      from methods import DefaultPermissions
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
      u = User(uname,fname,lname,grp,perm)
      # add user to db
      from model import db
      db.session.add(u)
      db.session.commit()
    return u
      
  # failure
  elif type(y) is str: 
    return y

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
