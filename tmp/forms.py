###########################################################################
#
#   File Name      Date          Owner            Description
#   ----------    -------      ----------       ----------------
#   forms.py    11/14/2014   Archana Bahuguna  Flask wtf forms for fearapp
#
#
###########################################################################

from flask_wtf import Form
from wtforms import TextField, IntegerField, PasswordField, RadioField, validators

class LoginForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=16)])
    password = PasswordField('Password', [validators.Length(min=4,max=16)])

class SignupForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=16)])
    password = PasswordField('New Password', [validators.Required(), 
                                              validators.EqualTo('confirm', message = 'passwords must match')])
    confirm = PasswordField('Repeat password']
    #Add other phone or email later
    mobilephone = IntegerField('Mobile Phone', [validators.Length(min=10, max=10)])
    email = Textfield('Email Address', [validators.Length(min=10, max=10)])
    #accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

class PreEventForm(Form):
    eventname = TextField('Event Name', [validators.Length(min=4, max=16)])
    eventdesc = TextField('Event description: What do you fear will happen at the event?',                                 [validators.Required(),validators.Length(min=3, max=500)])
    fearfactor = RadioField('Rate the fear you feel about the event', choices=[
                                                           ('0/5','No fear'),
                                                           ('1/5','Mild fear'),
                                                           ('2/5', 'Mild-Moderate fear'),
                                                           ('3/5','Moderate fear'),
                                                           ('4/5', 'Severe fear'), 
                                                           ('5/5', 'Mortified')])

class PostEventForm(Form):
    eventname = TextField('Event Name', [validators.Length(min=4, max=16)])
    eventdesc = TextField('Event description: Please describe how the event actually went',                                 [validators.Required(),validators.Length(min=3, max=500)])
    fearfactor = RadioField('Rate the fear that you actually felt at the event', choices=[
                                                           ('0/5','No fear'),
                                                           ('1/5','Mild fear'),
                                                           ('2/5', 'Mild-Moderate fear'),
                                                           ('3/5','Moderate fear'),
                                                           ('4/5', 'Severe fear'), 
                                                           ('5/5', 'Mortified')])

