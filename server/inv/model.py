"""
  @file   inv/model.py
  @author Brian Kim
  @brief  this module defines the entities used by inv
"""
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

db = SQLAlchemy()

class User(db.Model):
  class Groups():
    NoGroup = 0
    Student = 1
    Faculty = 2
    Operator = 3
    Admin = 4
    info = {0:'No Group', 
            1:'Student', 
            2:'Faculty',
            3:'Operator',
            4:'Admin'}

  uid = db.Column(db.String(16), unique=True, primary_key=True)
  passwd = db.Column(db.String(32))
  fname = db.Column(db.String(32))
  lname = db.Column(db.String(32))
  grp = db.Column(db.Integer)
  perm = db.Column(db.Integer)
  start = db.Column(db.DateTime)
  annon = db.Column(db.Boolean)
  email = db.Column(db.String(32))
  phone = db.Column(db.String(16))

  def __init__(self,uid, fname="", lname="",
                    grp=0, perm=0,
                    email="",phone="", 
                    annon=False,start=datetime.now()):
    self.uid = uid
    self.fname = fname
    self.lname = lname
    self.grp = grp
    self.perm = perm
    self.start = start
    self.annon = annon
    self.phone = phone
    self.email = email

  def __repr__(self):
    return '<User %r>' % self

  def __str__(self):
    return self.uid

  def __iter__(self):
    yield ('uid',self.uid)
    yield ('fname',self.fname)
    yield ('lname',self.lname)
    yield ('grp',self.grp)
    yield ('perm',self.perm)
    yield ('annon',self.annon)
    yield ('email',self.email)
    yield ('phone',self.phone)
    yield ('start',int(self.start.strftime("%s")))
  
  def generate_auth_token(self, expiration=None):
    if expiration is None: expiration = 3600
    from flask import current_app
    app = current_app
    s = Serializer(app.config['SECRET_KEY'], expires_in=int(expiration))
    y = s.dumps({'uid':self.uid})
    return y

  @staticmethod
  def verify_auth_token(token):
    from flask import current_app
    app = current_app
    s = Serializer(app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
    except SignatureExpired:
      return None # valid token, but expired
    except BadSignature:
      return None # invalid token
    user = User.query.get(data['uid'])
    return user

  @staticmethod
  def info():
    return {
      'uid':'user id',
      'fname':'first name',
      'lname':'last name',
      'grp':'user group (1:student,2:faculty,3:operator,4:admin)',
      'perm':'permissions',
      'start':'start date'
    }

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category_id = db.Column(db.Integer, db.ForeignKey('item_category.id'))
  manufacturer_id = db.Column(db.Integer, db.ForeignKey('item_manufacturer.id'))
  model = db.Column(db.String(32))

  category = db.relationship('ItemCategory', backref=db.backref('items', lazy='dynamic'))
  manufacturer = db.relationship('ItemManufacturer', backref=db.backref('items', lazy='dynamic'))

  def __init__( self, cat, man, mod ):
    self.category = cat
    self.manufacturer = man
    self.model = mod

  def __repr__(self):
    return '<Item %s>' % self

  def __str__(self):
    return '%s %s (%s)' % (self.manufacturer, self.model, self.category)

  def __iter__(self):
    yield ('id',self.id)
    yield ('category', self.category.name)
    yield ('manufacturer', self.manufacturer.name)
    yield ('model', self.model)

  @staticmethod
  def info():
    return {
      'id': 'item id',
      'category': 'category name',
      'manufacturer': 'manufacturer name',
      'model': 'model number (str)',
    }

class Location(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  building_id = db.Column(db.Integer, db.ForeignKey('location_building.id'))
  room = db.Column(db.String(8))

  building = db.relationship('LocationBuilding', backref=db.backref('locations', lazy='dynamic'))

  def __init__(self, building, room):
    self.building = building
    self.room = room
  def __repr__(self):
    return '<Location %s>' % self
  def __str__(self):
    return '%s %s' % (self.building, self.room)
  def __iter__(self):
    yield ('id',self.id)
    yield ('building', self.building.name)
    yield ('room', self.room)
  @staticmethod
  def info():
    return {
      'id': 'location id',
      'building': 'building name',
      'room': 'room number (str)'

    }

class Asset(db.Model):
  class Status():
    NoStatus = 0
    Available = 1
    Deployed = 2
    Loaned = 3 
    Disposed = 4
    info = {0:'Not Available', 
            1:'Available', 
            2:'Deployed',
            3:'Loaned',
            4:'Disposed'}

  tag_ece = db.Column(db.String(16), unique=True, primary_key=True)
  tag_vu = db.Column(db.String(16), unique=True)
  tag_unit = db.Column(db.String(16))
  tag_svc = db.Column(db.String(16))
  serial = db.Column(db.String(16))
  status = db.Column(db.Integer)
  item_id = db.Column(db.Integer, db.ForeignKey('item.id'))

  price = db.Column(db.Float)
  ip = db.Column(db.String(32))
  comments = db.Column(db.String(128))

  purchased = db.Column(db.DateTime)
  inventoried = db.Column(db.DateTime)
  owner_id = db.Column(db.String(16), db.ForeignKey('user.uid'))
  holder_id = db.Column(db.String(16), db.ForeignKey('user.uid'))
  home_id = db.Column(db.Integer, db.ForeignKey('location.id'))
  current_id = db.Column(db.Integer, db.ForeignKey('location.id'))

  item = db.relationship('Item', backref=db.backref('assets', lazy='dynamic'))
  current = db.relationship('Location', backref=db.backref('cassets', lazy='dynamic'), foreign_keys=[current_id])
  home = db.relationship('Location', backref=db.backref('hassets', lazy='dynamic'), foreign_keys=[home_id])
  owner = db.relationship('User', backref=db.backref('oassets', lazy='dynamic'), foreign_keys=[owner_id])
  holder = db.relationship('User', backref=db.backref('hassets', lazy='dynamic'), foreign_keys=[holder_id])

  def __init__( self, tag_ece, status, item, comments="", price=0.0, ip="", 
                      purchased=datetime.now(), owner=None, home=None, 
                      tag_vu="",tag_unit="",tag_svc="",serial="", 
                      inventoried=None, holder=None, current=None ):
    self.tag_ece = tag_ece
    self.tag_vu = tag_vu
    self.tag_unit = tag_unit
    self.tag_svc = tag_svc
    self.serial = serial
    self.status = status
    self.item = item
    self.price = price
    self.ip = ip
    self.comments = comments
    # creation data
    self.purchased = purchased
    self.owner = owner
    self.home = home
    # current data
    self.inventoried = inventoried
    self.holder = holder
    self.current = current

  def __repr__( self ):
    return '<Asset %s>' % self

  def __str__( self ):
    return '%s: %s' % (self.tag_ece, self.item)

  def __iter__( self ):
    yield ('tag_ece', self.tag_ece)
    yield ('tag_vu', self.tag_vu)
    yield ('tag_unit', self.tag_unit)
    yield ('tag_svc', self.tag_svc)
    yield ('serial', self.serial)
    yield ('status', self.status)
    yield ('item', self.item.id if self.item else None)
    yield ('price', self.price)
    yield ('ip', self.ip)
    yield ('comments', self.comments)

    yield ('purchased', int(self.purchased.strftime("%s")) if self.purchased else None)
    yield ('owner', self.owner.uid if self.owner else None)
    yield ('home', self.home.id if self.home else None)

    yield ('inventoried', int(self.inventoried.strftime("%s")) if self.inventoried else None)
    yield ('holder', self.holder.uid if self.holder else None)
    yield ('current', self.current.id if self.current else None)

  @staticmethod
  def info():
    return {
      'tag_ece': 'ece asset tag',
      'status': '1:available, 2:deployed, 3:loaned, 4:disposed',
      'item': 'the item that represents the asset',
      'price': 'value of asset ($)',
      'ip': 'ip address',
      'comments': 'any additional comments',

      'purchased': 'date of purchase',
      'owner': 'owner of the asset',
      'home': 'home location of asset',

      'inventoried': 'last date and time of inventory',
      'holder': 'current holder of the asset',
      'current': 'current location of asset'
    }

class Inventory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  who_id = db.Column(db.String(16), db.ForeignKey('user.uid'))
  what_id = db.Column(db.String(16), db.ForeignKey('asset.tag_ece'))
  when = db.Column(db.DateTime)
  where_id = db.Column(db.Integer, db.ForeignKey('location.id'))
  how = db.Column(db.Integer)

  who = db.relationship('User', backref=db.backref('invs', lazy='dynamic'))
  what = db.relationship('Asset', backref=db.backref('invs', lazy='dynamic'))
  where = db.relationship('Location', backref=db.backref('invs', lazy='dynamic'))

  def __init__(self,who,what,when=datetime.now(),where=None,how=Asset.Status.Available):
    self.who = who
    self.what = what
    self.when = when
    self.where = where
    self.how = status

  def __repr__( self ):
    return '<Inventory %s>' % self

  def __str__( self ):
    return '%s for %s on %s in %s as %s' % (self.who, self.what, self.when, self.where, Asset.Status.info[self.how])

  def __iter__( self ):
    yield ('id',self.id)
    yield ('who',self.who.uid)
    yield ('what',self.what.tag_ece)
    yield ('when',int(self.when.strftime("%s")))
    yield ('where',self.where.id)
    yield ('how',self.status)

  @staticmethod
  def info():
    return {
      'id': 'inventory id',
      'who': 'the user',
      'what': 'the asset',
      'when': 'the date',
      'where': 'the location',
      'how': 'the status'
    }

class ItemCategory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    return '<ItemCategory %s>' % self
  def __str__(self):
    return self.name
  def __iter__(self):
    yield ('id',self.id)
    yield ('name',self.name)
  @staticmethod
  def info():
    return {
      'id':'category id',
      'name':'category name'
    }

class ItemManufacturer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    return '<ItemManufacturer %s>' % self
  def __str__(self):
    return self.name
  def __iter__(self):
    yield ('id',self.id)
    yield ('name',self.name)
  @staticmethod
  def info():
    return {
      'id':'manufacturer id',
      'name':'manufacturer name'
    }

class LocationBuilding(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  def __init__(self,name):
    self.name = name
  def __repr__(self):
    return '<LocationBuilding %s>' % self
  def __str__(self):
    return self.name
  def __iter__(self):
    yield ('id',self.id)
    yield ('name',self.name)
  @staticmethod
  def info():
    return {
      'id':'building id',
      'name':'building name'
    }

