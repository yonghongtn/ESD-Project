from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import *
import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)
rentalvehicle_url = "http://localhost:5003/rentalvehicle"
rental_url = "http://localhost:5001/rental"

paidAmt = 0;


@app.route("/place_booking", methods=['POST'])
def place_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            booking = request.get_json()
            print("\nReceived an booking in JSON:", booking)

            # do the actual work
            # 1. Send order info {cart items}
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
    print('\n-----Invoking booking microservice-----')
    booking_result = invoke_http(rental_url, method='POST', json=booking)
    print('booking_result:', booking_result)

    code = booking_result["code"]
    if code not in range(200, 300):
        # continue even if this invocation fails
        print("Booking status ({:d}) sent to the error microservice:".format(
            code), booking_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"booking_result": booking_result},
            "message": "Booking creation failure sent for error handling."
        }

def calculatePaidAmt(TotalFare, BookingDuration):
    paidAmt = TotalFare * BookingDuration

    return paidAmt

@app.route("/updatevehicle/updatebooked/<string:plateno>", methods=["PUT"])
def updateVehicleBooked():
    if request.is_json:
        try:
            vehicle = request.get_json()
            print("\nReceived an update vehicle request in JSON:", vehicle)

            # do the actual work
            # 1. Send order info {cart items}
            result = processUpdateVehicleBooked(vehicle)
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


def processUpdateVehicleBooked(vehicle):
    vehicle_result = invoke_http(rentalvehicle_url, method="PUT", json=vehicle)
    print("Vehicle result: ", vehicle_result)

    code = vehicle_result["code"]
    if code not in range(200, 300):
        # continue even if this invocation fails
        print("Vehicle status ({:d}) sent to the error microservice:".format(
            code), vehicle_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"vehicle_result": vehicle_result},
            "message": "Vehicle creation failure sent for error handling."
        }


@app.route("/updatevehicle/updateavailable/<string:plateno>", methods=["PUT"])
def updateVehicleAvailable():
    if request.is_json:
        try:
            vehicle = request.get_json()
            print("\nReceived an update vehicle request in JSON:", vehicle)

            # do the actual work
            # 1. Send order info {cart items}
            result = processUpdateVehicleAvailable(vehicle)
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


def processUpdateVehicleAvailable(vehicle):
    vehicle_result = invoke_http(rentalvehicle_url, method="PUT", json=vehicle)
    print("Vehicle result: ", vehicle_result)

    code = vehicle_result["code"]
    if code not in range(200, 300):
        # continue even if this invocation fails
        print("Vehicle status ({:d}) sent to the error microservice:".format(
            code), vehicle_result)

        # 7. Return error
        return {
            "code": 500,
            "data": {"vehicle_result": vehicle_result},
            "message": "Vehicle creation failure sent for error handling."
        }


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an booking...")
    app.run(host="0.0.0.0", port=5100, debug=True)



    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.