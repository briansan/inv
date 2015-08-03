import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/inv')
from inv import create_app 
application = create_app('conf/deploy.cfg')

