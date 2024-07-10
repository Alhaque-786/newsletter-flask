import schedule
import time
from datetime import datetime
from .. import db
from ..models import User
from ..services.email_service import send_email

def send_newsletters():
    with app.app_context():
        users = User.query.filter_by(subscribed=True).all()
        for user in users:
            age_group = get_age_group(user.age)
            message = f"Newsletter for {age_group}"
            send_email(user.email, "Your Newsletter", message)
            notification = Notification(user_id=user.id, message="Newsletter sent")
            db.session.add(notification)
            db.session.commit()

def get_age_group(age):
    if age < 18:
        return "under 18"
    elif 18 <= age <= 34:
        return "18-34"
    else:
        return "35+"

schedule.every().day.at("00:00").do(send_newsletters)

while True:
    schedule.run_pending()
    time.sleep(1)
