from flask import Flask, request, jsonify
from flask_cors import CORS
import googlemaps
import os, sys

import requests
import amqp_setup
import pika
import json
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

gmaps = googlemaps.Client(key = 'AIzaSyAWm0apf-es3-DdJCkC-RimWitR5x2kFrw')
report_url = "http://localhost:5002/report"

# Sample input for this function
# {"Report": {
#     "DriverID": 3,
#     "RentalID": 3,
#     "PlateNo": "SGX1234A",
#     "Outcome": "Refund",
#     "Content": "My car door cannot open"},
# "Current Location": {"lat": 1.29715, "lng": 103.84981},
# "PaymentID": "pi_3MsMjPFZwLHtEN8W0Py49Hg7",
# "PhoneNo" : "+6597991787"}  

@app.route("/manage_issue", methods=['POST'])
def manage_issue():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            # Get the JSON data from the POST request
            full_report = request.get_json()
            report = full_report["Report"]
            payment_id = full_report["PaymentID"]
            current_location = full_report["Current Location"]
            phone_number = full_report["PhoneNo"]
            print("\nReceived an report in JSON:", report)
            #calls the appropriate function based on the outcome of the report
            if report["Outcome"] == "Refund":
                result = process_refund(report, payment_id, phone_number)
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
                "message": "manage_issue.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def process_refund(report, payment_id, phone_number):

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
    # print('\n-----Invoking payment microservice-----')
    # refund_url = "http://localhost:5006/refund-payment/" + f"{payment_id}"
    # try:
    #     refund_result = invoke_http(refund_url, method='POST')
    #     print('Refund successful', refund_result)

    # except:
    #     return {
    #             "code": 500,
    #             "message": "An error occurred in the payment microservice."
    #         }

    #5 Send SMS
    # print('\n-----Invoking SMS microservice-----')
    # sms_url = "http://localhost:5005/Twilio/send_txt_message/" + f"{report['PhoneNo']}"
    # try:
    #     sms_result = invoke_http(sms_url, method='GET')
    #     print('SMS Notification successful', sms_result)

    # except:
    #     return {
    #             "code": 500,
    #             "message": "An error occurred in the SMS microservice."
    #         }

    message = {
        "code": 200,
        "PhoneNo": phone_number,
        "message": "Your refund has been confirmed and send. Please check your bank account these few weeks. If there are any clarification or questions you have, do feel free to contact us. Thank you."
    }
    content = json.dumps(message)

    print('\n\n-----Publishing the (refund) message with routing_key=refund.sms-----')  
    # Response
    amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="refund.sms", 
            body=content, properties=pika.BasicProperties(delivery_mode=2))



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
        #get all vehicles
        get_vehicle_result = invoke_http(get_vehicle_url, method='GET')
        all_vehicles = get_vehicle_result['data']['vehicles']
        print('All vehicles retrieved successfully', all_vehicles)
        #filter available vehicles
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

    #compile list of available vehicle locations
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
    #get distances from browser location to all available vehicles
    try:
        distance = gmaps.distance_matrix(origins, destination, mode='walking')
    except:
        return {
                "code": 500,
                "message": "An error occurred in the Google Maps API."
            }
    #get vehicle with shortest distance
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