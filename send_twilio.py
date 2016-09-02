###########################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   send_twilio.py  4/4/2015   Archana Bahuguna  Msg to Twilio
#
#   A cron job is setup to run this module- an sms scheduler which
#   monitors the database for any updated events and sends a notification
#   to the user to prompt for updating the event info.
#
###########################################################################

from twilio.rest import TwilioRestClient 
import models
from models import *
from sqlalchemy.sql import and_, or_
import datetime


ACCOUNT_SID = "AC85250cc80055bfd5dfe95eb9072eaa65"

AUTH_TOKEN = "8de0e1f992ca4f46499ec975a6d8c142"

#Twilio client is invoked to create an HTTP message
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

def twilio_sms_scheduler():
        

        """The sms scheduler sends a trigger msg to Twilio to send reminder 
        SMSes to users whose events have expired requesting them to fill in 
        the actual experience of the event.

        The scheduler polls the db for events that have status CREATED and have
        have occured in the past (event.datetime <= datetime.now()). It then 
        finds the userids corresponding to those events and sends Twilio the 
        msg request.

        The scheduler is run (cronjob) every 30 mins(currently) to select all 
        events.  When a process is scheduled by the crontab, a previous 
        identical process might already be running (forked 30 mins back by 
        crontab) and result in a race condition on a row read causing multiple
        (duplicate) smses being sent to the same user id. 

        To avoid this, a combination of SQL queries- UPDATE (a unique batch id/
        per cron process) and SELECT is used (events are now selected for only 
        that unique batch id). Since batch id is unique per process the 
        duplication or race condition can be eliminated. 

        If a Twilio request returns with a valid Sid (smsid returned by Twilio) 
        the Sid is saved in a log file for future and the event status is 
        updated to TWILIO_SMS_SENT.
        """

        import random
        #Write a method for gen unique random no by adding jobname/datetime etc
        from random import randrange
        batchid = randrange(0,10000)
        
        marked_for_sms_events = models.Event.query.filter(and_(
                                                   models.Event.status==FEARAPP_STATUS_CREATED,
                                                   models.Event.datetime<=datetime.datetime.now(), models.Event.batchid==0)).update(dict(batchid=batchid))
        models.db.session.commit()
        #Need to figure out rollback in case batch fails
        #SQLAlchemy will do a transaction commit and rollback by itself?
        
        sms_events = models.Event.query.join(models.User).filter(and_(
                             models.Event.batchid==batchid, models.Event.userid==models.User.userid)).all()
        for event in sms_events:
            if event.user.phone: #if user has a phone
            
            #This ends up sending an HTTP POST message to 
            #/2014-04-01/Accounts/{AccountsSid}/Messages
            #The app has registered at twilio.com for the FROM no.(Server reg)
            #Should have event id so user can log in and update the 
                  #particular event info
            
                message = client.messages.create(
                      to=event.user.phone, from_="+19193733763", 
                      body="This is a reminder to update the event desc here- http://www.thefearapp.com/twilio/encrypted_eventid", 
                      statuscallback="http://thefearapp.com/twiliosmsresponses")
                  
            #loghandler- log event.eventid event.userid message.sid
            #Later you would need to dig the Sid from logs to link it to eventid??

            #If valid Sid is received for the SMS from Twilio, update event 
            #status

                if (message.sid is not None):
                    models.Event.query.filter_by(eventid=event.eventid).update(dict(status=FEARAPP_STATUS_SENT_SMS))
                    models.db.session.commit()
                
        return None

if __name__ == '__main__':
    twilio_sms_scheduler()
