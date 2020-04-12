from celery import Celery
from twilio.rest import Client
from app import cel


@cel.task(name='app.send_sms_reminder')
def send_sms_reminder():
    from app import TWILIO_ACCOUNT, TWILIO_TOKEN
    client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)
    phone = "+14702020929"
    body = "the reminder system is working!"
    to = "+14702637816"
    client.messages.create(to, from_=phone, body=body)