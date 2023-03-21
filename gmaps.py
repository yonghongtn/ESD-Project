from flask_cors import CORS
from flask import Flask, jsonify, request
import googlemaps


app = Flask(__name__)
CORS(app)

gmaps = googlemaps.Client(key = 'AIzaSyAWm0apf-es3-DdJCkC-RimWitR5x2kFrw')

@app.route("/")
def home():
    return 'home'

#these functions return the distance between two points in meters
#without the code '["rows"][0]["elements"][0]["distance"]["value"]',
#it returns a json with all the information this api is capable of returning
#see the bottom of the page for an example of the full json
@app.route('/gmaps/vehicledistance/<latorigin>/<lngorigin>/<latdestination>/<lngdestination>')
def vehicledistance(latorigin, lngorigin, latdestination, lngdestination):
    origin = (latorigin, lngorigin)
    destination = (latdestination, lngdestination)
    distance = gmaps.distance_matrix(origin, destination, mode='walking')["rows"][0]["elements"][0]["distance"]["value"]
    return jsonify(
        {
            "code": 200,
            "distance": distance
        }
    )

@app.route('/gmaps/parkingdistance/<latorigin>/<lngorigin>/<latdestination>/<lngdestination>')
def parkingdistance(latorigin, lngorigin, latdestination, lngdestination):
    origin = (latorigin, lngorigin)
    destination = (latdestination, lngdestination)
    distance = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
    return jsonify(
        {
            "code": 200,
            "distance": distance
        }
    )


if __name__ == '__main__':
    app.run(debug = True, port = 5000)

# Example of the full json returned by the api
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