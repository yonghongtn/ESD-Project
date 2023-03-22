from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3308/rentaltrip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Rental(db.Model): 
    __tablename__ = 'rental'
    # mirrors the existing table in db
    RentalID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DriverID = db.Column(db.Integer, nullable=False)
    PlateNo = db.Column(db.String(8), nullable=False)
    StartTime = db.Column(db.DateTime, nullable=False)
    EndTime = db.Column(db.DateTime)
    StartLocation = db.Column(db.Integer, nullable=False)
    EndLocation = db.Column(db.Integer)
    BookingDuration = db.Column(db.Float, nullable=False)
    TotalFare = db.Column(db.Float, nullable=False)
    
    # sets the properties (of itself) when created
    def __init__(self, DriverID, PlateNo, StartTime, StartLocation, BookingDuration, TotalFare):
        self.DriverID = DriverID
        self.PlateNo = PlateNo
        self.StartTime = StartTime
        self.EndTime = None
        self.StartLocation = StartLocation
        self.EndLocation = None
        self.BookingDuration = BookingDuration
        self.TotalFare = TotalFare
    
    # json representation of trip
    def json(self):
        return {"RentalID": self.RentalID,
                "DriverID": self.DriverID,
                "PlateNo": self.PlateNo,
                "StartTime": self.StartTime,
                "EndTime": self.EndTime,
                "StartLocation": self.StartLocation,
                "EndLocation": self.EndLocation,
                "BookingDuration": self.BookingDuration,
                "TotalFare": self.TotalFare}
    
# @app.route("/rental/<DriverID>/<PlateNo>/<StartLocation>/<BookingDuration>/<TotalFare>", methods=['POST'])
@app.route("/rental", methods=['POST'])
def create_trip():

   # trip = Rental(DriverID, PlateNo, func.now(), StartLocation, BookingDuration, TotalFare)
    trip = request.get_json()
    rental = Rental(trip["DriverID"], trip["PlateNo"], func.now(), trip["StartLocation"], trip["BookingDuration"], trip["TotalFare"])
    try:
        db.session.add(rental)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the trip"
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": rental.json()
        }
    ), 201

@app.route("/rental/<RentalID>/<PlateNo>", methods=['PUT'])
def change_car(RentalID, PlateNo):
    trip = Rental.query.filter_by(RentalID=RentalID).first()

    if trip:
        try:
            trip.PlateNo = PlateNo
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": trip.json()
                }
            ), 201
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "RentalID": RentalID
                    },
                    "message": "An error occurred when updating the vehicle for trip id {}".format(RentalID)
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "RentalID": RentalID
                },
                "message": "Trip not found."
            }
        ), 404

@app.route("/rental/endtrip/<RentalID>/<EndLocation>", methods=['PUT'])
def end_trip(RentalID, EndLocation):
    trip = Rental.query.filter_by(RentalID=RentalID).first()

    if trip:
        try:
            trip.EndLocation = EndLocation
            trip.EndTime = datetime.now()
            db.session.commit()
            return jsonify(
                {
                    "code": 201,
                    "data": trip.json()
                }
            ), 201
        except:
            return jsonify(
                {
                    "code": 500,
                    "data": {
                        "RentalID": RentalID
                    },
                    "message": "An error occurred when updating the vehicle for trip id {}".format(RentalID)
                }
            ), 500
    else:
        return jsonify(
            {
                "code": 404,
                "data": {
                    "RentalID": RentalID
                },
                "message": "Trip not found."
            }
        ), 404


if __name__ == '__main__':
    app.run(port=5001, debug=True)