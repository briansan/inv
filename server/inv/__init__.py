"""
 @file   inv/__init__.py
 @author Brian Kim
 @brief  the app initialization script for inv
"""

from flask import Flask
from flask_sslify import SSLify
from api import api
from site import site
from model import db

def create_app(conf):
  # init
  app = Flask(__name__)
  app.config.from_pyfile(conf)
  # connect model to app
  db.init_app(app)
  with app.app_context():
    db.create_all()
  # secure it
  SSLify(app)
  # register blueprints
  app.register_blueprint(api,url_prefix='/api/v1')
  app.register_blueprint(site,url_prefix='')
  return app

if __name__=="__main__":
  create_app('conf/debug.cfg').run(host='0.0.0.0')
