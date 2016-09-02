#*****************************************************************************
#      Name             Date         Filename       Functionality
#    ********         *********     ***********    ***************       
#  Archana Bahuguna  17th Aug 2015  oauthclient.py 3rd party oauth2.0 client 
#
# This code is not pythonic - 
#
#*****************************************************************************

from flask_oauth import OAuth
from flask import redirect
from flask import session

oauth=OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='<your key here>',
    consumer_secret='<your secret here>'
)

@twitter.tokengetter
#Registers function get_twitter_token as tokengetter
def get_twitter_token(token=None):
    """This method is used to get the access token received earlier from the
    auth server or Identity provider on a per user basis. Saving it in 
    session keeps the token on a user basis. Can/should this be stored in db?
    """
    return session.get('twitter_token')

@app.route('/users/<userid>/data')
#Need to recheck this endpoint- when user clicks show my bank info after 
#logging in?
def get_user_resource():    
    """This method is used to get user resource. If token available, get 
    resource from auth server by sending token and secret and receiving back 
    the link. If not, send an authorization request to ask for permission to 
    access the user resources.
    """
    if resp is None: 
        twitter.authorize(callback=url_for('oauth_authorized'),
                     next=request.args.get('next') or request.referrer or None)
        #meaning tokens were valid & auth resources are recvd from the auth server
        return redirect()
    else:
        resp=send_access_token_request():
                       
def send_access_token_request():
    """This method sends an access token request to auth server to get user 
    resources Does it automatically get tokens from tokengetter fn?
    """
    return request(url=twitter.access_token_url, 
                 format='urlencoded', 
                 method='GET')
    #problem: check how flask documentn uses token- seems like tokengetter is

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):

    if resp is not None:
        #if authorization resp recvd from provider, save the token and secret
        #send resource request with token- Do we send this now or only when requested?
        session['twitter_token']=(resp['oauth_token'], resp['oauth_secret'])
        return send_access_token_request() 
    else:
        #Redirect user to main page on app since the resource access was denied
        flash(u'You did not authorize the access to the resource.')
        return redirect(request.args.get('next') or url_for('/index'))


def refresh_token_to_renew_resource_request():

