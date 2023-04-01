from flask_cors import CORS
from flask import Flask, jsonify, request
import googlemaps
import requests

app = Flask(__name__)
CORS(app)

gmaps = googlemaps.Client(key = 'AIzaSyAWm0apf-es3-DdJCkC-RimWitR5x2kFrw')

#returns the distances each of the pairs of start points and the end point
@app.route('/gmaps/vehicledistance/', methods=['GET','POST'])
def vehicledistance():
    startend = request.get_json()
    origins = []
    for origin in startend["start"]:
        origins.append((origin["lat"], origin["lng"]))
    destination = (startend["end"]["lat"], startend["end"]["lng"])
    distance = gmaps.distance_matrix(origins, destination, mode='walking')
    print(distance)
    distances = distance["rows"]
    distances_to_return = []
    for distance in distances:
        distances_to_return.append(distance["elements"][0]["distance"]["value"])
    print("distances_to_return: ", distances_to_return)
    return jsonify(
        {
            "code": 200,
            "distance": distances_to_return
        }
    )

""" @app.route('/gmaps/parkingdistance/', methods=['GET','POST'])
def parkingdistance():
    startend = request.get_json()
    origin = (startend["start"]["lat"], startend["start"]["lng"])
    destination = (startend["end"]["lat"], startend["end"]["lng"])
    distance = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
    return jsonify(
        {
            "code": 200,
            "distance": distance
        }
    ) """


if __name__ == '__main__':
    app.run(debug = True, port = 5002)

# Example of a json input taken in by the function
# {
#     "start" : {
#         "lat" : 1.42681,
#         "lng" : 103.836
#     },
#     "end" : {
#         "lat" : 1.40145,
#         "lng" : 103.818
#     }
# }

# Example of the full json output returned by the api
# {
#     "code": 200,
#     "distance": {
#         "destination_addresses": [
#             "1230 Upper Thomson Rd, Singapore 787129"
#         ],
#         "origin_addresses": [
#             "29 Yishun Central 1, Singapore 768804"
#         ],
#         "rows": [
#             {
#                 "elements": [
#                     {
#                         "distance": {
#                             "text": "5.0 km",
#                             "value": 5045
#                         },
#                         "duration": {
#                             "text": "12 mins",
#                             "value": 711
#                         },
#                         "status": "OK"
#                     }
#                 ]
#             }
#         ],
#         "status": "OK"
#     }
# }