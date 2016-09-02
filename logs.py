###########################################################################
#
#   File Name    Date       Owner                Description
#   ---------   -------    ---------           -----------------------
#   logs.py    4/8/2015  Archana Bahuguna   Logging module for fearapp
#
###########################################################################

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)

def info_(prntstr):
    logging.info(prntstr)

def debug_(prntstr):
    logging.debug(prntstr)
