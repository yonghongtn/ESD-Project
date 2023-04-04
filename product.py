from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/rentalvehicle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import payment

# # Define Vehicle model
# class Vehicle(db.Model):
#     __tablename__ = 'vehicle'
#     plateno = db.Column(db.String(8), primary_key= True)
#     brand = db.Column(db.String(20), nullable=False)
#     model = db.Column(db.String(50), nullable=False)
#     vehiclestatus = db.Column(db.String(20), nullable=False)
#     parkingspotname = db.Column(db.String(50), nullable=False)
#     price = db.Column(db.Float(precision="2"), nullable=False)
#     latitude = db.Column(db.Float(precision="2"), nullable=False)
#     longitude = db.Column(db.Float(precision="2"), nullable=False)

# Retrieve all vehicles from database (complex microservice will POST)> change db
# vehicles = session.query(vehicle).all()

# Initialize Stripe API
payment.api_key = "sk_test_51MmZA2FZwLHtEN8WhQHaD5gC1XiWk9wni4zCP8p60kq6hC6H6nP6x5yu5XCQSKmOQF6VgNHB3AwJybDG8mpkgbFX00vgT93OCZ"

# Create vehicles in Stripe
for vehicle in vehicles:
    stripe_vehicle = payment.Product.create(
        name=vehicle.Model,
        id= vehicle.PlateNo,
        
        # type='good',
        description=vehicle.description
    )

    # Create price for the vehicle
    payment.Price.create(
        unit_amount=vehicle.price * 100,
        currency='sgd',
        vehicle=stripe_vehicle.id,
    )

if __name__ == '__main__':
    app.run()
