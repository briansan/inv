from flask import Flask
from flask.ext.testing import TestCase
import unittest

from model import db
from api import create_app

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
    inv = Inventory(u1,asset,location)

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

  def test_user(self):
    from model import User
    user = User.query.filter_by(uname='bob').first()
    assert user in db.session
    self.assertEquals(str(user),'bob')

  def test_item(self):
    from model import Item
    item = Item.query.filter(Item.manufacturer.has(name='Dell')).first()
    assert item in db.session
    assert item.manufacturer in db.session
    assert item.category in db.session
    self.assertEquals(str(item),'Dell Optiplex 360 (Computer)')

  def test_location(self):
    from model import Location
    loc = Location.query.filter_by(room='008').first()
    assert loc in db.session
    self.assertEquals(str(loc),'CEER 008')

  def test_asset(self):
    from model import AssetInfo, Asset
    asset = Asset.query.filter(Asset.tag.has(ece='ee02547')).first()
    assert asset in db.session
    self.assertEquals(str(asset),'ee02547: Dell Optiplex 360 (Computer)')

  def test_inv(self):
    from model import Inventory
    inv = Inventory.query.filter(Inventory.who.has(uname='bob')).first()
    assert inv in db.session
    self.assertIn('bob for ee02547: Dell Optiplex 360 (Computer)',str(inv))
  
if __name__ == '__main__':
  unittest.main()
