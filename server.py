#! /usr/bin/env python3.6

"""
server.py
Stripe Sample.
Python 3.6 or newer required.
"""
import os
from flask import Flask, redirect, request

import stripe
# This is your test secret API key.
stripe.api_key = 'sk_test_51MmZA2FZwLHtEN8WhQHaD5gC1XiWk9wni4zCP8p60kq6hC6H6nP6x5yu5XCQSKmOQF6VgNHB3AwJybDG8mpkgbFX00vgT93OCZ'

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

YOUR_DOMAIN = 'http://localhost:5006'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    # 'product': 'prod_NadPO9VwzIkITm',
                    'price': 'price_1MpSOYFZwLHtEN8Wv6ssbnsX',
                    'quantity': 2,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303) 





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
    
    
