from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class ParkingSpot(db.Model): 
    __tablename__ = 'parkingSpot'
    # mirrors the existing table in db
    Code = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(255), nullable=False)
    Latitude = db.Column(db.Float, nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    
    # sets the properties (of itself) when created
    def __init__(self, Name, Latitude, Longitude):
        self.Name = Name
        self.Latitude = Latitude
        self.Longitude = Longitude
    
    # json representation of trip
    def json(self):
        return {"Code": self.Code,
                "Name": self.Name,
                "Latitude": self.Latitude,
                "Longitude": self.Longitude}
    
@app.route("/parkingspot")
def create_trip():
    spots = ParkingSpot.query.all()
    if len(spots):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "parking spots": [spot.json() for spot in spots]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no parking spots."
        }
    ), 404
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)