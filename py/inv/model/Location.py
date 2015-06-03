"""
  @file   Location.py
  @author Brian Kim
  @brief  definition of the Location class and 
          the methods necessary to persist 
          it into a database
"""

class Location():
  def __init__( self, building, room, id=-1 ):
    self.building = building
    self.room = room
    self.id = id

  def __str__( self ):
    return self.building +' '+self.room
  
  class DBHelper():
    @staticmethod
    def create_table( db ):
      db.execute('''CREATE TABLE IF NOT EXISTS locations 
        (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         building TEXT NOT NULL,
         room TEXT NOT NULL); ''')
      db.commit()
    
    @staticmethod
    def add( db, location ):
      args = (location.building, location.room)
      c = db.execute( "INSERT INTO locations (building,room) values (?,?);", args )
      db.commit()
      return c.lastrowid

    @staticmethod
    def delete( db, id ):
      db.execute( "DELETE FROM locations WHERE id=?", (id,) )
      db.commit()

    @staticmethod
    def get( db, id ):
      c = db.execute( "SELECT * FROM locations WHERE id=?", (id,) )
      # fetch a row (should only be one)
      rows = c.fetchone()
      if not rows == None:
        return Location( rows[1], rows[2], rows[0] )
      else:
        return None

    @staticmethod
    def get_by_building( db, building ):
      c = db.execute( "SELECT * FROM locations WHERE building=?", (building,) )
      y = []
      for rows in c.fetchall():
        y.append( Location( rows[1], rows[2], rows[0] ))
      return y

    @staticmethod
    def get_all( db ):
      c = db.execute( "SELECT * FROM locations" )
      y = []
      for rows in c.fetchall():
        y.append( Location( rows[1], rows[2], rows[0] ))
      return y

    @staticmethod
    def set( db, location ):
      if location.id == -1:
        raise Exception( 'Location: DBHelper: set: invalid id' )
      args = (location.building,location.room,location.id)
      c = db.execute( "UPDATE locations SET building=?, room=? WHERE id=?", args )
      db.commit()
      return c.rowcount

if __name__ == "__main__":
  print "========================="
  print "Location database test:"
  print "========================="
  import sqlite3
  db = sqlite3.connect('inv.db')
  print "Test 1: create table"
  Location.DBHelper.create_table(db)
  print "Test 1: success"
  print "========================="
  print "Test 2: Create"
  l1 = Location( 'CEER', '114' )
  l2 = Location( 'CEER', '206' )
  l3 = Location( 'Mendel', '307' )
  print "adding " + str(l1)
  Location.DBHelper.add( db, l1 )
  print "adding " + str(l2)
  Location.DBHelper.add( db, l2 )
  print "adding " + str(l3)
  Location.DBHelper.add( db, l3 )
  print "Test 2: success"
  print "========================="
  print "Test 3: Read"
  print "get by building (CEER)..."
  locations = Location.DBHelper.get_by_building( db, 'CEER' )
  for l in locations:
    print str(l.id) + '. ' + str(l)
  print "get all..."
  locations = Location.DBHelper.get_all( db )
  for l in locations:
    print str(l.id) + '. ' + str(l)
  print "Test 3: success"
  print "========================="
  print "Test 4: Update"
  for l in locations:
    print "updating " + str(l)
    l.building = 'Tolentine'
    print "to " + str(l)
    Location.DBHelper.set(db,l)
  print "========================="
  print "Test 5: Delete"
  for l in locations:
    print "deleting " + str(l)
    Location.DBHelper.delete( db, l.id )
  print "Test 5: success"
  print "========================="
  print "Location database test succeeded"
  print "========================="
