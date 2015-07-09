from model import *

def user_exists(uname):
  return len(User.query.filter_by(uname=uname).all())==1

def login(uname):
  # ZZ: alot more involved in authenticating here...
  return user_exists(uname)

def register(uname):
  # ZZ: should do alot more checking here
  if not user_exists(uname):
    u = User(uname)
    db.session.add(u)
    db.session.commit()
    return u.id
  else:
    return False
