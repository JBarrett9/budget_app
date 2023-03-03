from flask import url_for
from flask_mail import Message

from budgetapp import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@budgetapp.com',
                  recipients=[user.email])
    msg.body = f'''A request has been made to change the password associated with your account. Click on the following
link to reset your password:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request simply ignore this  message.
    '''
    mail.send(msg)


def send_user_invite(user, email):
    token = user.get_add_token()
    msg = Message('Budget App Invite',
                  sender='noreply@budgetapp.com',
                  recipients=[email])
    msg.body = f'''{user.name} has sent you an invitation to share their budget account. Click on the following link to 
create an account:
{url_for('users.add_token', token=token, _external=True)}
'''
    mail.send(msg)
