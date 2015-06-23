"""
  @file   Asset.py
  @author Brian Kim
  @brief  definition of the Asset class and 
          the methods necessary to persist 
          it into a database
"""

from Item import Item
from Location import Location
from Person import Person
import calendar
import time
import datetime

class Asset():
  class Status():
    Purchased = 0
    Found = 0
    Loaned = 1
    Lost  = 2
    Discarded = 3
    Sold    = 4
    Transferred = 5
    Traded  = 6
    Donated = 7
    info = {
      Purchased : "Purchased",
      Found : "Found",
      Loaned : "Loaned Out",
      Lost  : "Lost",
      Discarded : "Discarded",
      Sold : "Sold",
      Transferred : "Transferred",
      Traded : "Traded",
      Donated : "Donated",

    }
  def __init__( self, ece_tag='', vu_tag='', service_tag='', serial_number='',
                      item=Item(), price=0, purchased=datetime.datetime.now(),
                      deployed=datetime.datetime.now(), img='', 
                      inventoried=datetime.datetime.now(), 
                      disposed=datetime.datetime.fromtimestamp(0), 
                      status=0, home=Location(), dest=Location(),
                      loanable=False, owner=Person(), holder=Person(), id=0):
    """
    constructor method
      $<str> ece_tag, vu_tag, service_tag, serial_number
      $<Item> item
      $<float> price
      $<Date> purchased, deployed, inventoried, disposed
      $<str> img
      $<AssetStatus> status
      $<Location> home, dest
      $<bool> loanable
      $<Person> owner, holder
    """
    # init by field
    self.ece_tag = ece_tag
    self.vu_tag  = vu_tag
    self.service_tag = service_tag
    self.serial_number = serial_number
    self.item = item
    self.price = price
    self.purchased = purchased
    self.deployed = deployed
    self.img = img
    self.inventoried = inventoried
    self.disposed = disposed
    self.status = status
    self.home = home
    self.dest = dest
    self.loanable = loanable
    self.owner = owner
    self.holder = holder
    self.id = id

  def __str__( self ):
    return self.ece_tag + ': ' + str(self.item)

  @staticmethod
  def init_from_db_row( db, row ):
    id     = row[0]
    ecetag = row[1]
    vutag  = row[2]
    svctag = row[3]
    serial = row[4]
    item   = Item.DBHelper.get(db,row[5])
    price  = row[6]
    purch  = datetime.datetime.fromtimestamp(row[7])
    deploy = datetime.datetime.fromtimestamp(row[8])
    img    = row[9]
    inv    = datetime.datetime.fromtimestamp(row[10])
    dispose= datetime.datetime.fromtimestamp(row[11])
    status = row[12]
    home   = Location.DBHelper.get(db,row[13])
    dest   = Location.DBHelper.get(db,row[14])
    loan   = row[15]
    owner  = Person.DBHelper.get(db,row[16])
    holder = Person.DBHelper.get(db,row[17])
    return Asset( ecetag, vutag, svctag, serial, item, price, purch, deploy, img, inv, dispose, status, home, dest, loan, owner, holder, id )

  class DBHelper():
    @staticmethod
    def create_table( db ):
      db.execute('''CREATE TABLE IF NOT EXISTS assets 
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
 
  class FileParser():
    @staticmethod
    def loadJSON( fname ):
      import json
      with open(fname) as fp:
        json_str = fp.read()
        asset_list = json.loads(json_dict)         
        for asset in asset_list:
          ecetag = asset['ECETag']
          vutag  = asset['VUTag']
          svctag = asset['SvcTag']
          serial = asset['Serial']
          category = asset['Category']
          manufacturer = asset['Manufacturer']
          model  = asset['Model']
          price  = asset['Price']
          purchased = asset['Purchased']
          img    = asset['img']
          invetoried = asset['LastInventory']
	  home_b = asset['HomeBuilding']
	  home_r = asset['HomeRoom']
          dest_b = asset['DestBuilding']
          dest_r = asset['DestRoom']
          

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
