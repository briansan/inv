from flask import Flask, session, request
import model, view, methods

def create_app(fname):
  # initialize and configure the app
  app = Flask(__name__)
  app.config.from_pyfile(fname)
  # connect the model to the app
  model.db.init_app(app)
  return app

app = create_app('conf/debug.cfg')

@app.route('/')
def root():
  if 'uname' in session:
    return view.all_methods()
  else:
    return view.request_login()

def logged_in():
  return session.get('uname')
  
@app.route('/login',methods=['GET','POST'])
def login():
  if not logged_in():     # make sure not already logged in
    if request.method=='POST': # check method type
      uname = request.form['uname'] # get username
      if methods.login(uname): # authenticate the user
        session['uname'] = uname # success => welcome
        return view.welcome(uname)
      else: # failure => go away
        return view.goaway(uname)
    else: # GET => display login menu
      return view.login()
  else:
    return view.failure('you\'re already logged in...')

# this method wont be necessary once 
# ldap is properly implemented
@app.route('/register',methods=['GET','POST'])
def register():
  if not logged_in():     # make sure not already logged in
    if request.method=='POST':
      uname = request.form['uname']
      if methods.register(uname):
        session['uname'] = uname
        return view.success('welcome %s!'%uname)
      else:
        return view.failure('you already go here %s...'%uname)
    else:
      return view.login()
  else:
    return view.failure('you\'re already logged in...')
      
@app.route('/logout',methods=['GET','POST'])
def logout():
  if logged_in():
    session.pop('uname',None)
    return view.success('bye bye!')
  else:
    return view.failure('you didn\'t login...')

@app.route('/users')
def users():
  pass
  return ':)'

if __name__=="__main__":
  app.run(host='0.0.0.0')