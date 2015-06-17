"""
  @file   Item.py
  @author Brian Kim
  @brief  definition of the Item class and 
          the methods necessary to persist 
          it into a database
"""

from Permissions import Permissions

class Item():
  """
  the class that defines an item of a certain
  category, manufacturer, and model
  """
  def __init__( self, category="None", manufacturer="", model="", id=0 ):
    """
    constructor method
    """
    self.category = category
    self.manufacturer = manufacturer
    self.model = model
    self.id = id

  def __str__( self ):
    """
    manufacturer model (category)
    """
    return self.manufacturer+' '+self.model+' ('+self.category+')'
  
  class DBHelper():
    @staticmethod
    def create_table( db ):
      """
      creates the table in the database
        $<int> id
        $<str> category
        $<str> manufacturer
        $<str> model
      """
      db.execute('''CREATE TABLE IF NOT EXISTS items 
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         category TEXT NOT NULL,
         manufacturer TEXT NOT NULL,
         model TEXT NOT NULL); ''')
      db.execute( 'INSERT OR IGNORE INTO items (id,category,manufacturer,model) values (0,"None","","")')
      db.commit()
    
    @staticmethod
    def add( db, item ):
      """
      creates a row in the Item table using the
      input Item object
      """
      args = (item.category, item.manufacturer, item.model)
      c = db.execute( "INSERT INTO items (category,manufacturer,model) values (?,?,?);", args )
      db.commit()
      return c.lastrowid

    @staticmethod
    def delete( db, item ):
      """
      deletes a row in the Item table using the
      id of the Item
      """
      db.execute( "DELETE FROM items WHERE id=?", (item.id,) )
      db.commit()

    @staticmethod
    def get( db, id ):
      """
      returns an Item object specified by 'id'
      from the Item table in the database specified by 'db' 
      """
      c = db.execute( "SELECT * FROM items WHERE id=?", (id,) )
      # fetch a row (should only be one)
      rows = c.fetchone()
      if not rows == None:
        return Item( rows[1], rows[2], rows[3], rows[0] )
      else:
        return None

    @staticmethod
    def get_categories( db ):
      """
      returns a list of all the distinct categories
      in the item table
      """
      c = db.execute( "SELECT DISTINCT category FROM items" )
      y = [] 
      for rows in c.fetchall():
        y = append( rows[0] )
      return y

    @staticmethod
    def get_by_category( db, category ):
      """
      returns all the rows in the Item table of
      the specified category
      """
      c = db.execute( "SELECT * FROM items WHERE category=?", (category,))
      y = []
      for rows in c.fetchall():
        y.append( Item( rows[1], rows[2], rows[3], rows[0] ))
      return y

    @staticmethod
    def get_by_manufacturer( db, man ):
      """
      returns all the rows in the Item table of
      the specified manufacturer
      """
      c = db.execute( "SELECT * FROM items WHERE manufacturer=?", (man,))
      y = []
      for rows in c.fetchall():
        y.append( Item( rows[1], rows[2], rows[3], rows[0] ))
      return y

    @staticmethod
    def get_all( db ):
      """
      returns all the rows in the Item table as 
      a list of Item objects
      """
      c = db.execute( "SELECT * FROM items WHERE id>0" )
      y = []
      for rows in c.fetchall():
        y.append( Item( rows[1], rows[2], rows[3], rows[0] ))
      return y

    @staticmethod
    def set( db, item ):
      """
      updates the row in the Item table specified
      by the Item object
      the Item object must have a valid id
      """
      if item.id == 0:
        raise Exception( 'Item: DBHelper: set: invalid id' )
      args = (item.category,item.manufacturer,item.model,item.id)
      c = db.execute( "UPDATE items SET category=?, manufacturer=?, model=? WHERE id=?", args )
      db.commit()
      return c.rowcount

if __name__ == "__main__":
  print "========================="
  print "Item database test:"
  print "========================="
  import sqlite3
  db = sqlite3.connect('inv.db')
  print "Test 1: creating table"
  Item.DBHelper.create_table(db)
  print "Test 1: success"
  print "========================="
  print "Test 2: Create"
  l1 = Item( 'Monitor', 'Dell', 'E172FPb' )
  l2 = Item( 'Monitor', 'Samsung', 'SyncMaster 930B' )
  l3 = Item( 'Computer', 'Dell', 'Optiplex 9010' )
  print "adding " + str(l1)
  Item.DBHelper.add( db, l1 )
  print "adding " + str(l2)
  Item.DBHelper.add( db, l2 )
  print "adding " + str(l3)
  Item.DBHelper.add( db, l3 )
  print "Test 2: success"
  print "========================="
  print "Test 3: Read"
  print "get by category (Monitor)..."
  items = Item.DBHelper.get_by_category( db, 'Monitor' )
  for i in items:
    print str(i.id) + '. ' + str(i)
  print "get by manufacturer (Dell)..."
  items = Item.DBHelper.get_by_manufacturer( db, 'Dell' )
  for i in items:
    print str(i.id) + '. ' + str(i)
  print "get all..."
  items = Item.DBHelper.get_all( db )
  for i in items:
    print str(i.id) + '. ' + str(i)
  print "Test 3: success"
  print "========================="
  print "Test 4: Update"
  for i in items:
    print "updating " + str(i)
    i.category = "Other"
    print "to " + str(i)
    Item.DBHelper.set(db,i)
  print "Test 4: success"
  print "========================="
  print "Test 5: Delete"
  for i in items:
    print "deleting " + str(i)
    Item.DBHelper.delete( db, i.id )
  print "Test 5: success"
  print "========================="
  print "Item database test succeeded"
  print "========================="
