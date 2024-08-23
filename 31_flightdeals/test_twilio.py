# Download the helper library from https://www.twilio.com/docs/python/install

from twilio.rest import Client
import json
#import requests

secret_data = json.load(open('secrets.json'))

class NotificationManager:
    def __init__(self):
      self.account_sid = secret_data["twilio_auth"]["account_sid"]
      self.auth_token = secret_data["twilio_auth"]["auth_token"]
      self.phone_no = secret_data["twilio_auth"]["phone_no"]
      self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, to_no):
        message = self.client.messages.create(
            body="Join Earth's mightiest heroes. Like Kevin Bacon.",
            from_= self.phone_no,
            to= to_no,
        )

        return print(message.body)
    
my_messenger = NotificationManager()
my_messenger.send_message(to_no="12265004547")