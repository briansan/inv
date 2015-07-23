from app import create_app
if __name__=="__main__":
  create_app('conf/debug.cfg').run(host='0.0.0.0')
