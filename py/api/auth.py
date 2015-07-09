"""
  @file   VULDAPAuth.py
  @author Brian Kim
  @brief  a script that authenticates a user using 
          the Villanova LDAP server
"""

import ldap
from getpass import getpass

uid = raw_input('Username: ')
passwd = getpass('Password: ')

conn = ldap.initialize('ldaps://ldaps.villanova.edu')
results = conn.search_s('o=villanova.edu',ldap.SCOPE_SUBTREE,'uid='+uid)
if len(results) != 1:
  print 'Invalid Username'
  exit()
else:
  info = results[0]
  dn = info[0]
  try:
    chk = conn.bind_s(dn,passwd)
  except:
    print 'Wrong Password'
    exit()

print 'Welcome ' + info[1]['cn'][0] + '!'
