# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
import os
from twilio.rest import Client

def send_txt_message (destination: str, message: str) :
    # Find these values at https://twilio.com/user/account
    # To set up environmental variables, see http://twil.io/secure
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(body=message, from_="+15073535295", to=destination)

    print (message.sid)

def main() :
    send_txt_message("+6591504834", "Hello, You")


if __name__ == "__main__" :
    main()