import redis # type: ignore
from flask import current_app as app # type: ignore
import json
from ..models import db, Notification
redis_client = redis.from_url(app.config['REDIS_URL'])

def queue_notification(user):
    message = {
        "email": user.email,
        "message": "Thank you for subscribing to our newsletter!"
    }
    notification = Notification(user_id=user.id, message=message["message"])
    db.session.add(notification)
    db.session.commit()
    redis_client.lpush('notification_queue', json.dumps(message))
