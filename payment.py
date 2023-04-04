#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os,sys
from flask import Flask, redirect, request, jsonify
import requests
from invokes import invoke_http
import stripe
from flask_cors import CORS
# This is your test secret API key.
stripe.api_key = 'sk_test_51MmZA2FZwLHtEN8WhQHaD5gC1XiWk9wni4zCP8p60kq6hC6H6nP6x5yu5XCQSKmOQF6VgNHB3AwJybDG8mpkgbFX00vgT93OCZ'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')
CORS(app)
YOUR_DOMAIN = 'http://localhost:5006'


""" 
When a customer clicks on the button to checkout, redirect them to your Checkout page.
Accepts the following JSON parameters:
{
    "price": "price_1J9Z9tFZwLHtEN8W1qZ1Zq2a",
    "quantity": 1
}

 """
@app.route('/create-checkout-session/<priceid>/<int:quantity>', methods=['GET'])
def create_checkout_session(priceid, quantity):

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                    {
                        'price': priceid,
                        'quantity': quantity,
                    }
                ],
            mode='payment',
            success_url='http://localhost/ESDProject/booking.html',
            cancel_url='http://localhost/ESDProject/booking.html',
            )
        return jsonify({"sessionId": checkout_session['id'],"url": checkout_session['url'],"object": checkout_session})

    except Exception as e:
        return str(e)

@app.route('/retrieve-session/<sessionid>', methods=['GET'])    
def retrieve_session(sessionid):
    try:
        session = stripe.checkout.Session.retrieve(sessionid)
        return jsonify({"sessionId": session['id'],"payment_intent": session['payment_intent']})
    except Exception as e:
        return str(e)
    




@app.route('/refund-payment/<payment_intent_id>', methods=['POST'])
def refund_payment(payment_intent_id):
    # payment_intent_id = request.form['payment_intent_id']
    # payment_intent_id = "pi_3MsMjPFZwLHtEN8W0Py49Hg7"
    try:
        # Retrieve the payment intent to make sure it hasn't already been refunded
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        # if payment_intent['amount_refunded'] == payment_intent['amount']:
        #     return 'Error: Payment already refunded.'
        
        # Refund the payment intent
        refund = stripe.Refund.create(payment_intent=payment_intent_id)
        
    except Exception as e:
        return str(e)

    return 'Payment refunded successfully!'


if __name__ == '__main__':
    app.run(port=5006, debug= True)
    
    
