###########################################################################
#
#   File Name      Date          Owner               Description
#   ----------   --------      ---------        -----------------
#   models.py    11/7/2014   Archana Bahuguna  Db table design/models 
#                                                for fearapp 
#
#   Schema- models.db - Users, Events
#
###########################################################################

#Arch ----Remove these lines once you start using the views module
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from sqlalchemy.sql import and_, or_
app = Flask(__name__)
bcrypt = Bcrypt(app)
#Arch ---Remove these lines once you start using the views module

FEARAPP_STATUS_CREATED=0
FEARAPP_STATUS_SENT_SMS=1
FEARAPP_STATUS_RECVD=2
FEARAPP_STATUS_UPDATED=3

flask.ext.sqlalchemy import SQLAlchemy
#Arch ---And uncomment the following line
#from views import app, bcrypt
import os
from datetime import datetime, timedelta

app.config['SQLALCHEMY_DATABASE_URI']='postgresql+psycopg2://fearappuser:abc123@localhost:5432/fearappdb'
db = SQLAlchemy(app)

class User(db.Model):
    """ Defines the columns and keys for User table """
    userid    = db.Column(db.Integer, primary_key=True)
    username  = db.Column(db.String)
    password  = db.Column(db.String)
    firstname  = db.Column(db.String)
    lastname  = db.Column(db.String)
    phone     = db.Column(db.String(10))
    email     = db.Column(db.String)

    users = db.relationship("Event", backref = "user")

    def __init__ (self, username, password, firstname, lastname, phone, email):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.phone    = phone
        self.email    = email

    def __repr__(self):
        return '%i        %s         %s       %s      %s      %s    %s' % (
           self.userid, self.username, self.password, self.firstname, 
           self.lastname, self.phone, self.email)
    
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

    #populate User table
    #user1 = User("abahuguna", bcrypt.generate_password_hash("mypwd"), "Arch",\
    #              "Bahuguna", 9194130, "abahuguna@hotmail.com")
    user1 = User("abahuguna", "mypwd", "Arch",\
                  "Bahuguna", "9194138865", "abahuguna@hotmail.com")
    db.session.add(user1)
    db.session.commit()
    user2 = User("user2", bcrypt.generate_password_hash("pwd2"), "user2",\
                  "Tibby", "9194138961", "user2@hotmail.com")
    db.session.add(user2)
    db.session.commit()

    event1 = Event("Job", datetime.now(), \
                   "May not be able to do a good job", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    db.session.add(event1)
    event2 = Event("Host", datetime.now(), \
                   "Not feeling so confident about the ppt", "Blank",\
                   7, 0, FEARAPP_STATUS_CREATED, 0, user2.userid)
    db.session.add(event2)
    db.session.commit()

    import os
    os.system('clear')
    qry = User.query.all()
    print ("\n\n---------------- ***** User db ***** ------------------")
    print ("Userid  username pwd  Firstname   lastname   Phone     Email")
    print ("-------------------------------------------------------\n\n")
    for i in qry:
        print i

    #import pdb; pdb.set_trace()
    qry2 = Event.query.all()
    print ("\n\n---------------- ***** Event db ***** -----------------")
    print ("Eventid  Title   Datetime   Pretxt   Posttxt   PreFactor   postfactor  Status    Batchid    userid")
    print ("-----------------------------------------------------------\n")
    for j in qry2:
        print j

    return None

if __name__ == '__main__':

    db_init()
