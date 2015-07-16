"""
  @file   Person.py
  @author Brian Kim
  @brief  definition of the Person class and 
          the methods necessary to persist 
          it into a database
"""

import md5
from Permissions import Permissions
from PersonGroup import PersonGroup

class Person():
  def __init__( self, uname="", fname="", lname="", phone="", email="",
                      ptype=PersonGroup.Guest, permissions=PersonGroup.permissions[PersonGroup.Guest], year=0, id=0):
    # init by database row
    if fname == None:
      self.id = uname[0]
      self.uname = uname[1]
      self.fname = uname[2]
      self.lname = uname[3]
      self.phone = uname[4]
      self.email = uname[5]
      self.ptype = uname[6]
      self.permissions = Permissions(int(uname[8]))
      self.year = uname[7]
      return

    # init by field
    self.uname = uname
    self.fname = fname
    self.lname = lname
    self.phone = phone
    self.email = email

    # person type check
    ptype = ptype if ptype else PersonGroup.Guest
    self.ptype = ptype

    # permissions can be blank
    self.permissions = Permissions(permissions if permissions else PersonGroup.permissions[ptype])
    self.year = year
    self.id = id

  def __str__( self ):
    return self.uname +' ('+self.fname+' '+self.lname+')'

  @staticmethod
  def init_from_db_row( db, row ):
    id = row[0]
    uname = row[1]
    fname = row[2]
    lname = row[3]
    phone = row[4]
    email = row[5]
    ptype = row[6]
    permissions = int(row[8])
    year = row[7]
    return Person(uname,fname,lname,phone,email,ptype,permissions,year,id)
  
  class DBHelper():
    @staticmethod
    def create_table( db ):
      db.execute('''CREATE TABLE IF NOT EXISTS persons 
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         uname TEXT NOT NULL,
         passwd TEXT NOT NULL,
         fname TEXT NOT NULL,
         lname TEXT NOT NULL,
         phone TEXT NOT NULL,
         email TEXT NOT NULL,
         ptype INTEGER NOT NULL,
         year INTEGER NOT NULL,
         permissions INTEGER NOT NULL); ''')
      db.execute('INSERT OR IGNORE INTO persons (id,uname,passwd,fname,lname,phone,email,ptype,year,permissions) values (0,"","","","","","",0,0,0)')
      db.commit()
    
    @staticmethod
    def add( db, person, pw ):
      # check if user already exists
      chk = Person.DBHelper.get_by_uname( db, person.uname )
      if chk:
        return -1
      phash = md5.md5(pw).hexdigest()
      args = (person.uname, phash, person.fname, person.lname, person.phone, person.email,
              person.ptype, person.year, person.permissions.value)
      c = db.execute( "INSERT INTO persons (uname,passwd,fname,lname,phone,email,ptype,year,permissions) values (?,?,?,?,?,?,?,?,?);", args )
      db.commit()
      person.id = c.lastrowid
      return person.id

    @staticmethod
    def create_admin( db ):
      c = db.execute( "SELECT id FROM persons WHERE uname='admin'" )
      row = c.fetchone()
      if row:
        return False
      else:
        user = Person( 'admin', 'Admin', 'istrator', '8005550123', 'admin@inv.com', PersonGroup.Admin )
        Person.DBHelper.add( db, user, 'password' )
        return True

    @staticmethod
    def delete( db, user ):
      db.execute( "DELETE FROM persons WHERE id=?", (user.id,) )
      db.commit()

    @staticmethod
    def get( db, id ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE id=?", (id,) )
      # fetch a row (should only be one)
      rows = c.fetchone()
      if not rows == None:
        return Person.init_from_db_row(db, rows )
      else:
        return None

    @staticmethod
    def auth( db, person, pw ):
      # hash the password
      phash = md5.md5(pw).hexdigest()
      # fetch the person and check the hash
      c = db.execute( 'SELECT passwd FROM persons WHERE id=?', (person.id,) )
      truehash = c.fetchone()[0]
      # compare it against the 
      if phash == truehash:
        return True
      else:
        return False

    @staticmethod
    def get_by_fname( db, fname ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE fname LIKE '%?%'", (fname,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_lname( db, fname ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE lname=?", (lname,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_uname( db, uname ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE uname=?", (uname,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_phone( db, phone ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE phone=?", (phone,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_email( db, email ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE email=?", (email,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_type( db, ptype ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE ptype=?", (ptype,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_year( db, year ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE year=?", (year,) )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_all( db ):
      c = db.execute( "SELECT id,uname,fname,lname,phone,email,ptype,year,permissions FROM persons WHERE id>0" )
      y = []
      for rows in c.fetchall():
        y.append( Person.init_from_db_row(db, rows ))
      return y

    @staticmethod
    def set( db, person ):
      if person.id == 0:
        raise Exception( 'Person: DBHelper: set: invalid id' )
      args = (person.uname, person.fname, person.lname, person.phone, person.email,
              person.ptype, person.year, person.permissions.value, person.id)
      c = db.execute( "UPDATE persons SET uname=?,fname=?,lname=?,phone=?,email=?,ptype=?,year=?,permissions=? WHERE id=?", args) 
      db.commit()
      return c.rowcount

    @staticmethod
    def update_pw( db, person, pw ):
      phash = md5.md5(pw).hexdigest()
      args = (phash,person.id)
      c = db.execute( "UPDATE persons SET passwd=? WHERE id=?", args )
      db.commit()

if __name__ == "__main__":
  print "========================="
  print "Person database test:"
  print "========================="
  import sqlite3
  db = sqlite3.connect('inv.db')
  print "Test 1: create table"
  Person.DBHelper.create_table(db)
  print "Test 1: success"
  print "========================="
  print "Test 2: Create"
  p1 = Person( 'user1', 'John', 'Doe', '8005550123', 0, 1, 0 )
  p1_pw = 'passwd1'
  p2 = Person( 'user2', 'Jane', 'Doe', '8005550124', 1, 1, 1 )
  p2_pw = 'passwd2'
  p3 = Person( 'user3', 'John', 'Smith', '8005550125', 1, 0, 1 )
  p3_pw = 'passwd3'
  print "adding " + str(p1)
  Person.DBHelper.add( db, p1, p1_pw )
  print "adding " + str(p2)
  Person.DBHelper.add( db, p2, p2_pw )
  print "adding " + str(p3)
  Person.DBHelper.add( db, p3, p3_pw )
  print "Test 2: success"
  print "========================="
  print "Test 3: Read"
  print ""
  print "get by first name (John)..."
  persons = Person.DBHelper.get_by_fname( db, 'John' )
  for l in persons:
    print str(l.id) + '. ' + str(l)
  print ""
  print "get all..."
  persons = Person.DBHelper.get_all( db )
  for l in persons:
    print str(l.id) + '. ' + str(l)
  print "Test 3: success"
  print "========================="
  print "Test 4: Authentication"
  import getpass
  pw = getpass.getpass('password for '+str(l)+': ')
  if Person.DBHelper.auth(db,l,pw):
    print "correct!"
  else:
    print "wrong pw..."
  print "Test 4: success"
  print "========================="
  print "Test 5: Update"
  for l in persons:
    print "updating " + str(l)
    l.last = 'Tolentine'
    print "to " + str(l)
    Person.DBHelper.set(db,l)
  print "Test 5: success"
  print "========================="
  print "Test 6: Delete"
  for l in persons:
    print "deleting " + str(l)
    Person.DBHelper.delete( db, l.id )
  print "Test 6: success"
  print "========================="
  print "Person database test succeeded"
  print "========================="
