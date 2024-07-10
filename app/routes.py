from flask import request, jsonify, current_app as app
from .models import db, User, Log, Child, Notification
from .services.payment_service import create_order
from .services.email_service import send_email
from .services.notification_service import queue_notification
from datetime import datetime

@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user:
        user.subscribed = True
    else:
        user = User(name=data['name'], email=data['email'], age=data['age'], subscribed=True)
        db.session.add(user)
        db.session.commit()

    if 'child_name' in data and 'child_age' in data:
        child = Child(parent_id=user.id, child_name=data['child_name'], child_age=data['child_age'])
        db.session.add(child)
        db.session.commit()

    order = create_order(user.id)
    return jsonify(order), 200

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment():
    data = request.json
    user = User.query.get(data['userId'])
    # Add payment verification logic here

    if payment_verified:
        user.subscribed = True
        log = Log(user_id=user.id, timestamp=datetime.now())
        db.session.add(log)
        db.session.commit()
        queue_notification(user)
        return jsonify({"message": "Payment verified and user subscribed"}), 200
    return jsonify({"message": "Payment verification failed"}), 400
