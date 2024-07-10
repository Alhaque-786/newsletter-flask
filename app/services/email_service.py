from flask_mail import Message # type: ignore
from . import mail

def send_email(to, subject, template):
    msg = Message(subject, recipients=[to])
    msg.body = template
    mail.send(msg)
