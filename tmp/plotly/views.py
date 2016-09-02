###########################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   views.py      11/4/2014   Archana Bahuguna  Initial structure    
#   views.py      02/17/2014  Archana Bahuguna  View fns for fearapp 
#
#  Handles HTTP requests for a fear app using Flask/SQLAlchemy.
#  Flask session is implemented, Flask bcrypt is used for pwd encryption.
#  Jinja templating is used for ui of web app
#
###########################################################################

import os, logging
from pprint import pprint
from flask import Flask, request, render_template, make_response, session
from flask.ext.sqlalchemy import SQLAlchemy, sqlalchemy
from flask.ext.bcrypt import Bcrypt
import datetime

import models
import logs
#import plotsline
import plotsbar

#pagination
POSTS_PER_PAGE=3

#flask sets default static and templates folders to 'static' & 'templates'
#if you do not specify anything
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/index.html', methods = ['GET'])
def index():

    # GET /index
    if request.method == 'GET':
        error=""
        """Get index.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("index.html get fn: %s" %(request))

       # Return response
        #utls.display_tables()
        return render_template('welcome.html', error=error)

@app.route('/forms/login', methods = ['GET', 'POST'])
def login():

    #User clicks on login button- GET /users/login 
    if request.method == 'GET':
        error=""
        """Get login.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login.html get fn: %s" %(request))
        
        return render_template('loginform.html', error=error)

    # User posts log in info in form and submits -POST /login 
    elif request.method == 'POST':
        error=""
        """Post login.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login.html get fn: %s" %(request))


        if (request.form["Login"] != "Submit"):
            pass;
        # Return error
        else:
            username = request.form["username"]
            password = request.form["password"]
        
            query_obj=models.User.query.filter_by(username=username).first()
            userid=query_obj.userid

            #import pdb; pdb.set_trace()
            if (query_obj is None):
                error= "Username does not exist"
                return render_template('loginform.html', error=error)
            elif ((query_obj.username == username) and (not bcrypt.check_password_hash(query_obj.password,password))):
                error= "Password is incorrect"
                return render_template('loginform.html', error=error)

            if 'username' not in session:
                session['username']=username
            # Return response
            #utls.display_tables()
            return render_template('welcomelgn.html', username=username, userid=userid, error=error)

    else:# methods other than get/post
        error = "Incorrect Method"
        response = make_response(render_template('error.html', error=error), 400)
        return response

@app.route('/forms/logout')
def logout():

    # GET /
    error=""
    logs.debug_ ("_______________________________________________")
    logs.debug_ ("Fearapp post fn: %s" %(request))

    session.pop('username',None)

    # Return response
    #utls.display_tables()
    return render_template('logout.html', error=error)

@app.route('/forms/signup', methods = ['GET','POST'])
def signup():

    # GET /signup 
    if request.method == 'GET':
        error=""
        """Get signup.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("signup.html get fn: %s" %(request))

        # Return response
        #utls.display_tables()
        return render_template('signupform.html', error=error)

    # POST /signup 
    elif request.method == 'POST':
        error=""
        """Post login.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login.html get fn: %s" %(request))

        username = request.form["username"]
        password = request.form["password1"]
        password2 = request.form["password2"]
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        phone = request.form["phone"]
        email = request.form["email"]
        
        query_obj=models.User.query.filter_by(username=username).first()

        if (query_obj is not None):
            error= "Username already exists. Please choose a unique username"
            return render_template('signupform.html', error=error)
        
        elif (password != password2):
            error="Passwords do not match. Re-enter password"
            return render_template('signupform.html', error=error)
       
        elif ((len(password)<6) or (len(password2)<6)):
            print "Length of password should be greater than 6"
            return render_template('signupform.html', error=error)

        elif (len(phone)!=10):
            print "Incorrect phone no format. SHould be 10 digits"
            return render_template('signupform.html', error=error)

        #Check email and phone format

        #Also add a process where you send a notification (code) to phone 
        #so user can confirm it is him who is registering

        else:
        #Add new user to database
            models.db.session.add(models.User(username,
                                     bcrypt.generate_password_hash(password),
                                     firstname,
                                     lastname,
                                     phone,
                                     email))
            models.db.session.commit()
            query_obj=models.User.query.filter_by(username=username).first()
            userid=query_obj.userid
            if 'username' not in session:
                session['username']=username
        # Return response
        #utls.display_tables()
        return render_template('welcomelgn.html', username=username, userid=userid, error=error)


@app.route('/forms/newevent', methods = ['GET'])
def newevent():

    # GET /events (event info for user)
    if request.method == 'GET':
        error=""
        """Get userevents.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("userevents.html get fn: %s" %(request))

#Arch: you need to get userid first -maybe in func args; then write a query to get username
#The following should always result in error all through this code- look at quizngn code
        username = session['username']
        if 'username' not in session:
            print "Error user not in session"
        else:
            user_obj=models.User.query.filter_by(username=username).first()
            if user_obj:
                userid=user_obj.userid
                return render_template('createeventform.html',userid=userid, error=error)

@app.route('/forms/updateevent/<int:eventid>', methods = ['POST'])
def updateevent(eventid):

    # GET /events (event info for user)
    if request.method == 'POST':
        error=""
        """Get userevents.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("userevents.html get fn: %s" %(request))

        username = session['username']
        if 'username' not in session:
            print "Error user not in session"
        else:
            if (request.form["submit"] == "Update"):
                user_obj=models.User.query.filter_by(username=username).first()
                if user_obj:
                    userid=user_obj.userid
                    #get created event info and pass for template
                    event_obj=models.Event.query.filter_by(eventid=eventid).all()
                    event=event_obj[0]
                    return render_template('updateventform.html',userid=userid, event=event, error=error)


@app.route('/users/<int:userid>/events', methods = ['GET', 'POST'])
def userevents(userid):

    # GET /events (event info for user)
    if request.method == 'GET':
        error=""
        """Get userevents.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("userevents.html get fn: %s" %(request))

     #does flask get username from session from http message? does username
     #come in any form and appear as a function argument in uservents(username)?

        #get username from flask session
        username = session['username']
        
        if 'username' not in session:
            #return error#-------------------------------------?????-----
            print "Error -username not in session"

        #get user event info
        events= models.Event.query.filter_by(userid=userid).all()
        if (events is None):
            print "error, no events for this username"
            return render_template('error.html', error=error)

        # Return response
        #utls.display_tables()
        #Create graph comparison of pre and post event fear factors
        #filename to save graph in
        #import pdb; pdb.set_trace()
        return render_template('eventslist.html', username=username, events=events, error=error)

    # POST /events (new event creation) 
    elif request.method == 'POST':
        error=""
        """Post login.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login.html get fn: %s" %(request))

        #get username from flask session
        username = session['username']
        if 'username' not in session:
            print "Error -username not in session"

        if (request.form["Submit"]=="Submit"):
            title = request.form['title']
            preeventtxt = request.form['preeventtxt']
            prefearfactor = request.form['prefearfactor'] #no rating fear out of 10

            datetime = request.form['datetime'] #time of future event given by user

            users = models.User.query.filter_by(username=username).all()
            userid = users[0].userid
            status = 0
            #twiliosmsstatus = NONE for now- will be updated by polling sched app
            models.db.session.add(models.Event(title, datetime, preeventtxt, "", prefearfactor,0, status, 0, userid))
        
            models.db.session.commit()
            # Return response
            #utls.display_tables()
            return render_template('welcomelgn.html', username=username, userid=userid, error=error)


@app.route('/events/<int:eventid>', methods = ['GET', 'POST', 'DELETE'])
def userevent(eventid):

    # GET /event (event info for user)
    if request.method == 'GET':
        error=""
        """Get userevents.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("userevents.html get fn: %s" %(request))

        #get username from flask session
        username = session['username']

        if username not in session:
            print "Error -username not in session"

        event=models.Event.query.filter_by(eventid=eventid).first()
        
        # Return response
        #utls.display_tables()
        #Create graph comparison of pre annd post event fear factors
        #filename to save graph in
        from datetime import datetime
        if (event.datetime<datetime.now()):
            return render_template('eventresultsummaryU.html', event=event, error=error)
        else:
            return render_template('eventresultsummary.html', event=event, error=error)

    # PUT /eventid (Update event on event completion)
    elif request.method == 'POST':
        error=""
        """Put login.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login.html get fn: %s" %(request))

        #get username from flask session
        username=session["username"]
        if 'username' not in session:
            return None#-------------------------------------?????-----

        query_obj=models.User.query.filter_by(username=username).first()
        userid=query_obj.userid

        posteventtxt = request.form['posteventtxt']
        postfearfactor = request.form['postfearfactor'] 
        status=3

        models.Event.query.filter_by(eventid=eventid).update(dict
(posteventtxt=posteventtxt,postfearfactor=postfearfactor,status=status))
        models.db.session.commit()
        
        # Return response
        return render_template('welcomelgn.html', username=username, userid=userid, error=error)

    # DELETE /eventid (Delete event)
    elif request.method == 'DELETE':
        error=""
        """Post login.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("login.html get fn: %s" %(request))

        eventid = request.form["eventid"]
        models.Event.query.filter_by(eventid=eventid).delete()
        
        return render_template('useraccount.html', errmsg=errmsg, error=error)
        # Return response
        #utls.display_tables()


"""
Arch: for a javascript fn
@app.route('/jsurl', methods = ['POST'])
def jsurl():

    # JS URL testing
    if request.method == 'POST':
       import pdb; pdb.set_trace()
       print request.json
"""


@app.route('/users/<int:userid>/pages/<int:pageid>/txteventsresultsummary', methods = ['GET'])
def eventtxtresults(userid, pageid):                       
    
    # GET allevents summary for user (event sumaary result for user)
    if request.method == 'GET':
        error=""
        """Get texteventsresultsummary.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("gettextresultsummary.html get fn: %s" %(request))

     #does flask get username from session from http message? does username
     #come in any form and appear as a function argument in uservents(username)?

        #get username from flask session
        username = session['username']

        if 'username' not in session:
            print "Error: Username not in session"

        #Arch: Paginate the results into pages of 5 each- later we can try monthwise in dropdown
        events = models.Event.query.filter(models.Event.userid==userid, models.Event.status==3).paginate(page=pageid, per_page=2, error_out=False)
        thispage=events.items
        totalpages=events.pages
        if (events == []):
            print "error, no events for this username"
            return render_template('error.html', error=error)
        
        return render_template('txteventsresultsummary.html', thispage=thispage, pageid=pageid, userid=userid, totalpages=totalpages, error=error)

@app.route('/users/<int:userid>/grapheventsresultsummary', methods = ['GET'])
def eventgraphresults(userid):

    # GET allevents summary for user (event sumaary result for user)
    if request.method == 'GET':
        error=""
        """Get grapheventsresultsummary.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("getgraphresultsummary.html get fn: %s" %(request))

     #does flask get username from session from http message? does username
     #come in any form and appear as a function argument in uservents(username)?

        #get username from flask session
        username = session['username']

        import pdb; pdb.set_trace()
        if 'username' not in session:
            print "Error: Username not in session"

        #get user event info for events that have occured
        events = models.Event.query.filter(models.Event.userid==userid,models.Event.status==3).all()

        if (events == []):
            print "error, no events for this username"
            return render_template('error.html', error=error)
        
        #if using plotly
        plot_url1=plotsbar.eventplot(events)
        plotno = ''.join(s for s in plot_url1 if s.isdigit())

        return render_template('grapheventsresultsummary.html', events=events, plot_url1=plot_url1, plotno=plotno, error=error)


if __name__ == '__main__':

    models.db_init()
    #Initial config for db, this can be disabled
    #models.display_tables()
    #app.debug = True
    app.run('192.168.33.10', 5005)



