import razorpay
from flask import current_app as app

client = razorpay.Client(auth=(app.config['RAZORPAY_KEY_ID'], app.config['RAZORPAY_KEY_SECRET']))

def create_order(user_id):
    order = client.order.create({
        "amount": 50000,  # amount in paise
        "currency": "INR",
        "receipt": f"receipt_{user_id}"
    })
    return order
