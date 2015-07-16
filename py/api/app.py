from flask import Flask, session, request, Blueprint
import model, view, methods, controller
from crossdomain import crossdomain

api = Blueprint('admin',__name__)
origin='http://bread.ece.villanova.edu'

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
def vw_all(entity):
  return vw(entity,0)

@api.route('/view/<entity>/<id>')
@crossdomain(origin=origin)
def vw(entity,id):
  return controller.vw(entity,id)

@api.route('/view/user')
@crossdomain(origin=origin)
def vw_self():
  return controller.view_user()

@api.route('/view/user/<id>')
@crossdomain(origin=origin)
def vw_user(id):
  return controller.view_user_all(id)

@api.route('/view/user/group')
@crossdomain(origin=origin)
def vw_user_groups():
  return view.success(model.User.Groups.info)

@api.route('/view/asset/status')
@crossdomain(origin=origin)
def vw_asset_statuses():
  return view.success(model.Asset.Status.info)

@api.route('/edit/<entity>/<id>', methods=['POST'])
@crossdomain(origin=origin)
def edit(entity,id):
  return controller.edit(entity,id)

@api.route('/rm/<entity>/<id>')
@crossdomain(origin=origin)
def rm(entity,id):
  return controller.rm(entity,id)

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
