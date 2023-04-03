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
    
    
    
    
