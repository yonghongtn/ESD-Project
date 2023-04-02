import stripe

# Set your Stripe API key
stripe.api_key = 'sk_test_51MmZA2FZwLHtEN8WhQHaD5gC1XiWk9wni4zCP8p60kq6hC6H6nP6x5yu5XCQSKmOQF6VgNHB3AwJybDG8mpkgbFX00vgT93OCZ'

# Create a new price
price = stripe.Price.create(
    unit_amount=7,  # Set the price in cents. In this case, it's $5.
    currency='sgd',  # Set the currency of the price
    product='prod_NadPO9VwzIkITm',  # Set the product ID
)

# # Retrieve the price ID
# price_id = price.id
