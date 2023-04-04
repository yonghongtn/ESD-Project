import os
from flask import Flask, redirect, request, jsonify, url_for
import stripe

app = Flask(__name__,
            static_url_path='',
            static_folder='public')

# This is your test secret API key.
app.config['STRIPE_PUBLIC_KEY']= 'pk_test_51MmZA2FZwLHtEN8WbCC5jqApkid9bBWeJ3ufL4C7T9I1y8FqyjrIlN7M2SYQXfnw3lkZmIoJb6SPC7gtRy1xHzCX00T1e0faZF'
app.config['STRIPE_SECRET_KEY']= 'sk_test_51MmZA2FZwLHtEN8WhQHaD5gC1XiWk9wni4zCP8p60kq6hC6H6nP6x5yu5XCQSKmOQF6VgNHB3AwJybDG8mpkgbFX00vgT93OCZ'
stripe.api_key = app.config['STRIPE_SECRET_KEY']

YOUR_DOMAIN = 'http://localhost:4242'

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # data = request.get_json()
        # price = data['price']
        # quantity = data['quantity']
       
        
        # price = 'price_1MsPOIFZwLHtEN8Wtw0f4SOT'
        quantity = 1
        
        price_id = "price_1MsPOIFZwLHtEN8Wtw0f4SOT"
        price = stripe.Price.retrieve(price_id)
        product = stripe.Product.retrieve(price.product)
        print(product)


        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Uncomment the price & quantity of the product you want to sell
                    
                    # # Kia Nitro Hybrid, $10
                    # 'price': 'price_1MsPOIFZwLHtEN8Wtw0f4SOT',
                    # 'quantity': 1,
                    
                    # # Honda Civic, $20
                    # 'price': 'price_1MsPToFZwLHtEN8WZIbuZs75',
                    # 'quantity': 1,
                    
                    'price': price,
                    'quantity': quantity,
                },
            ],
            
                #    Stripe gets car details from price_id
            # product_id = price.product
            # product = stripe.Product.retrieve(product_id)
            # product_metadata = product.metadata
            # product_name = product.name
            # product_details= product.details
            # print(product_details)
            mode='payment',
            success_url=YOUR_DOMAIN + '/success.html',
            cancel_url=YOUR_DOMAIN + '/cancel.html',
            # success_url= url_for('success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            # cancel_url=url_for('cancel', _external=True),
            
        )
    except Exception as e:
        return str(e)

    
    return redirect(checkout_session.url, code=303) 
    # redirect(checkout_session.url, code=303) 
    # return jsonify({'name': product_name, 'metadata': product_metadata})






   

    """def webhook():

    Returns:{}
    Prints: Payment intent in terminal below "WEBHOOK CALLED"
            eg: PAYMENT_INTENT_ID:
                pi_3Mt1ZlFZwLHtEN8W0nHxmMm8  
    Can also send the information elsewhere depending on where you want it   
        
    """
# stripe listen --forward-to 127.0.0.1:4242/stripe_webhook
@app.route('/stripe_webhook', methods=['POST'])
def webhook():
    print("WEBHOOK CALLED")

    if request.content_length> 1024 * 1024:
        print("Request too big.")
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_4297b4da3c900638c135bdbff1b86b417f4af894ab1097acd92a63aaa43ad5f4'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    
    except stripe.error.SignatureVerificationError as e:
        # Invalid signture
        print('INVALID SIGNATURE')
        return {}, 400
    
    # Handle the event: Print payment intent
    if event['type'] == 'checkout.session.completed':
        payment_intent_id = event['data']['object']['payment_intent'] # retrieve the PaymentIntent ID
        print("PAYMENT_INTENT_ID: ")
        print(payment_intent_id )
        
        
        
        '''THE COMMENTED PART DOESNT WORK YET'''
    # # Handle the event: Send receipt
    # if event['type'] == 'payment_intent.succeeded':
    #     payment_intent_id = event['data']['object']['id']
    #     customer_email = event['data']['object']['payment_intent']['charges']['data'][0]['billing_details']['email']
    #     stripe.PaymentIntent.modify(
    #         payment_intent_id,
    #         receipt_email=customer_email
    #     )   
    
    
    # # Handle the event: Print refund successful and send refund receipt
    # elif event['type'] == 'charge.refunded':
    #     refund_id = event['data']['object']['id']
    #     customer_email = event['data']['object']['billing_details']['email']
    #     print("Refund successful: " + refund_id)
    #     stripe.Refund.modify(
    #         refund_id,
    #         refund_receipt_email=customer_email
        # )  
        
    # Handle the event: Print payment intent
        #     session = event['data']['object']
        #     print(session)
        # line_items = stripe.checkout.Session.list_line_items(session['id'], limit = 1)
        # print(line_items['data'][0]['description'])
    
    # If want to store in another db / send receipt (code not done)
        # payment_intent_id = session.get('payment_intent')
        # if payment_intent_id:
        #     payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        #     print( payment_intent)
        #     return jsonify(payment_intent)
            
    return {}  
    








    """def refund_payment():
    Input: Payment_Intent
    Does: Refund
    Returns:
    Prints: 'Payment refunded successfully!'    
        
    """
@app.route('/refund-payment', methods=['POST'])
def refund_payment():
    # payment_intent_id = request.form['payment_intent_id']
    payment_intent_id = "pi_3MpUSoFZwLHtEN8W1GFwPJiW"
    try:
        # Retrieve the payment intent to make sure it hasn't already been refunded
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        # Refund the payment intent
        refund = stripe.Refund.create(payment_intent=payment_intent_id)
    except Exception as e:
        return str(e)

    return 'Payment refunded successfully!'


if __name__ == '__main__':
    app.run(port=4242, debug= True)
    
    
    
    
