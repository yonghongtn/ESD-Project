# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from os import environ
from twilio.rest import Client
import amqp_setup
import json
import os


from flask_cors import CORS
from flask import Flask, jsonify

app = Flask(__name__)
CORS(app)

monitorBindingKey='*.sms'


def receiveRefund():
    amqp_setup.check_setup()
    
    queue_name = "refundsms"  

    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.



def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a refund request by " + __file__)
    main(body)
    print() # print a new line feed



def send_txt_message (destination: str, message: str) :
    # Find these values at https://twilio.com/user/account
    # To set up environmental variables, see http://twil.io/secure

    # Need to pre set environment variables in windows computer first in order to work 
    account_sid = environ.get('TWILIO_ACCOUNT_SID')
    auth_token = environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=message, from_=environ.get('TWILIO_PHONE_NUMBER'), to=destination)

# @app.route('/Twilio/send_txt_message/<destination>')
def main(body) :
    stuff = json.loads(body)
    destination = stuff['PhoneNo']
    msg = stuff['message']
    send_txt_message(destination, msg)

    # return jsonify({'message': 'Message sent successfully!'})


# if __name__ == "__main__" :
#     app.run(port=5005, debug=True)

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveRefund()