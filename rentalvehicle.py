
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/rentalvehicle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    plateno = db.Column(db.String(8), primary_key= True)
    brand = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    vehiclestatus = db.Column(db.String(50), nullable=False)
    parkingspotname = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float(precision="2"), nullable=False)
    latitude = db.Column(db.Float(precision="2"), nullable=False)
    longitude = db.Column(db.Float(precision="2"), nullable=False)
    

    def __init__(self,plateno,brand,model,vehiclestatus,parkingspotname,price,latitude,longitude):
        self.plateno = plateno
        self.brand = brand
        self.model = model
        self.vehiclestatus = vehiclestatus
        self.parkingspotname = parkingspotname
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        

    def json(self):
        return {"PlateNo": self.plateno,
                "Brand": self.brand,
                "Model": self.model,
                "VehicleStatus": self.vehiclestatus,
                "ParkingSpotName": self.parkingspotname,
                "Price": self.price,
                "Latitude": self.latitude,
                "Longitude": self.longitude}
    


@app.route("/rentalvehicle/")
def get_all():
    vehiclelist = Vehicle.query.all()
    if(len(vehiclelist)):
        return jsonify(
            {
                "code":200,
                "data":{
                    "vehicles": [vehicle.json() for vehicle in vehiclelist]
                }
            }
        )
    return jsonify(
        {
            "code":404,
            "message": "There are no vehicles."
        }
    ),404

@app.route("/rentalvehicle/<string:brand>")
def get_by_brand(brand):
    vehiclelist = Vehicle.query.filter_by(brand=brand).all()
    if len(vehiclelist):
        return jsonify(
            {
                "code": 200,
                "data":{
                    
                    "vehicles": [vehicle.json() for vehicle in vehiclelist]

                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Vehicle not found."
        }
    ), 404



@app.route("/rentalvehicle/updatebooked/<string:plateno>", methods=['PUT'])
def update_vehicle(plateno):
    vehicle = Vehicle.query.filter_by(plateno=plateno).first()
    if vehicle:
        try:
            vehicle.vehiclestatus = 'Booked'
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": vehicle.json()
                }
            ),201
        except:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "plateno": plateno
                    },
                    "message": "Vehicle not found."
                }
            ), 404
""" 
Accepts a JSON object with the following attributes:
{
    "parkingspotname": "Parking Spot 1",
    "latitude": 1.2345,
    "longitude": 1.2345
}
 """
@app.route("/rentalvehicle/updateavailable/<string:plateno>", methods=['PUT'])
def update_vehicle_available(plateno):
    update = request.get_json()
    vehicle = Vehicle.query.filter_by(plateno=plateno).first()
    if vehicle:
        try:
            vehicle.vehiclestatus = 'Available'
            vehicle.parkingspotname = update["parkingspotname"]
            vehicle.latitude = update["latitude"]
            vehicle.longitude = update["longitude"]
            db.session.commit()
            return jsonify(
                    {
                        "code": 201,
                        "data": vehicle.json()
                    }
                ),201
        except:
            return jsonify(
                    {
                        "code": 404,
                        "data": {
                            "plateno": plateno
                        },
                        "message": "Vehicle not found."
                    }
                ), 404      

@app.route("/rentalvehicle/damage/<string:plateno>", methods=['PUT'])
def damage_update(plateno):
    vehicle = Vehicle.query.filter_by(plateno=plateno).first()
    if vehicle:
        try:
            vehicle.vehiclestatus = 'Damaged'
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": vehicle.json()
                }
            ),201
        except:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "plateno": plateno
                    },
                    "message": "Vehicle not found."
                }
            ), 404   

if __name__ == '__main__':
    app.run(port=5003,debug=True)
