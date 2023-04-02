from flask import Flask, request, jsonify
from flask_cors import CORS
import googlemaps
import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

gmaps = googlemaps.Client(key = 'AIzaSyAWm0apf-es3-DdJCkC-RimWitR5x2kFrw')
report_url = "http://localhost:5002/report"

# Sample input for this function
# { "Report":
#   {"ReportID": 3,
#   "DriverID": 3,
#   "RentalID": 3,
#   "PlateNo": "SGX1234A",
#   "Outcome": "Replace",
#   "Content": "My car door cannot open"},
#   "Current Location": {'lat': 1.29715, 'lng': 103.84981},
#   "PaymentID": "pi_3MsMjPFZwLHtEN8W0Py49Hg7"}    

@app.route("/manage_issue", methods=['POST'])
def manage_issue():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            full_report = request.get_json()
            report = full_report["Report"]
            payment_id = full_report["PaymentID"]
            current_location = full_report["Current Location"]
            print("\nReceived an report in JSON:", report)
            # do the actual work
            # 1. Send order info {cart items}
            if report["Outcome"] == "Refund":
                result = process_refund(report, payment_id)
            else:
                result = replace_vehicle(report, current_location)
            return result

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

def process_refund(report, payment_id):

    #1 initialize report
    print('\n-----Invoking report microservice-----')
    try:
        report_result = invoke_http(report_url, method='POST', json=report)
        print('Report creation successful', report_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the report microservice."
            }

    #2 update reported vehicle status to damaged
    print('\n-----Invoking vehicle microservice-----')
    damaged_vehicle_url = "http://localhost:5003/rentalvehicle/damage/" + report["PlateNo"]
    try:
        damageupdate_result = invoke_http(damaged_vehicle_url, method='PUT')
        print('Vehicle status update successful', damageupdate_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the vehicle microservice."
            }


    #3 end rental period

    print('\n-----Invoking rental microservice-----')
    update_rental_url = "http://localhost:5001/rental/canceltrip/" + f"{report['RentalID']}"
    try:
        endrental_result = invoke_http(update_rental_url, method='PUT')
        print('Rental ended successfully', endrental_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the rental microservice."
            }


    #4 initiate refund
    print('\n-----Invoking payment microservice-----')
    refund_url = "http://localhost:5006/refund-payment/" + f"{payment_id}"
    try:
        refund_result = invoke_http(refund_url, method='POST')
        print('Refund successful', refund_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the payment microservice."
            }

    #5 Send SMS
    print('\n-----Invoking SMS microservice-----')
    sms_url = "http://localhost:5005/Twilio/send_txt_message/" + "'+6597991787'"
    try:
        sms_result = invoke_http(sms_url, method='GET')
        print('SMS Notification successful', sms_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the SMS microservice."
            }

    return {"code": 200, "message": "Successfully processed refund"}


def replace_vehicle(report, current_location):

    #1 initialize report
    print('\n-----Invoking report microservice-----')
    try:
        report_result = invoke_http(report_url, method='POST', json=report)
        print('Report creation successful', report_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the report microservice."
            }

    #2 update reported vehicle status to damaged
    print('\n-----Invoking vehicle microservice-----')
    damaged_vehicle_url = "http://localhost:5003/rentalvehicle/damage/" + report["PlateNo"]
    try:
        damageupdate_result = invoke_http(damaged_vehicle_url, method='PUT')
        print('Vehicle status update successful', damageupdate_result)

    except:
        return {
                "code": 500,
                "message": "An error occurred in the vehicle microservice."
            }
    
    #3 get available vehicles and choose nearest one
    print('\n-----Invoking vehicle microservice-----')
    get_vehicle_url = "http://localhost:5003/rentalvehicle/"
    try:
        #get available vehicles
        get_vehicle_result = invoke_http(get_vehicle_url, method='GET')
        all_vehicles = get_vehicle_result['data']['vehicles']
        print('All vehicles retrieved successfully', all_vehicles)
        available_vehicles = []
        for vehicle in all_vehicles:
            if vehicle["VehicleStatus"] == "Available":
                available_vehicles.append(vehicle)
        print('Available vehicles retrieved successfully', available_vehicles)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the vehicle microservice."
            }
    #get browser location, code below is to be changed after UI integration

    origins = []
    for vehicle in available_vehicles:
        origins.append({'lat': vehicle['Latitude'], 'lng': vehicle['Longitude']})

    startend = {"start":
            origins,
            "end":
            {"lat": current_location['lat'], "lng": current_location['lng']}
        }
    print('\n-----Invoking gmaps api-----')
    origins = []
    for origin in startend["start"]:
        origins.append((origin["lat"], origin["lng"]))
    destination = (startend["end"]["lat"], startend["end"]["lng"])
    try:
        distance = gmaps.distance_matrix(origins, destination, mode='walking')
    except:
        return {
                "code": 500,
                "message": "An error occurred in the Google Maps API."
            }
    distances = distance["rows"]
    shortest_distance = 10000000000000000000000000000000000000000000000000000000000000000
    for i in range(len(distances)):
        if distances[i]["elements"][0]["distance"]["value"] < shortest_distance:
            shortest_distance = distances[i]["elements"][0]["distance"]["value"]
            closest_vehicle = available_vehicles[i]
            
    print('Closest vehicle retrieved successfully', closest_vehicle)

    
   #4 update vehicle status to booked
    print('\n-----Invoking vehicle microservice-----')
    update_vehicle_url = "http://localhost:5003/rentalvehicle/updatebooked/" + closest_vehicle["PlateNo"]
    try:
        update_result = invoke_http(update_vehicle_url, method='PUT')
        print('Vehicle updated successfully', update_result)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the vehicle microservice."
            }

    #5 update vehicle in rental record
    print('\n-----Invoking rental microservice-----')
    update_rental_url = "http://localhost:5001/rental/" + f"{report['RentalID']}/" + closest_vehicle["PlateNo"]
    try:
        update_rental = invoke_http(update_rental_url, method='PUT')
        print('Rental record updated successfully', update_rental)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the rental microservice."
            } 
    
    return {"code": 200, "message": "Successfully processed replacement"}

if __name__ == "__main__":
    app.run(port=5100, debug=True)