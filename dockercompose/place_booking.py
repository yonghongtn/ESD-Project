from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import *
import os, sys
from os import environ
import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)
vehicle_url = environ.get('rentalvehicle_url')
rental_url = environ.get('rental_url')

""" 
Takes in a JSON of the format:
{
    "DriverID": 1,
    "PlateNo": "ABC1234D",
    "BookingDuration": 2,
    "TotalFare": 2000,
    "StartLocation": 1,
}
 """

@app.route("/place_booking", methods=['POST'])
def place_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking = request.get_json()
            print("\nReceived an booking in JSON:", booking)

            # do the actual work
            result = processBooking(booking)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_booking.py internal error: " + ex_str
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def processBooking(booking):
    #1. Call RentalVehicle microservice to update vehicle to booked status
    try: 
        print('\n-----Invoking RentalVehicle microservice-----')
        print(vehicle_url, booking["PlateNo"])
        booking_result = invoke_http(vehicle_url + booking["PlateNo"], method='PUT')
        print('booking_result:', booking_result)
        if booking_result["code"] != 201:
            return {
                "code": 500,
                "message": "An error occurred in the RentalVehicle microservice."
            }
    except:
        return {
                "code": 500,
                "message": "An error occurred in the RentalVehicle microservice."
            }
    #2 Call Rental microservice to create a new rental
    try:
        print('\n-----Invoking Rental microservice-----')
        new_booking = {
            "DriverID": booking["DriverID"],
            "PlateNo": booking["PlateNo"],
            "BookingDuration": booking["BookingDuration"],
            "TotalFare": booking["TotalFare"],
            "StartLocation": booking["StartLocation"],
        }
        print('new_booking:', new_booking)
        rental_result = invoke_http(rental_url, method='POST', json=new_booking)
        print('rental_result:', rental_result)
        if rental_result["code"] != 201:
            return {
                "code": 500,
                "message": "An error occurred in the Rental microservice."
            }
    except:
        return {
                "code": 500,
                "message": "An error occurred in the Rental microservice."
            }
    #3 Return success message
    return {
        "code": 200,
        "message": "Booking successful.",
        "data": rental_result
    }

    


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an booking...")
    app.run(host="0.0.0.0", port=5200, debug=True)



    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.