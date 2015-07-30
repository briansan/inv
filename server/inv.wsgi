import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/inv')
from inv import app as application

