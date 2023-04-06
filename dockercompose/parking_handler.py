from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
import googlemaps
import requests
from invokes import invoke_http
from os import environ

app = Flask(__name__)
CORS(app)

#list of all URLS
parking_URL = environ.get('parking_url')
gmaps = googlemaps.Client(key = 'AIzaSyAWm0apf-es3-DdJCkC-RimWitR5x2kFrw')
rental_URL = environ.get('rental_url')
vehicle_URL = environ.get('vehicle_url')
""" 
For handling parking using coordinates
Takes in a JSON of the format:
{
    "driver_id": 1,
    "coordinates": {
        "lat": 1.2665125,
        "lng": 103.8204025
    },
    "rentalid": 1
}
 """
@app.route("/parking_handler", methods=['POST'])
def place_order():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            parking = request.get_json()
            print("\nReceived an order in JSON:", parking)

            # do the actual work
            result = processParkingHandler(parking)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processParkingHandler(parking):
    
    try:
        # 1. Get all parking spots
        # Invoke the order microservice
        print('\n-----Invoking parking microservice-----')
        parking_return = invoke_http(parking_URL, method='GET')
        print('Parking spots', parking_return)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the ParkingSpot microservice."
            }

    #Get all parking spots in a list
    parking_spots = parking_return['data']["parking spots"]
    print(parking_spots)
    #2. Get all pairs of distances between the driver and the parking spot
    driver_coordinates = parking['coordinates']
    driver_lat = driver_coordinates['lat']
    driver_lng = driver_coordinates['lng']

    origins = []
    for parking_spot in parking_spots:
        origins.append({"lat":parking_spot['Latitude'], "lng":parking_spot['Longitude']})

    parking_lat = parking_spot['Latitude']
    parking_lng = parking_spot['Longitude']

    startend = {"start":
                origins,
                "end":
                {"lat": driver_lat, "lng": driver_lng}
            }
    
    print("Sent to gmaps", startend)
    #Invoke the gmaps api
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
    print(distance)
    distances = distance["rows"]
    distances_to_return = []
    for distance in distances:
        distances_to_return.append(distance["elements"][0]["distance"]["value"])
    
    #map the distances to the parking spots
    parking_spots_with_distances = []
    for i in range(len(parking_spots)):
        parking_spots_with_distances.append({"parking_spot": parking_spots[i], "distance": distances_to_return[i]})
    print(parking_spots_with_distances)

    #if driver is not within 50 of any parking spot, return error
    if all(distance > 100 for distance in distances_to_return):
        return {"code": 400, "message": "Driver is not within 100m of any parking spot"}
    
    #3. End trip by calling the RentalTrip microservice
    try:
        #pick the parking spot with the shortest distance
        parking_spot_chosen = min(parking_spots_with_distances, key=lambda x: x['distance'])
        print("Parking spot chosen", parking_spot_chosen)
        parking_spot_id = parking_spot_chosen['parking_spot']['Code']
        print("Parking spot id", parking_spot_id)


        rental_URL = environ.get('rental_url')+ f"{parking['rentalid']}/{parking_spot_id}"
        print('\n-----Invoking rental trip microservice-----')
        
        rental_return = invoke_http(rental_URL, method='PUT')
        print('Rental return message', rental_return)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the RentalTrip microservice."
            }

    #4. Update current vehicle status to "available"
    #changed the path slightly on the rentalvehicle microservice
    try:
        print('\n-----Invoking rentalvehicle microservice-----')
        vehicle_URL = environ.get('vehicle_url') + rental_return['data']['PlateNo']
        json_to_send ={
            "parkingspotname": parking_spot_chosen['parking_spot']['Name'],
            "latitude": parking["coordinates"]["lat"],
            "longitude": parking["coordinates"]["lng"]
        }
        print("Vehicle URL", vehicle_URL)
        print("JSON to send", json_to_send)
        vehicle_return = invoke_http(vehicle_URL, method='PUT',json=json_to_send)
        print('Vehicle return message', vehicle_return)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the RentalVehicle microservice."
            }
    #5. Return back success message
    start_location_code = rental_return['data']['StartLocation']
    end_location_code = rental_return['data']['EndLocation']
    #find start and end location name
    start_location = next((item for item in parking_spots if item["Code"] == start_location_code), None)
    start_location = start_location['Name']
    end_location = next((item for item in parking_spots if item["Code"] == end_location_code), None)
    end_location = end_location['Name']
    #start time and end time
    start_time = rental_return['data']['StartTime']
    end_time = rental_return['data']['EndTime']
    vehicle_plate = rental_return['data']['PlateNo']
    totalfare = rental_return['data']['TotalFare']/100

    return {"code": 200, 
            "message": "Successfully ended trip",
            "data": {
                "start_location": start_location,
                "end_location": end_location,
                "start_time": start_time,
                "end_time": end_time,
                "vehicle_plate": vehicle_plate,
                "totalfare": totalfare
                }
            }

""" 
For handling parking using coordinates
Takes in a form of the format:
{
    "driver_id": 1,
    "rentalid": 1,
    image": "URL"
}
 """
@app.route("/parking_handler/qrcode", methods=['POST'])
def place_order_2():
    try:
        parking = request.get_json()
        print(parking)
        # do the actual work
        result = processParkingHandlerQR(parking)
        return jsonify(result), result["code"]

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500


def processParkingHandlerQR(parking):

    #1. Get parking spot details from QR code decoder
    print('\n-----Getting parking spot details from QR code decoder-----')
    try:
        parking_spot_details = invoke_http("https://api.qrserver.com/v1/read-qr-code/?fileurl=" + parking["image"], method='GET')
        parking_spot_id = int(parking_spot_details[0]['symbol'][0]['data'])
        print('Parking spot id', parking_spot_id)
    except:
        return {
                "code": 500,
                "message": "QR code decoder API failed to work."
            }
    # 3. Get all parking spots
    try:
        print('\n-----Invoking parking microservice-----')
        parking_return = invoke_http(parking_URL, method='GET')
        print('Parking spots', parking_return)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the ParkingSpot microservice."
            }
    #Get all parking spots in a list
    parking_spots = parking_return['data']["parking spots"]
    #Get the parking spot with the id from the QR code
    parking_spot_chosen = next((item for item in parking_spots if item["Code"] == parking_spot_id), None)
    print('Parking spot chosen', parking_spot_chosen)
    if parking_spot_chosen == None:
        return {
                "code": 500,
                "message": "Parking spot not found."
            }
    #4. End trip by calling the RentalTrip microservice
    try:
        
        #pick the parking spot with the shortest distance
        parking_spot_id = parking_spot_chosen['Code']
        print("Parking spot id", parking_spot_id)
        rental_URL = environ.get('rental_url') + f"{parking['rentalid']}/{parking_spot_id}"
        print('\n-----Invoking rental trip microservice-----')
        
        rental_return = invoke_http(rental_URL, method='PUT')
        print('Rental return message', rental_return)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the RentalTrip microservice."
            }

   #4. Update current vehicle status to "available"
    #changed the path slightly on the rentalvehicle microservice
    try:
        
        print('\n-----Invoking rentalvehicle microservice-----')
        vehicle_URL = environ.get('vehicle_url') + rental_return['data']['PlateNo']
        json_to_send ={
            "parkingspotname": parking_spot_chosen['Name'],
            "latitude": parking_spot_chosen["Latitude"],
            "longitude": parking_spot_chosen["Longitude"]
        }
        print("Vehicle URL", vehicle_URL)
        print("JSON to send", json_to_send)
        vehicle_return = invoke_http(vehicle_URL, method='PUT',json=json_to_send)
        print('Vehicle return message', vehicle_return)
    except:
        return {
                "code": 500,
                "message": "An error occurred in the RentalVehicle microservice."
            }
    #5. Return back success message

    start_location_code = rental_return['data']['StartLocation']
    end_location_code = rental_return['data']['EndLocation']

    #find start and end location name
    start_location = next((item for item in parking_spots if item["Code"] == start_location_code), None)
    start_location = start_location['Name']
    end_location = next((item for item in parking_spots if item["Code"] == end_location_code), None)
    end_location = end_location['Name']
    #start time and end time
    start_time = rental_return['data']['StartTime']
    end_time = rental_return['data']['EndTime']
    vehicle_plate = rental_return['data']['PlateNo']
    totalfare = rental_return['data']['TotalFare']/100

    return {"code": 200, 
            "message": "Successfully ended trip",
            "data": {
                "start_location": start_location,
                "end_location": end_location,
                "start_time": start_time,
                "end_time": end_time,
                "vehicle_plate": vehicle_plate,
                "totalfare": totalfare
                }
            }

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          " for placing an order...")
    app.run(host="0.0.0.0", port=5100, debug=True)
    # Notes for the parameters:
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program,
    #       and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.