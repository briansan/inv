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

class Loan():
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
    ofni = {
      "Requested" : Requested,
      "Approved" : Approved,
      "Loaned" : Loaned,
      "Returned" : Returned,
    }

  def __init__( self, items=[], status=Status.Requested, who=Person(),
                      create=datetime.datetime.now(),
                      start=datetime.datetime.now(), 
                      due=datetime.datetime.now(), 
                      returnDate=datetime.datetime.now(), id=0 ):
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
    y = 'Loan #' + str(self.id) + 'to '+self.who+': \n' 
    y += '\tfor:\n'
    for x in self.items:
      y += str(x)+'\n'
    y += '\trequested: '+str(self.create)+'\n'
    if self.status > Loan.Status.Requested:
      y += '\tapproved: '+str(self.start)+'\n'
    if self.status > Loan.Status.Approved:
      y += '\tdue: '+str(self.due)+'\n'
    if self.status > Loan.Status.Returned:
      y += '\treturned: '+str(self.returnDate)+'\n'
    return y

  @staticmethod
  def init_from_db_row( db, row ):
    id     = row[0]
    items  = Loan.DBHelper.get_all_assets_from_loan( db, row[1] )
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
         status INTEGER NOT NULL,
         who INTEGER NOT NULL,
         create INTEGER NOT NULL,
         start INTEGER NOT NULL,
         due INTEGER NOT NULL,
         rdate INTEGER NOT NULL
        ); ''')
      db.execute('''CREATE TABLE IF NOT EXISTS loan_assets
        (loan_id INTEGER NOT NULL,
         asset_id INTEGER NOT NULL
        );''')
      db.execute("INSERT OR IGNORE INTO loans (id,status,who,create,start,due,rdate) values (0,0,0,0,0,0,0);")
      db.commit()

    @staticmethod
    def get_all_assets_from_loan( db, loan_id ):
      c = db.execute( "SELECT * FROM loan_assets WHERE loan_id=?", (loan_id) )
      y = []
      for rows in c.fetchall():
        y.append( Asset.DBHelper.get( db, rows[1] ) )
      return y
    
    @staticmethod
    def add( db, loan ):
      args = (loan.status,loan.who.id,loan.create,loan.start,loan.due,loan.returnDate)
      c = db.execute( "INSERT INTO loan (status,who,create,start,due,rdate) values (?,?,?,?,?,?);", args )
      for asset in loan.items:
        db.execute( "INSERT INTO loan_assets(loan_id,asset_id) values (?,?);", (c.lastrowid, asset.id ))
      db.commit()
      return c.lastrowid

    @staticmethod
    def delete( db, asset ):
      db.execute( "DELETE FROM loans WHERE id=?", (asset.id,) )
      db.commit()

    @staticmethod
    def get( db, id ):
      c = db.execute( "SELECT * FROM loans WHERE id=?", (id,) )
      # fetch a row (should only be one)
      rows = c.fetchone()
      if not rows == None:
        return Loan.init_from_db_row( db, rows )
      else:
        return None

    @staticmethod
    def get_by_status( db, status ):
      q = "SELECT * FROM loans WHERE status=?"
      c = db.execute( q, (status,) )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_who( db, who ):
      c = db.execute( "SELECT * FROM loans WHERE who=?", (who.id,) )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_create( db, date ):
      c = db.execute( "SELECT * FROM loans WHERE create=?", (date,) )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_start( db, date ):
      c = db.execute( "SELECT * FROM loans WHERE start=?", (date,) )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_due( db, date ):
      c = db.execute( "SELECT * FROM loans WHERE due=?", (date,) )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_by_return( db, date ):
      c = db.execute( "SELECT * FROM loans WHERE rdate=?", (date,) )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows) )
      return y

    @staticmethod
    def get_all( db ):
      c = db.execute( "SELECT * FROM loans WHERE id>0" )
      y = []
      for rows in c.fetchall():
        y.append( Loan.init_from_db_row(db,rows))
      return y

    @staticmethod
    def set_approved( db, loan, start=datetime.datetime.now() ):
      if loan.id == 0:
        raise Exception( 'Loan: DBHelper: set: invalid id' )
      # do a little validation
      start = int(start.strftime("%s"))
      c = db.execute( "UPDATE loans SET status=?, start=? WHERE id=?", (Loan.Status.Approved,start,loan.id)) 
      db.commit()
      return c.rowcount

    @staticmethod
    def set_loaned( db, loan, due=datetime.datetime.now()+datetime.timedelta(7) ):
      if loan.id == 0:
        raise Exception( 'Loan: DBHelper: set: invalid id' )
      due = int(due.strftime("%s"))
      # do a little validation
      c = db.execute( "UPDATE loans SET status=?, due=? WHERE id=?", (Loan.Status.Loaned, due, loan.id)) 
      db.commit()
      return c.rowcount

    @staticmethod
    def set_returned( db, loan, returned=datetime.datetime.now() ):
      if loan.id == 0:
        raise Exception( 'Loan: DBHelper: set: invalid id' )
      returned = int(returned.strftime("%s"))
      # do a little validation
      c = db.execute( "UPDATE loans SET status=?,rdate=? WHERE id=?", (Loan.Status.Returned,returned,loan.id)) 
      db.commit()
      return c.rowcount

