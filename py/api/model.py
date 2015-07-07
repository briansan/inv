from api import db
from datetime import datetime

class User(db.Model):
  class UserGroup():
    NoGroup = 0
    Student = 1
    Faculty = 2
    Operator = 3
    Admin = 4

  id = db.Column(db.Integer, primary_key=True)
  uname = db.Column(db.String(32), unique=True)
  passwd = db.Column(db.String(32))
  fname = db.Column(db.String(32))
  lname = db.Column(db.String(32))
  grp = db.Column(db.Integer)
  perm = db.Column(db.Integer)
  start = db.Column(db.DateTime)

  def __init__(self,uname,fname="",lname="",grp=0,perm=0,start=datetime.now()):
    self.uname = uname
    self.fname = fname
    self.lname = lname
    self.grp = grp
    self.perm = perm
    self.start = start

  def __repr__(self):
    return '<User %r>' % self.uname

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category_id = db.Column(db.Integer, db.ForeignKey('item_category.id'))
  manufacturer_id = db.Column(db.Integer, db.ForeignKey('item_manufacturer.id'))
  model = db.Column(db.String(32), unique=True)

  category = db.relationship('ItemCategory', backref=db.backref('items', lazy='dynamic'))
  manufacturer = db.relationship('ItemManufacturer', backref=db.backref('items', lazy='dynamic'))

  def __init__( self, cat, man, mod ):
    self.category = cat
    self.manufacturer = man
    self.model = mod

  def __repr__(self):
    return '<Item %s>' % self

  def __str__(self):
    return '%s %s (%s)' % self.manufacturer, self.model, self.category

class Location(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  building_id = db.Column(db.Integer, db.ForeignKey('location_building.id'))
  room = db.Column(db.String)

  building = db.relationship('LocationBuilding', backref=db.backref('locations', lazy='dynamic'))

  def __init__(self, building, room):
    self.building = building
    self.room = room
  def __repr__(self):
    return '<Location %s>' % self
  def __str__(self):
    return '%s %s' % self.building, self.room

class Asset(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('asset_info.id'), unique=True)
  status = db.Column(db.Integer)
  item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
  purchased = db.Column(db.DateTime)
  img = db.Column(db.String(64))
  owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  price = db.Column(db.Float)
  receipt = db.Column(db.String(64))
  ip = db.Column(db.String(32))
  comments = db.Column(db.String(128))
  home_id = db.Column(db.Integer, db.ForeignKey('location.id'))
  current_id = db.Column(db.Integer, db.ForeignKey('location.id'))

  tag = db.relationship('AssetInfo', backref=db.backref('asset', lazy='dynamic'))
  item = db.relationship('Item', backref=db.backref('assets', lazy='dynamic'))
  current = db.relationship('Location', backref=db.backref('cassets', lazy='dynamic'), foreign_keys=[current_id])
  home = db.relationship('Location', backref=db.backref('hassets', lazy='dynamic'), foreign_keys=[home_id])
  owner = db.relationship('User', backref=db.backref('assets', lazy='dynamic'))

  def __init__( self, tag, status, item, purchased=datetime.now(), img="", owner=None, home=None, current=None, comments="", price=0.0, receipt="", ip=""):
     self.tag = tag
     self.status = status
     self.item = item
     self.purchased = purchased
     self.img = img
     self.owner = owner
     self.price = price
     self.receipt = receipt
     self.ip = ip
     self.comments = comments
     self.home = home
     self.current = current

class Inventory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  who_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  what_id = db.Column(db.Integer, db.ForeignKey('asset.id'))
  when = db.Column(db.DateTime)
  where_id = db.Column(db.Integer, db.ForeignKey('location.id'))

  who = db.relationship('User', backref=db.backref('invs', lazy='dynamic'))
  what = db.relationship('Asset', backref=db.backref('invs', lazy='dynamic'))
  where = db.relationship('Location', backref=db.backref('invs', lazy='dynamic'))
  def __init__(self,who,what,where,when=datetime.now()):
    self.who = who
    self.what = what
    self.when = when
    self.where = where

class ItemCategory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name

class ItemManufacturer(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name

class LocationBuilding(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(32), unique=True)
  def __init__(self,name):
    self.name = name
  def __str__(self):
    return self.name

class AssetInfo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ece = db.Column(db.String(8), unique=True)
  vu = db.Column(db.String(8), unique=True)
  unit = db.Column(db.String(8), unique=True)
  svc = db.Column(db.String(8), unique=True)
  serial = db.Column(db.String(8), unique=True)

  def __init__(self,ece,vu='',unit='',svc='',serial=''):
    self.ece = ece
    self.vu = vu
    self.unit = unit
    self.svc = svc
    self.serial = serial

  def __repr__(self):
    return '<AssetInfo %r>' % self.ece

