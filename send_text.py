# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
import os
from twilio.rest import Client

from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)


def send_txt_message (destination: str, message: str) :
    # Find these values at https://twilio.com/user/account
    # To set up environmental variables, see http://twil.io/secure

    # Need to pre set environment variables in windows computer first in order to work 
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']

    client = Client(account_sid, auth_token)
    
    message = client.messages.create(body=message, from_="+1 585 639 4954", to=destination)

    #print (message.sid)
    return jsonify({'message': 'Message sent successfully!'})

@app.route('/Twilio/send_txt_message/<destination>')
def main(destination) :
    
    hpnum = '+6597991787'
    msg = 'Your refund has been confirmed and send. Please check your bank account these few weeks. If there are any clarification or questions you have, do feel free to contact us. Thank you.'
    send_txt_message(destination, msg)

    return jsonify({'message': 'Message sent successfully!'})


if __name__ == "__main__" :
    #main()
    app.run(port=5005, debug=True)