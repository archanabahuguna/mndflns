###########################################################################
#
#   File Name      Date          Owner               Description
#   ----------   --------      ---------        -----------------
#   cnfg.py    4/7/2014   Archana Bahuguna  config file for models.db table 
#
###########################################################################


from views import bcrypt
import models
from constnts import *

def populate_db():
    """ Initial config/population of the database tables """

    user1 = models.User("abahuguna", bcrypt.generate_password_hash("mypwd123"), \
                  "abahuguna76@gmail.com", "9194138865")
    models.db.session.add(user1)
    models.db.session.commit()
    user2 = models.User("user2", bcrypt.generate_password_hash("abcd1234"), \
                  "archmeetup@gmail.com", "9194138961")
    models.db.session.add(user2)
    models.db.session.commit()

    event1 = models.Event("Founder's pitch", models.datetime.now(), \
                   "I am very afraid that I will not do a good job. I am very nervous. I think people will not like me at all. I can never do this. I will never learn how to speak in public. I think it will not go well at all.", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event1)
    event2 = models.Event("Public speaking", models.datetime(2015, 11, 15, 5, 8, 51, 173120), \
                   "I am feeling very afraid of being judged by so many people. I think the event will become a complete failure because of me.", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event2)
    event3 = models.Event("Toastmasters speech", models.datetime(2015, 11, 23, 5, 8, 51, 173120), \
                   "I am very sure that I might go blank or forget some of the lines from my speech. I am also feeling very shy. I wish it were not a formal setting. I should never try this again.", "Blank",\
                   7, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event3)
    event4 = models.Event("Sky diving", models.datetime.now(), \
                   "Afraid of not falling properly and hurting myself ", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event4)
    event5 = models.Event("Speech2", models.datetime.now(), \
                   "May not be able to do a good job", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event5)
    event6 = models.Event("Public speaking2", models.datetime.now(), \
                   "Feeling afraid of being judged", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event6)
    event7 = models.Event("Toastmasters speech2", models.datetime.now(), \
                   "I might go blank or forget lines from my speech", "Blank",\
                   7, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event7)
    event8 = models.Event("Sky diving2", models.datetime.now(), \
                   "Afraid of not falling properly and hurting myself ", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event8)

    event9 = models.Event("Speech3", models.datetime.now(), \
                   "May not be able to do a good job", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event9)
    event10 = models.Event("Public speaking3", models.datetime.now(), \
                   "Feeling afraid of being judged", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event10)
    event11 = models.Event("Toastmasters speech3", models.datetime.now(), \
                   "I might go blank or forget lines from my speech", "Blank",\
                   7, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event11)
    event12 = models.Event("Sky diving3", models.datetime.now(), \
                   "Afraid of not falling properly and hurting myself ", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event12)
    
    event13 = models.Event("Toastmasters speech4", models.datetime.now(), \
                   "I might go blank or forget lines from my speech", "Blank",\
                   7, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event13)
    event14 = models.Event("Sky diving4", models.datetime.now(), \
                   "Afraid of not falling properly and hurting myself ", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event14)

    event15 = models.Event("Speech4", models.datetime.now(), \
                   "May not be able to do a good job", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event15)
    event16 = models.Event("Public speaking4", models.datetime.now(), \
                   "Feeling afraid of being judged", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event16)
    event17 = models.Event("Toastmasters speech5", models.datetime.now(), \
                   "I might go blank or forget lines from my speech", "Blank",\
                   7, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event17)
    event18 = models.Event("Sky diving5", models.datetime.now(), \
                   "Afraid of not falling properly and hurting myself ", "Blank",\
                   8, 0, FEARAPP_STATUS_CREATED, 0, user1.userid)
    models.db.session.add(event18)

    models.db.session.commit()

    
    models.Event.query.filter_by(eventid=event1.eventid).update(dict
    (posteventtxt="I was only nervous in the first 2-3 minutes of the speech. After that it all went really well.In fact people complemented me on my presentation skills. I now think I can do this.",postfearfactor=5,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event2.eventid).update(dict
    (posteventtxt="It is surprising how I did not do so badly. I will be honest, my heart was pounding until the first couple mins. But after that all went great.",postfearfactor=4,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event3.eventid).update(dict
    (posteventtxt="Well, I would say that I was nervous but not as bad as I thought. In fact people's reviews actually help me understand that I am actually very good.",postfearfactor=3,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event4.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=2,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event5.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=7,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event6.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=8,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event7.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=5,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event8.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=4,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event9.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=3,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event10.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=6,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event11.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=7,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event12.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=5,status=FEARAPP_STATUS_UPDATED))

    models.Event.query.filter_by(eventid=event13.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=5,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event14.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=4,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event15.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=3,status=FEARAPP_STATUS_UPDATED))
    
    models.Event.query.filter_by(eventid=event16.eventid).update(dict
    (posteventtxt="Not so much any more",postfearfactor=6,status=FEARAPP_STATUS_UPDATED))
    
    #Arch: deliberately leaving two events unupdated (the last two)    
    models.db.session.commit()

    return None




