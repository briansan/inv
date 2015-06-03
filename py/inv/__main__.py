"""
  @file inv/__main__.py
  @author Brian Kim
  @brief the top level script to execute the 
         inventory system
"""
from model.Asset import Asset
from model.Location import Location
from model.Person import Person
from model.Item import Item
from getpass import getpass

DEBUG = 1
db = None

def display_header():
  print "************************************"
  print "              inv"
  print "             by: bk"
  print "************************************"

def init_db():
  if DEBUG > 0: print "\tinitializing database..."
  import sqlite3
  from os.path import expanduser
  home = expanduser('~')
  db_path = home + "/.inv.db"
  if DEBUG > 1: print db_path
  global db 
  db = sqlite3.connect(db_path)
  
  if DEBUG > 0: print "\tcreating tables..."
  Asset.DBHelper.create_table(db)
  Location.DBHelper.create_table(db)
  Person.DBHelper.create_table(db)
  Item.DBHelper.create_table(db)

  if DEBUG > 0: print "\tchecking admin acct..."
  chk = Person.DBHelper.create_admin(db)
  if DEBUG > 0 and not chk: print "\tadmin acct already exists..."
  elif DEBUG > 0 and chk: print "\tadmin acct successfully created!"

def main_menu():
  print ""
  print "Main Menu"
  print "1. Login"
  print "2. Register"
  print "3. Quit"
  print ""

  opt = input('Select your option: ')
  return opt

def login():
  print ""
  print "Login"

  # request credentials
  uname = raw_input('username: ')
  pw = getpass('password: ')

  # check credentials
  global db
  user = Person.DBHelper.get_by_uname(db,uname)
  if user:
    if Person.DBHelper.auth(db,user,pw):
      return user
    else:
      print "Wrong Password..."
      return None
  else:
    print "User does not exist..."
    return None

def register():
  print ""
  print "Registration"

  uname = raw_input("Username: ")
  pw = getpass("Password: ")
  pw_chk = getpass("Re-type Password: ")
  fname = raw_input("First Name: ")
  lname = raw_input("Last Name: ")
  phone = raw_input("Phone Number: ")
  email = raw_input("Email: ")

  if pw != pw_chk:
    print "Passwords don't match!"
    return register()

  # create user object
  user = Person(uname,fname,lname,phone,email)
  global db
  # try to create user into db
  uid = Person.DBHelper.add(db,user,pw)
  # check for success
  if uid == -1:
    print "User with that name already exists! Try again"
  else:
    print "Thank you for registering with inv!"
  return user

def user_main_menu( user ):
  global db
  print ""
  print "======================================"
  print "Welcome " + user.fname + " " + user.lname + "!"
  print "======================================"

  opt = 0
  while opt != 6:
    print ""
    print "Main Menu:"
    print "1. Assets"
    print "2. Loans"
    print "3. Items"
    print "4. Locations"
    print "5. People"
    print "6. Quit"
    print ""
    opt = input("Please select an option: ")
    
    if opt == 1:
      pass
    elif opt == 2:
      pass
    elif opt == 3:
      Item.CLI.main(db,user)
    elif opt == 4:
      pass
    elif opt == 5:
      pass
    elif opt == 6: 
      print "Goodbye!"

def asset_menu(user):
  pass 
def loan_menu(user):
  pass 
def item_menu(user):
  pass 
def location_menu(user):
  pass 
def people_menu(user):
  pass 

# main
if __name__ == "__main__":
  # init
  display_header()
  init_db()

  # start
  opt = main_menu()
  if opt == 1:   # login
    user = login()
    if user:
      user_main_menu(user)
  elif opt == 2: # register
    user = register()
    if user.id != -1:
      print "Welcome " + user.fname + " " + user.lname + "!"
      user_main_menu(user)
  elif opt == 3: # quit
    pass
  else:
    pass
