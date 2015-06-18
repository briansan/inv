"""
  @file   Loan.py
  @author Brian Kim
  @brief  definition of the Loan class and 
          the methods necessary to persist 
          it into a database
"""

from Item import Item
from Location import Location
from Person import Person
from Asset import Asset
import calendar
import time
import datetime

class Asset():
  class Status():
    Requested = 0
    Approved  = 1
    Loaned    = 2
    Returned  = 3
    info = {
      Requested : "Requested",
      Approved  : "Approved",
      Loaned    : "Loaned",
      Returned  : "Returned"
    }
  def __init__( self, items=[], status=Asset.Status.Requested, who=Person(),
                      create=datetime.datetime.now(),
                      start=datetime.datetime.now(), 
                      due=datetime.datetime.now(), 
                      returnDate=datetime.datetime.now(), id=0 )
    """
    constructor method
      $<list: Assets> items
      $<LoanStatus> status
      $<Person> who
      $<Date> create, start, due, return
    """
    # init by field
    self.items = items
    self.status = status
    self.who = who
    self.create = create
    self.start = start
    self.due = due
    self.returnDate = returnDate
    self.id = id

  def __str__( self ):
    y = 'Loan #' + str(self.id) + 'to '+self.who ': \n' 
    y += '\trequested: '+str(self.create)+'\n'
    if self.status > Asset.Status.Requested:
      y += '\tapproved: '+str(self.start)+'\n'
    if self.status > Asset.Status.Approved:
      y += '\tdue: '+str(self.due)+'\n'
    if self.status > Asset.Status.Returned:
      y += '\treturned: '+str(self.returnDate)+'\n'
    return y

  @staticmethod
  def init_from_db_row( db, row ):
    id     = row[0]
    items  = row[1]
    status = row[2]
    who    = Person.DBHelper.get(row[3])
    create = datetime.datetime.fromtimestamp(row[4])
    start  = datetime.datetime.fromtimestamp(row[5])
    due    = datetime.datetime.fromtimestamp(row[6])
    rdate  = datetime.datetime.fromtimestamp(row[7])
    return Loan( items, status, who, create, start, due, rdate )

  class DBHelper():
    @staticmethod
    def create_table( db ):
      db.execute('''CREATE TABLE IF NOT EXISTS loans 
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         ece_tag TEXT NOT NULL,
         vu_tag TEXT NOT NULL,
         service_tag TEXT NOT NULL,
         serial_number TEXT NOT NULL,
         item INTEGER NOT NULL,
         price REAL NOT NULL,
         purchased INTEGER NOT NULL,
         deployed INTEGER NOT NULL,
         img TEXT NOT NULL,
         inventoried INTEGER NOT NULL,
         disposed INTEGER NOT NULL,
         status INTEGER NOT NULL,
         home INTEGER NOT NULL,
         dest INTEGER NOT NULL,
         loanable INTEGER NOT NULL,
         owner INTEGER NOT NULL,
         holder INTEGER NOT NULL
        ); ''')
      db.execute("INSERT OR IGNORE INTO assets (id,ece_tag,vu_tag,service_tag,serial_number,item,price,purchased,deployed,img,inventoried,disposed,status,home,dest,loanable,owner,holder) values (0,'','','','',0,0,0,0,'',0,0,0,0,0,0,0,0)")
      
      db.commit()
    
    @staticmethod
    def add( db, asset ):
      args = (asset.ece_tag, asset.vu_tag, asset.service_tag, 
              asset.serial_number, asset.item.id, asset.price,
              int(asset.purchased.strftime("%s")), int(asset.deployed.strftime("%s")), 
	      asset.img, int(asset.inventoried.strftime("%s")), 
              int(asset.disposed.strftime("%s")), asset.status,
              asset.home.id, asset.dest.id, asset.loanable, asset.owner.id, asset.holder.id)
      c = db.execute( "INSERT INTO assets (ece_tag,vu_tag,service_tag,serial_number,item,price,purchased,deployed,img,inventoried,disposed,status,home,dest,loanable,owner,holder) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", args )
      db.commit()
      return c.lastrowid

    @staticmethod
    def delete( db, asset ):
      db.execute( "DELETE FROM assets WHERE id=?", (asset.id,) )
      db.commit()

    @staticmethod
    def get( db, id ):
      c = db.execute( "SELECT * FROM assets WHERE id=?", (id,) )
      # fetch a row (should only be one)
      rows = c.fetchone()
      if not rows == None:
        return Asset.init_from_db_row( db, rows )
      else:
        return None

    @staticmethod
    def get_by_tag( db, tag, tag_t='ece' ):
      q = "SELECT * FROM assets WHERE " + tag_t + "_tag=?"
      c = db.execute( q, (tag,) )
      rows = c.fetchone()
      if not rows == None:
        return Asset.init_from_db_row( db, rows )
      else:
        return None

    @staticmethod
    def get_by_item( db, item ):
      c = db.execute( "SELECT * FROM assets WHERE item=?", (item.id,) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_status( db, status ):
      c = db.execute( "SELECT * FROM assets WHERE status=?", (status,) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_owner( db, owner ):
      c = db.execute( "SELECT * FROM assets WHERE owner=?", (owner.id,) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_holder( db, owner ):
      c = db.execute( "SELECT * FROM assets WHERE owner=?", (owner.id,) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_home( db, owner ):
      c = db.execute( "SELECT * FROM assets WHERE home=?", (owner.id,) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_dest( db, owner ):
      c = db.execute( "SELECT * FROM assets WHERE dest=?", (owner.id,) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_all( db ):
      c = db.execute( "SELECT * FROM assets WHERE id>0" )
      y = []
      for rows in c.fetchall():
        y.append( Asset.init_from_db_row(db,rows))
      return y

    @staticmethod
    def set( db, asset ):
      if asset.id == 0:
        raise Exception( 'Asset: DBHelper: set: invalid id' )
      # do a little validation
      item_id = 0 if not asset.item else asset.item.id
      home_id = 0 if not asset.home else asset.home.id
      dest_id = 0 if not asset.dest else asset.dest.id
      owner_id = 0 if not asset.owner else asset.owner.id
      holder_id = 0 if not asset.holder else asset.holder.id
      args = (asset.ece_tag, asset.vu_tag, asset.service_tag, 
              asset.serial_number, item_id, asset.price,
              asset.purchased, asset.deployed, asset.img, 
              asset.inventoried, asset.disposed, asset.status,
              home_id, dest_id, asset.loanable, 
              owner_id, holder_id, asset.id)
      c = db.execute( "UPDATE assets SET ece_tag=?,vu_tag=?,service_tag=?,serial_number=?,item=?,price=?,purchased=?,deployed=?,img=?,inventoried=?,disposed=?,status=?,home=?,dest=?,loanable=?,owner=?,holder=? WHERE id=?", args) 
      db.commit()
      return c.rowcount

if __name__ == "__main__":
  print "========================="
  print "Asset database test:"
  print "========================="
  import sqlite3
  db = sqlite3.connect('inv.db')
  print "Test 1: create table"
  Asset.DBHelper.create_table(db)
  print "Test 1: success"
  print "========================="
  print "Test 2: Create"
  # create a person
  p = Person( 'user1', 'John', 'Doe', '8005550123', 0, 1, 0 )
  p_pw = 'passwd1'
  print "adding person" + str(p)
  p.id = Person.DBHelper.add( db, p, p_pw )
  # create an item
  i = Item( 'Monitor', 'Dell', 'E172FPb' )
  print "adding item: " + str(i)
  i.id = Item.DBHelper.add( db, i )
  # create a location
  l = Location( 'CEER', '008' )
  print "adding location: " + str(l)
  l.id = Location.DBHelper.add( db, l )
  # using arbitrary dates
  now = calendar.timegm(time.gmtime())
  # create the asset
  a = Asset( 'ee06637', 'vu11647', '', '031120-00', i, 200.00, now, now, '', 
             now, 0, Asset.Status.Found, l, l, True, p, p )
  print "adding asset: " + str(a)
  Asset.DBHelper.add( db, a )
  print "Test 2: success"
  print "========================="
  print "Test 3: Read"
  print ""
  print "get by tag..."
  asset = Asset.DBHelper.get_by_tag( db, 'ee06637' )
  print str(asset)
  print ""
  print "get all..."
  assets = Asset.DBHelper.get_all( db )
  for l in assets:
    print str(l.id) + '. ' + str(l)
  print "Test 3: success"
  print "========================="
  print "Test 4: Update"
  print "updating " + str(l)
  for l in assets:
    l.ece_tag = 'ee00000'
    print "to " + str(l)
    Asset.DBHelper.set(db,l)
  print "Test 4: success"
  print "========================="
  print "Test 5: Delete"
  print "deleting " + str(l)
  Asset.DBHelper.delete( db, l.id )
  print "Test 5: success"
  print "========================="
  print "Asset database test succeeded"
  print "========================="
