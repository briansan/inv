from flask import Flask, session, request, Blueprint
import model, view, methods, controller
from crossdomain import crossdomain

api = Blueprint('admin',__name__)
origin='http://vecr.ece.villanova.edu'

@api.route('/')
@crossdomain(origin=origin)
def root():
  return controller.root()

@api.route('/login',methods=['GET','POST'])
@crossdomain(origin=origin)
def login():
  return controller.login()
      
@api.route('/logout',methods=['GET','POST'])
@crossdomain(origin=origin)
def logout():
  return controller.logout()

@api.route('/add/<entity>', methods=['POST'])
@crossdomain(origin=origin)
def add(entity):
  return controller.add(entity)

@api.route('/view/<entity>')
@crossdomain(origin=origin)
def vw(entity):
  return controller.vw(entity)

@api.route('/edit/<entity>/<id>', methods=['POST'])
@crossdomain(origin=origin)
def edit(entity):
  return controller.edit(entity)

@api.route('/rm/<entity>/<id>', methods=['DELETE'])
@crossdomain(origin=origin)
def rm(entity):
  return controller.rm(entity)

def create_app(fname):
  # initialize and configure the app
  app = Flask(__name__)
  app.config.from_pyfile(fname)
  # connect the model to the app
  model.db.init_app(app)
  with app.app_context():
    model.db.create_all()
  # register blueprints
  app.register_blueprint(api)
  return app

if __name__=="__main__":
  create_app('conf/debug.cfg').run(host='0.0.0.0')
