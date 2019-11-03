from app import app
from app.forms import ConditionForm
from flask import render_template, flash, redirect, url_for, request
from flask_pymongo import pymongo
from googleplaces import GooglePlaces, ranking, types, lang
import json
import requests

client = pymongo.MongoClient("mongodb+srv://aliu:aliu@hackduke2019-nkevk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.inline
hospitalList = db.HospitalCost.find()

# Use your own API key for making api request calls
API_KEY = 'AIzaSyBHGtFlzUzLX4251KTO3IBfen2no0Jllic'
# Initialising the GooglePlaces constructor
google_places = GooglePlaces(API_KEY)

hospitalNames = []
for hospital in hospitalList:
    hospitalNames.append(hospital['HospitalName'].lower())

waitHospitals = []
costHospitals = []

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

    # Iterate over the search results
    for place in query_result.places:
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
                        costHospital['tags']    # filters
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

@app.route('/')

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }

    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/condition', methods=['GET', 'POST'])
def condition():
    items = db.HospitalCost
    item = items.find()
    # for entry in client.test_database.find():
    #     print(entry)
    form = ConditionForm()
    if form.validate_on_submit():
        flash('Condition={}, remember_me={}'.format(
            form.condition.data, form.remember_me.data))
        return redirect(url_for('hospitals'))
    return render_template('condition.html', title='Condition', form=form)
    

@app.route('/hospitals')
def hospitals():
    my_var = request.args.get('my_var', None)
    getNearbyHospitals(34.5289,-86.8178, 50000, hospitalList, hospitalNames)
    print("WAIT", waitHospitals, "COST", costHospitals)
    for hospital in waitHospitals:
        print(hospital[0])
    return render_template('hospitals.html', title='Hospitals', wHospitals=waitHospitals, cHospitals=costHospitals)