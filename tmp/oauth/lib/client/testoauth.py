#****************************************************************************
#           Name                File             Date        Desc
#      ---------------         ------------    ---------     ------------
#      Archana Bahuguna        testoauth.py    08/20/2015    oauth client
#
#      Desc: This app is using google oauth to authenticate users. The 
#            resource being accessed is whether user is authenticated or not.             
#
#****************************************************************************

class oauthlib(object):
	def __init__(key, secret, provider,base_url, request_token_url,access_token_url,authorize_url):
		self.consumer_key=key
		self.consumer_secret=secret
		self.provider=provider
        self.base_url=base_url
        self.request_token_url=request_token_url
        self.access_token_url=access_token_url
        self.authorize_url=authorize_url
        self.callback_url=callback_url

#Twitter consumer key
#    consumer_key='PSiDBhcYZX5LfJCL3FBimBUDz',
#    consumer_secret='GRYFHRDHwgYUVf7rhnt6lTOvOiQ0wp8OUm4YCRR8sTMAQwRijg'

	def authorize():
		pass

	def accesstoken():
		pass

	def (token=None, secret=None):

@app.route('/login', methods=['GET'])
def login():
	if 'username' in session:
	    username=session['username'] #return user object from userid
	user=get_user_obj(username)
	if user.is_authenticated(): 
		#do nothing? Since authenticating is the only purpose of the app
		#return user to the main page like index.html etc
		return redirect(url_for('/index') or request.Referrer#need to check this)
	else: #user not authenticated? what are the other options? Not logged in?
	    return oauth.authorize(oauth.authorize_url, 
	    	            url_for('/oauth_authorized'), #redirect url 
	    	            oauth.key,
        	            oauth.secret)

@app.route('/oauth_authorized', methods=['POST'])
def authorized(resp):

	if resp.status=200: #checking if authentication happened correctly
	    user.key=resp.data[key]
	    user.secret=resp.data[secret]
	    user.is_authenticated=True
	    return redirect(url_for('/index') or request.Referrer)
	elif resp.status=401:
	   	flash(u'Unauthorized request')
	elif resp.status=500:
	   	flash(u'Service you requested cannot be found')
	else:
	   	flash(u'Some other error')
























