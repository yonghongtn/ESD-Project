from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3308/rentalvehicle'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    plateno = db.Column(db.String(8), primary_key= True)
    brand = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    vehiclestatus = db.Column(db.String(20), nullable=False)
    parkingspotname = db.Column(db.String(50), nullable=False)
    

    def __init__(self,plateno,brand,model,vehiclestatus,parkingspotname):
        self.plateno = plateno
        self.brand = brand
        self.model = model
        self.vehiclestatus = vehiclestatus
        self.parkingspotname = parkingspotname

    def json(self):
        return {"PlateNo": self.plateno, "Brand": self.brand, "Model": self.model, "VehicleStatus": self.vehiclestatus, "ParkingSpotName": self.parkingspotname}
    


@app.route("/rentalvehicle")
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



@app.route("/rentalvehicle/update/<string:plateno>", methods=['PUT'])
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
if __name__ == '__main__':
    app.run(port=5000,debug=True)
