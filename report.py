from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3308/report'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)

class Report(db.Model): 
    __tablename__ = 'rentalreport'
    # mirrors the existing table in db
    ReportID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DriverID = db.Column(db.Integer, nullable=False)
    PlateNo = db.Column(db.String(8), nullable=False)
    Outcome = db.Column(db.String(100), nullable=False)
    Content = db.Column(db.String(1000), nullable=False)
    
    # sets the properties (of itself) when created
    def __init__(self, DriverID, PlateNo, Outcome, Content):
        self.DriverID = DriverID
        self.PlateNo = PlateNo
        self.Outcome = Outcome
        self.Content = Content
    
    # json representation of Report
    def json(self):
        return {"ReportID": self.ReportID,
                "DriverID": self.DriverID,
                "PlateNo": self.PlateNo,
                "Outcome": self.Outcome,
                "Content": self.Content}
    

@app.route("/report", methods=['POST'])
def create_Report():
    rentalreport = request.get_json()
    report = Report(rentalreport["DriverID"], rentalreport["PlateNo"], rentalreport["Outcome"], rentalreport["Content"])
    try:
        db.session.add(report)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the report"
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": report.json()
            
            
        }
    ), 201

if __name__ == '__main__':
    app.run(port=5002, debug=True)