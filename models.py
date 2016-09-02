###########################################################################
#
#   File Name      Date          Owner               Description
#   ----------   --------      ---------        -----------------
#   models.py    4/4/2015   Archana Bahuguna  Db table design/models 
#                                                for fearapp 
#
#   Schema- models.db - Users, Events
#
###########################################################################

from views import app
import cnfg
from constnts import *

from flask.ext.sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timedelta

"""
class MySQLAlchemy(SQLAlchemy):

    def __init__(self, app=None, use_native_unicode=True, session_options=None,
                 metadata=None, query_class=BaseQuery, model_class=Model):
        super(MySQLAlchemy, self).__init__(app, use_native_unicode, session_options, metadata, query_class, model_class) 

    def apply_pool_defaults(self, app, options):   

        def _setdefault(optionkey, configkey):
            value = app.config[configkey]
            if value is not None:
                options[optionkey] = value     
        
        _setdefault('echo_pool', 'SQLALCHEMY_ECHO_POOL')
        super(MySQLAlchemy, self).apply_pool_defaults(app,options)
        import pdb; pdb.set_trace()
"""

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://fearappuser:abc123@localhost:5432/fearappdb'
#app.config['SQLALCHEMY_ECHO_POOL']=True
db =    SQLAlchemy(app)
       

class User(db.Model):
    """ Defines the columns and keys for User table """
    userid    = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String)
    password  = db.Column(db.String)
    email     = db.Column(db.String)
    phone     = db.Column(db.String(10))
    
    users = db.relationship("Event", backref = "user")

    def __init__ (self, username, password, email, phone):
        self.username = username
        self.password = password
        self.email    = email
        self.phone    = phone

    def __repr__(self):
        return '%i        %s           %s         %s          %s' % (
           self.userid, self.username, self.password, self.email, self.phone)
    
class Event(db.Model):
    """ Defines the columns and keys for Quiz table """
    eventid = db.Column(db.Integer, primary_key=True)
    title    = db.Column(db.String(80), unique = True)

    #Use a datetime type- check sqlalchemy
    datetime= db.Column(db.DateTime) #date time of event
    preeventtxt = db.Column(db.String(500))
    prefearfactor = db.Column(db.Integer)
    posteventtxt = db.Column(db.String(500))
    postfearfactor = db.Column(db.Integer)
    status = db.Column(db.Integer)
    """
      FEARAPP_EVENT_STATUS_CREATED: event created by user, 
      FEARAPP_EVENT_STATUS_TWILIO_SMS_SENT: Event has occured and cron job successfully sends a message to Twilio to send the user a reminder and gets an Sid back
      FEARAPP_EVENT_STATUS_TWILIO_SMS_RECVD: A Twilio response has been recvd specifying user rcvd the SMS
      FEARAPP_EVENT_STATUS_UPDATED: event has been updated by the user
    """

    """This Sid should not be stored in the db, rather in a log file since it
     is temporary"""
    #sid = db.Column(db.Integer) #the id returned by twilio for sms sent to user
    batchid  = db.Column(db.Integer)
    userid  = db.Column(db.Integer, db.ForeignKey('user.userid'))

    def __init__ (self,title, datetime, preeventtxt, posteventtxt, prefearfactor, postfearfactor, status, batchid, userid):
        self.title = title
        self.datetime = datetime
        self.preeventtxt = preeventtxt
        self.posteventtxt = posteventtxt
        self.prefearfactor = prefearfactor
        self.postfearfactor = postfearfactor
        #self.fearcategory=fearcategory
        self.status = status
        self.batchid = batchid
        self.userid = userid

    def __repr__(self):
        return '%i   %s     %s     %s     %i     %s     %i    %i    %i   %i' % ( self.eventid, self.title, self.datetime, self.preeventtxt, self.prefearfactor, self.posteventtxt, self.postfearfactor, self.status, self.batchid, self.userid)
                    

def db_init():
    """ Initial config/population of the database tables """

    #Using drop_all temporarily to prevent integrity error between
    #subsequent runs. If db_init is not called this can be removed.
    #this can also be called at the end of this fn
    
    db.drop_all()
    db.create_all()

    cnfg.populate_db()

    import os
    qry = User.query.all()
    print ("\n\n---------------- ***** User db ***** ------------------")
    print ("Userid  username pwd  Firstname   lastname   Phone     Email")
    print ("-------------------------------------------------------\n\n")
    for i in qry:
        print i

    qry2 = Event.query.all()
    print ("\n\n---------------- ***** Event db ***** -----------------")
    print ("Eventid  Title   Datetime   Pretxt   Posttxt   PreFactor   postfactor  Status    Batchid    userid")
    print ("-----------------------------------------------------------\n")
    for j in qry2:
        print j

    return None

