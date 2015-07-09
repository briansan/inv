from flask import Flask, session, request, Blueprint
import model, view, methods, controller
from crossdomain import crossdomain

api = Blueprint('admin',__name__)

@api.route('/')
@crossdomain(origin='http://vecr.ece.villanova.edu')
def root():
  if 'uname' in session:
    return view.all_methods()
  else:
    return view.request_login()

def logged_in():
  return session.get('uname')
  
@api.route('/login',methods=['GET','POST'])
@crossdomain(origin='http://vecr.ece.villanova.edu')
def login():
  if not logged_in():     # make sure not already logged in
    if request.method=='POST': # check method type
      uname = request.form['uname'] # get username
      passwd = request.form['passwd'] # get username
      y = controller.login(uname,passwd)
      if not (type(y) is str): # authenticate the user
        session['uname'] = dict(y) # success => welcome
        return view.welcome(y.fname +' '+y.lname)
      else: # failure => go away
        return view.failure(y)
    else: # GET => display login menu
      return view.login()
  else:
    return view.failure('you\'re already logged in...')
      
@api.route('/logout',methods=['GET','POST'])
@crossdomain(origin='http://vecr.ece.villanova.edu')
def logout():
  if logged_in():
    session.pop('uname',None)
    return view.success('bye bye!')
  else:
    return view.failure('you didn\'t login...')

@api.route('/users')
@crossdomain(origin='http://vecr.ece.villanova.edu')
def users():
  pass
  return ':)'

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
