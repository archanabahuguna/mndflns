###########################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   views.py      4/4/2015   Archana Bahuguna  Basic view functions
#
#  Handles HTTP requests for a fear app using Flask/SQLAlchemy.
#  Flask session is implemented, Flask bcrypt is used for pwd encryption.
#  Jinja templating is used for ui of web app
#
###########################################################################

import os, logging
from pprint import pprint
from flask import Flask, request, render_template, session, make_response, \
                  url_for, abort
from flask.ext.sqlalchemy import SQLAlchemy, sqlalchemy
from flask.ext.bcrypt import Bcrypt
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

#import pdb; pdb.set_trace()
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'mypyflask@gmail.com',
    MAIL_PASSWORD = 'Phloem13'
    )

mail=Mail(app)
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
import datetime as dt 
resetlink_context = []
#password reset expiry link for a user needs to expire after some time
PASSWORD_RESET_EXPIRY_WINDOW = dt.timedelta(days=30) #setting this to 30 days as most apps do these days

#pagination
POSTS_PER_PAGE=5

import models, logs
from constnts import *
import bokehbar, bokehradial


@app.route('/', methods = ['GET'])
@app.route('/index', methods = ['GET'])
@app.route('/index.html', methods = ['GET'])
def index():

    # GET /index
    if request.method == 'GET':
        error=""
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        userid=""
        loggedin=False
        username=""

        if 'username' in session:
            username=session['username']
            query_obj=models.User.query.filter_by(username=username).first()
            userid=query_obj.userid
            loggedin=True
            
        return render_template('index.html', loggedin=loggedin, username=username, userid=userid, error=error)


@app.route('/login', methods = ['GET', 'POST'])
@app.route('/login/', methods = ['GET', 'POST'])
@app.route('/login.html', methods = ['GET', 'POST'])
def login():
    reset=False
    #import pdb; pdb.set_trace()
    #User clicks on login button- GET /users/login 
    if request.method == 'GET':
        error=""

        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        
        return render_template('login.html', error=error, reset=reset)

    # User posts log in info in form and submits -POST /login 
    elif request.method == 'POST':
        error=""
        loggedin=False
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        if ((request.form["username"]) and (request.form["password"])):
            username = request.form["username"]
            password = request.form["password"]
        else:
            error= "Fields are empty!"
            return render_template('login.html', error=error, reset=reset), 400

        query_obj=models.User.query.filter_by(username=username).first()
        

        if (query_obj is None):
            error= "Username does not exist!"
            return render_template('login.html', error=error, reset=reset), 404
        elif ((query_obj.username == username) and (not bcrypt.check_password_hash(query_obj.password,password))):
            error= "Incorrect password. Type again!"
            return render_template('login.html', reset=reset, error=error), 400

        userid=query_obj.userid
        session['username']=username
        loggedin=True
        
        response=make_response()
        
        response.location="/users/"+str(userid)+"/dashboard"
        response.status_code=303
        return response

@app.route('/login/sendreset')
def sendresetlink():
    error=""
    usermsg=""
    initial=True
    
    #After user has typed emailid
    if (request.args.get('email')):
        email=request.args.get('email')
        query_obj=models.User.query.filter_by(email=email).first()        
        
        #invalid email
        if not query_obj: 
            error="User with that email does not exist. Please enter the correct email address."
            return render_template('loginreset.html', initial=initial, usermsg=usermsg, error=error)
        
        else: 
            initial=False
            
            #set token
            passwordresettoken=ts.dumps(email, salt='email-confirm-key')
            passwordtokenexpirytime=dt.datetime.now()+PASSWORD_RESET_EXPIRY_WINDOW
            #using "@" as the string separator- initially used "#" but that's a special char in url
            passwordresetlink="/login/resetpassword/"+passwordresettoken+'@'+passwordtokenexpirytime.strftime("%Y-%m-%d")
            print passwordresetlink
            #passwordresetlink=url_for('resetpassword')+passwordresettoken

            msg = Message(
                   'Your password reset request on Sati app',
                   sender=app.config['MAIL_USERNAME'],
                   recipients=[email]
                         )
            msg.body = "Hi You asked us to reset your password on Sati app."\
                   "If this is not you then please ignore. Otherwise click on the link below--\n\n"\
                   +passwordresetlink
            mail.send(msg)

            #create a context for this email which indicates a reset link received from this
            #user is authorized
            global resetlink_context
            if (email not in resetlink_context):
                resetlink_context.append(email)
            #print resetlink_context

            usermsg="A reset link has been successfully sent to you at your email."
            return render_template('loginreset.html', initial=initial, usermsg=usermsg, error=error)
                    
    else: 
        #Comes here first when user clicks on forgot password
        return render_template('loginreset.html', initial=initial, usermsg=usermsg, error=error)
    

@app.route('/login/resetpassword/<token>', methods = ['GET', 'POST'])
#Keeping token for post will distinguish one user from another, I guess-Arch
def resetpassword(token):
    
    #User clicks on login button- GET /users/login 
    if request.method == 'GET':
        
        reset=True
        error=""
        reset=True
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        
        (emailpart, expirytime)=token.split("@")
        try:
            #get email from token
            email = ts.loads(emailpart, salt="email-confirm-key", max_age=86400)
        except:
            abort(404)

        global resetlink_context
        #do we need to convert the string expirytime to datetime format?

        if ((email in resetlink_context) and (dt.datetime.now().strftime("%Y-%m-%d")<expirytime)):
            #valid email reset
            resetlink_context.remove(email)
        else:
            #Reset link sent by unauthorized user or token expired
            abort(401)
        return render_template('login.html', error=error, reset=reset, token=token)

    # User posts log in info in form and submits -POST /login 
    elif request.method == 'POST':
        error=""
        reset=True
        loggedin=False
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        if ((request.form["username"]) and (request.form["password"]) and (request.form["password2"])):
            username = request.form["username"]
            password = request.form["password"]
            password2 = request.form["password2"]
        else:
            error= "Fields are empty!"
            return render_template('login.html', error=error)

        if (password!=password2):
            error= "Password does not match confirm password!"
            return render_template('login.html', reset=reset, token=token, error=error), 400
        elif (len(password)<8):
            error= "Min. length of password should be 8 characters!"
            return render_template('login.html', reset=reset, token=token, error=error), 400

        password=bcrypt.generate_password_hash(password)
        models.User.query.filter_by(username=username).update(dict(password=password))
        models.db.session.commit()

        query_obj=models.User.query.filter_by(username=username).first()
        userid=query_obj.userid
        session['username']=username
        loggedin=True
        
        response=make_response()
        response.location="/users/"+str(userid)+"/dashboard"
        response.status_code=303
        return response

@app.route('/logout')
@app.route('/logout.html')
def logout():

    # GET /
    error=""
    loggedin=False
    logs.debug_ ("_______________________________________________")
    logs.debug_ ("HTTP request get fn: %s" %(request))

    if 'username' in session:
        session.pop('username',None)

    return render_template('index.html', loggedin=loggedin, error=error)


@app.route('/signup', methods = ['GET','POST'])
@app.route('/signup.html', methods = ['GET','POST'])
def signup():
    """
    Users enter their username, passwords and emails for sign up. 
    Phone no is optional- if they wish to receive sms notifications.
    ** The app does not send email notification to users on signup;
    ** OAuth or openID using Gmail/facebook/Twitter is not yet
    implemented. 
    ** Password can be reset online via email reset link- but email 
    is not verified
    """
    # email smtp server config app flask

    # GET /signup 
    if request.method == 'GET':
        error=""
        """Get signup.html"""
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        # Return response
        return render_template('signup.html', error=error)

    # POST /signup 
    elif request.method == 'POST':
        error=""
    
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        
        #Form validation - ideally use restful+request.parse OR WTForms?
        if ((request.form["username"]) and (request.form["password"]) and \
            (request.form["password2"]) and (request.form["email"])):
            username = request.form["username"]
            password = request.form["password"]
            password2 = request.form["password2"]
            email = request.form["email"]
        else:
            error= "Username, passwords and email fields are mandatory!"
            return render_template('signup.html', error=error), 400    
        phone=None
        if request.form["phone"]:
            phone = request.form["phone"] #not mandatory

        query_obj=models.User.query.filter_by(username=username).first()
         
        #Multiple users can have same email id and phone- so not checking for it
        if (query_obj is not None):
            error= "Username already exists. Please choose a unique username!"
            return render_template('signup.html', error=error), 400
        elif (password!=password2):
            error= "Password does not match confirm password!"
            return render_template('signup.html', error=error), 400
        #length os password is at least 8 characters
        elif (len(password)<8):
            error= "Min. length of password should be 8 characters!"
            return render_template('signup.html', error=error), 400
        #phone no is not mandatory
        elif ((phone) and (len(phone)!=10)):
            error= "Incorrect phone no format. Enter a 10 digit no!"
            return render_template('signup.html', error=error), 400
        else:
        #Add new user to database
            models.db.session.add(models.User(username,
                                     bcrypt.generate_password_hash(password),
                                     email,
                                     phone))
            models.db.session.commit()

            query_obj=models.User.query.filter_by(username=username).first()
            userid=query_obj.userid
            if 'username' not in session:
                session['username']=username
                loggedin = True
        # Return response
        
        return render_template('index.html', username=username, userid=userid, loggedin=loggedin, error=error)


@app.route('/users/<int:userid>/events', methods = ['POST'])
def userevents(userid):

    # POST /events (new event creation info submitted here) 
    if request.method == 'POST':
        error=""
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        username = session['username']
        if 'username' not in session:
            return render_template('login.html', error=error)

        if (request.form["Submit"]=="Submit"):
            if (request.form["title"] and request.form["preeventtxt"] and \
               request.form["prefearfactor"] and request.form["datetime"]):
                title = request.form['title']
                preeventtxt = request.form['preeventtxt']
                prefearfactor = request.form['prefearfactor'] #no rating fear out of 10
                datetime = request.form['datetime'] #time of future event given by user
            else:
                error= "All fields are mandatory!"
                return render_template('dashboard.html', error=error), 400

            users = models.User.query.filter_by(username=username).all()
            userid = users[0].userid
            status = 0

            models.db.session.add(models.Event(title, datetime, preeventtxt, "", prefearfactor,0, status, 0, userid))
            models.db.session.commit()
                    
            location="/users/"+str(userid)+"/dashboard"
            code=303
            response=make_response()
            response.location=location
            response.status_code=code
            return response


@app.route('/events/<int:eventid>', methods = ['GET','POST'])
def userevent(eventid):
    
    # Get event info to update the rest part
    if request.method == 'GET':
        error=""
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        username = session['username']
        if 'username' not in session:
            return render_template('login.html', error=error)
        
        if (request.args.get("submit") == "Update"):
            user_obj=models.User.query.filter_by(username=username).first()
            if user_obj: #The 'else' for this condition will not happen
                userid=user_obj.userid
                #get created event info and pass for template
                event_obj=models.Event.query.filter_by(eventid=eventid).all()
                event=event_obj[0]
                return render_template('updateventform.html',userid=userid, event=event, error=error)

    #Update event
    if request.method == 'POST':
        error=""
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        if 'username' not in session:
            #Also doesnt seem like this can happen
            return render_template('login.html', error=error)

        #get username from flask session
        username=session["username"]
        
        if (request.form["submit"] =="Submit"):
            query_obj=models.User.query.filter_by(username=username).first()
            userid=query_obj.userid

            posteventtxt = request.form['posteventtxt']
            postfearfactor = request.form['postfearfactor'] 
            status=3

            models.Event.query.filter_by(eventid=eventid).update(dict
                (posteventtxt=posteventtxt,postfearfactor=postfearfactor,status=status))
            models.db.session.commit()
        
            # Return response
            location="/users/"+str(userid)+"/dashboard"
            code=303
            response=make_response()
            response.location=location
            response.status_code=code
            return response


@app.route('/users/<int:userid>/pages/<int:pageid>/<strval>', methods = ['GET'])
def eventtxtresults(userid, pageid, strval): #default pageid=1 if url does not provide                      
    
    # GET all events summary for user (event summary result for user)
    if request.method == 'GET':
        error=""

        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        
        if 'username' not in session:
            return "Error: Username not in session"
        username=session['username']
        
        if (str(strval)=='updatedevents'):
            events = models.Event.query.filter(models.Event.userid==userid, models.Event.status==FEARAPP_STATUS_UPDATED).paginate(page=pageid, per_page=POSTS_PER_PAGE, error_out=False)
            futureevents=False
        else:
            events = models.Event.query.filter(models.Event.userid==userid, models.Event.status!=FEARAPP_STATUS_UPDATED).paginate(page=pageid, per_page=POSTS_PER_PAGE, error_out=False)
            futureevents=True
        thispage=events.items
        totalpages=events.pages

        #Not sure if the foll part of code is of any use since paginate takes care of 404. If error_out=False 
        #like in our case, no error is displayed on zero results; else it will return a 404 code automatically
        if (events == []):
            print "error, no events for this username"
            return render_template('error.html', error=error), 404
        
        return render_template('eventsajax.html', futureevents=futureevents, thispage=thispage, pageid=pageid, userid=userid, totalpages=totalpages, error=error)
                               


@app.route('/users/<int:userid>/dashboard', methods = ['GET'])
def eventgraphresults(userid):

    # GET allevents summary for user (event summary result for user)
    if request.method == 'GET':
        error=""
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

    
        if 'username' not in session:
            return None
        
        username=session['username']
        loggedin=True
                
        #if using bokeh
        events = models.Event.query.filter(models.Event.userid==userid,models.Event.status==3).all()
        olduser=False #has at least one event so a dashboard makes sense
        if (events):
            olduser=True

            #Unique js and div tag created everytime for a new plot
            bokehjs1, raddivtag=bokehradial.plotradial(events, userid)
            bokehjs2, bardivtag= bokehbar.plotbar(events, userid)

            return render_template('dashboard.html', olduser=True, raddivtag=raddivtag, bardivtag=bardivtag, loggedin=loggedin,\
                                    events=events, username=username, userid=userid, error=error)
                                
        else:
            return render_template('dashboard.html', olduser=False, loggedin=loggedin,
                                    events=events, username=username, userid=userid, error=error)
                                

if __name__ == '__main__':

    models.db_init()
    app.run('192.168.33.10', 5005)
