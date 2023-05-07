from twilio.rest import Client
import os
import requests

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self, message):
        message = self.client.messages \
            .create(
                body=message,
                from_=os.environ.get("TWILIO_PHONE_NUMBER"),
                to=os.environ.get("MY_PHONE_NUMBER")
            )

        print(message.sid)
    pass