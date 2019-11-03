from googleplaces import GooglePlaces, ranking, types, lang
import requests
import json

from flask_pymongo import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://aliu:aliu@hackduke2019-nkevk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.inline

# Use your own API key for making api request calls
API_KEY = 'AIzaSyBHGtFlzUzLX4251KTO3IBfen2no0Jllic'
# Initialising the GooglePlaces constructor
google_places = GooglePlaces(API_KEY)


# coordinates = {'lat': 36.4089, 'lng': -78.3178}
testLat = 33.25289
testLng = -86.8178
# start at 10000, then increment by like 1000 until you get some hospitals
searchRadius = 50000
# searchRadius = 50000

# efficiency can be improved
# To make this more efficient: cache the data points
hospitals = db.HospitalCost.find()
hospitalNames = []
for hospital in hospitals:
    hospitalNames.append(hospital['HospitalName'].lower())
# print(hospitals)
# print(hospitalNames)


# call the function nearby search with
# the parameters as longitude, latitude, radius and type of place

# query_result will store the places that google gives
# this is NOT the same as the ones we have
def getNearbyHospitals(latitude, longitude, sRadius, hospitals, hospitalNames):
    # Search all hospitals within certain radius
    # (rip the rankby=ranking.DISTANCE,searchTerm="disease" didn't work)
    query_result = google_places.nearby_search(
        lat_lng={'lat': latitude, 'lng': longitude},
        radius=sRadius,
        types=[types.TYPE_HOSPITAL]
    )
    # If any attributions related with search results print them
    if query_result.has_attributions:
        print(query_result.html_attributions)

    costHospitals = []
    waitHospitals = []
    # Iterate over the search results
    for place in query_result.places:
        # # from place we know: name, lat, long
        # name: place.name
        # lat: place.geo_location['lat']
        # long: place.geo_location['lng']

        name = place.name
        # url variable to store google maps' url
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        #print(place.geo_location['lat'], place.geo_location['lng'])
        r = requests.get(url + 'origins=' + str(latitude) + ',' + str(longitude) +
                         '&destinations=' + str(place.geo_location['lat']) + ',' + str(place.geo_location['lng']) +
                         '&key=' + API_KEY)
        x = r.json()  # json method of response object

        # from the API response, get the drive time and address
        # couldn't get the ratings...b/c hospitals don't have ratings
        address = x['destination_addresses'][0]
        # not the exact distance in seconds, use value
        time = x['rows'][0]['elements'][0]['duration']['text']
        # not the exact distance in km, use the value
        distance = x['rows'][0]['elements'][0]['distance']['text']

        # If the current hospital from Google is in our subset,
        # then we add it to the list sorted by costs
        # after sorting by waiting times
        if name.lower() in hospitalNames:
            hospitals = db.HospitalCost.find()
            for hospital in hospitals:
                if (name.upper() == hospital['HospitalName']):
                    costHospital = hospital
                    costTuple = (
                    name,  # name
                    time,                  # time
                    address,
                    float(place.geo_location['lat']),  # latitude
                    float(place.geo_location['lng']),  # longitude
                    distance,              # distance
                    costHospital['AvgOutOfPocketCost'],  # cost
                )
                costHospitals.append(costTuple)
                break
        # regardless of whether the google hospital
        # was found in our small set of hospitals
        # we still register it, insert based on waiting time
        else:
            waitTuple = (
                name,
                time,
                address,
                float(place.geo_location['lat']),
                float(place.geo_location['lng']),
                distance,
            )
            waitHospitals.append(waitTuple)
    print()
    print("Wait Hospitals: ", waitHospitals)
    print()
    print("Cost Hospitals: ", costHospitals)


getNearbyHospitals(testLat, testLng, searchRadius, hospitals, hospitalNames)
