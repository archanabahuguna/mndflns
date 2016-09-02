#if using blueprints all you need to do is also add the following lines
#to views.py
"""
from blueprintlogin import login_bp
app.register_blueprint(login_bp)
"""

from flask import Blueprint
login_bp=Blueprint('login_bp', __name__, template_folder='templates')

from views import *

@login_bp.route('/login', methods = ['GET', 'POST'])
@login_bp.route('/login.html', methods = ['GET', 'POST'])
def login():

    #User clicks on login button- GET /users/login 
    if request.method == 'GET':
        error=""
        
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        
        return render_template('login.html', error=error)

    # User posts log in info in form and submits -POST /login 
    elif request.method == 'POST':
        error=""
        loggedin=False
        reset=False
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))

        if ((request.form["username"]) and (request.form["password"])):
            username = request.form["username"]
            password = request.form["password"]
        else:
            error= "Fields are empty!"
            return render_template('login.html', error=error), 400

        query_obj=models.User.query.filter_by(username=username).first()
        

        if (query_obj is None):
            error= "Username does not exist!"
            return render_template('login.html', error=error), 404
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

@login_bp.route('/login/sendreset')
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
            error="User with that email does not exist. Please enter the correct email."
            return render_template('loginreset.html', initial=initial, usermsg=usermsg, error=error)
        
        #email indicates a valid user
        else: 
            initial=False

            passwordresettoken=bcrypt(email+models.datetime.now())
            #passwordtokenexpiry=
            passwordresetlink="http://192.168.33.10/login/reset-password/"+resettoken
            
            msg = Message(
              'Your password reset request on Sati login_bp',
              sender='mypyflask@gmail.com',
              recipients=[email]
                 )
            msg.body = "Hi You asked us to reset your password on Sati login_bp."\
                   "If this is not you then please ignore. Otherwise click on the link below--\n\n"\
                   +resetlink
            mail.send(msg)
            usermsg="A reset link has been successfully sent to you at your email."
            return render_template('loginreset.html', initial=initial, usermsg=usermsg, error=error)
                    
    else: 
        #Comes here first when user clicks on forgot password
        return render_template('loginreset.html', initial=initial, usermsg=usermsg, error=error)
    

@login_bp.route('/login/reset-password', methods = ['GET', 'POST'])
@login_bp.route('/login/reset-password.html', methods = ['GET', 'POST'])
def resetpassword():

    #User clicks on login button- GET /users/login 
    if request.method == 'GET':
        error=""
        reset=True
        logs.debug_ ("_______________________________________________")
        logs.debug_ ("HTTP request get fn: %s" %(request))
        
        return render_template('loginreset.html', error=error)

    # User posts log in info in form and submits -POST /login 
    elif request.method == 'POST':
        error=""
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

@login_bp.route('/logout')
@login_bp.route('/logout.html')
def logout():

    # GET /
    error=""
    loggedin=False
    logs.debug_ ("_______________________________________________")
    logs.debug_ ("HTTP request get fn: %s" %(request))

    if 'username' in session:
        session.pop('username',None)

    return render_template('index.html', loggedin=loggedin, error=error)
