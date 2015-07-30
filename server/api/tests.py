from flask import Flask
from flask.ext.testing import TestCase
import unittest

from model import db
from app import create_app

class InvTest(TestCase):
  
  def create_app(self):
    return create_app('conf/test.cfg')

  def setUp(self):
    # init tables
    db.create_all()
    # do imports
    from model import User
    from model import ItemCategory, ItemManufacturer, Item
    from model import LocationBuilding, Location
    from model import AssetInfo, Asset
    from model import Inventory
    # create objects
    u1 = User('bob')
    cat = ItemCategory('Computer')
    man = ItemManufacturer('Dell')
    item = Item(cat,man,'Optiplex 360')
    building = LocationBuilding('CEER')
    location = Location(building,'008')
    tag = AssetInfo('ee02547','13349')
    asset = Asset(tag,0,item,owner=u1,current=location,ip='153.104.47.23')
    import datetime
    inv = Inventory(u1,asset,datetime.datetime.now(),location)

    # add to database
    db.session.add(u1)
    db.session.add(cat)
    db.session.add(man)
    db.session.add(building)
    db.session.add(tag)
    db.session.add(item)
    db.session.add(location)
    db.session.add(asset)
    db.session.add(inv)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def get_user(self):
    from model import User
    return User.query.filter_by(uname='bob').first()

  def get_item(self):
    from model import Item
    return Item.query.filter(Item.manufacturer.has(name='Dell'),Item.category.has(name='Computer')).first()

  def get_location(self):
    from model import Location
    return Location.query.filter_by(room='008').first()

  def get_asset(self):
    from model import AssetInfo, Asset
    return Asset.query.filter(Asset.tag.has(ece='ee02547'),Asset.ip.is_('153.104.47.23')).first()
    
  def get_inv(self):
    from model import Inventory
    return Inventory.query.filter(Inventory.who.has(uname='bob')).first()

  def get_user_api(self):
    return self.client.get('/view/user')

  def get_login(self):
    from getpass import getpass
    uname = raw_input('Username: ')
    passwd = getpass('Password: ')
    import base64
    auth = base64.encodestring(uname+':'+passwd)
    return self.client.get('/api/v1/', headers={'Authorization':'Basic %s' % auth}, follow_redirects=True)

  def test_api(self):
    r = self.get_login()
    assert 'token' in r.json['msg']

  def test_user(self):
    user = self.get_user()
    assert str(user) == 'bob'

  def test_item(self):
    item = self.get_item()
    assert item.manufacturer in db.session
    assert item.category in db.session
    assert str(item) == 'Dell Optiplex 360 (Computer)'

  def test_location(self):
    loc = self.get_location()
    assert loc.building in db.session
    assert str(loc) == 'CEER 008'

  def test_asset(self):
    asset = self.get_asset()
    assert asset in db.session
    assert str(asset) == 'ee02547: Dell Optiplex 360 (Computer)'

  def test_inv(self):
    inv = self.get_inv()
    assert 'bob for ee02547: Dell Optiplex 360 (Computer)' in str(inv)
  
if __name__ == '__main__':
  unittest.main()
