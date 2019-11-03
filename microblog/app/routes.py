from app import app
from app.forms import ConditionForm
from flask import render_template, flash, redirect, url_for, request, session
from flask_pymongo import pymongo
from googleplaces import GooglePlaces, ranking, types, lang
from geolocation.main import GoogleMaps
from geolocation.distance_matrix.client import DistanceMatrixApiClient
import json
import requests
import random
import bcrypt

client = pymongo.MongoClient(
    "mongodb+srv://aliu:aliu@hackduke2019-nkevk.gcp.mongodb.net/test?retryWrites=true&w=majority"
)
db = client.inline
# Use your own API key for making api request calls
API_KEY = 'AIzaSyBHGtFlzUzLX4251KTO3IBfen2no0Jllic'
API_KEY2 = 'AIzaSyAzj2-Frms17wZPXVkL-YkvLgxZqikKOj4'

# Initialising the GooglePlaces constructor
google_places = GooglePlaces(API_KEY)
google_maps = GoogleMaps(API_KEY2)

address = "New York City Wall Street 12"

google_maps = GoogleMaps(API_KEY2)

location = google_maps.search(location=address)  # sends search to Google Maps.

'''
Home page
'''
@app.route('/')
def index():
    user = {'username': 'Miguel'}
    posts = [{
        'author': {
            'username': 'John'
        },
        'body': 'Beautiful day in Portland!'
    }, {
        'author': {
            'username': 'Susan'
        },
        'body': 'The Avengers movie was so cool!'
    }]
    return render_template('index.html', title='Home', user=user, posts=posts)
<<<<<<< HEAD
=======

# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    users = db.Admins
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = db.Admins
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(
                request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert(
                {'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))


        return 'That username already exists!'
    return render_template('register.html')

>>>>>>> cfef24a8407cf60218f3eb25bc2f85b525690bd2

'''
Search function
'''
@app.route('/search', methods=['GET', 'POST'])
def search():
    items = db.HospitalCost
    item = items.find()
    # for entry in client.test_database.find():
    #     print(entry)
    form = ConditionForm()
    if form.validate_on_submit():
        flash('Condition={}, remember_me={}'.format(form.condition.data,
                                                    form.remember_me.data))
        return redirect(url_for('hospitals'))
    return render_template('condition.html', title='Condition', form=form)


@app.route('/hospitals')
def hospitals():
    my_var = request.args.get('my_var', None)
    hospitalList = db.HospitalCost.find()
    hospitalNames = []

    for hospital in hospitalList:
        hospitalNames.append(hospital['HospitalName'].lower())

    getNearbyHospitals(34.5289, -86.8178, 50000, hospitalList, hospitalNames)
    fWaitHospitals = []
    fCostHospitals = []

    for hospital in waitHospitals:
        if (my_var.lower() in hospital[-1]):
            fWaitHospitals.append(hospital)

    for hospital in costHospitals:
        if (my_var.lower() in hospital[-1]):
            fCostHospitals.append(hospital)

    getNearbyHospitals(34.5289, -86.8178, 50000, hospitalList, hospitalNames)
    return render_template('hospitals.html',
                           title='Hospitals',
                           wHospitals=fWaitHospitals,
                           cHospitals=fCostHospitals)


'''
Personalized hospital page
'''
@app.route('/hospital/<hName>')
def hospitalProfile(hospitalName):
    # get the website, phone number, addy of hospital
    return render_template('baseHospital.html', hName=hospitalName)

<<<<<<< HEAD
@app.route('/admin')
def hospital_admin():
    if 'username' in session:
        return render_template("form.html")
    redirect(url_for('index'))

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      treatmentArray = []
      pippo =  request.form.to_dict()
      for x in pippo.values():
        treatmentArray.append(x)
      print(session['username'])
      '''db.Admins.update( {"name": session['username']}, {"treatments":treatmentArray})'''
      return render_template('form.html',result = result)
=======

'''
#########################################################################################################################################
#########################################################################################################################################
'''
>>>>>>> cfef24a8407cf60218f3eb25bc2f85b525690bd2

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        treatmentArray = []
        pippo = request.form.to_dict()
        for x in pippo.values():
            treatmentArray.append(x)
        print(session['username'])
        '''db.Admins.update( {"name": session['username']}, {"treatments":treatmentArray})'''
        return render_template('form.html', result=result)
#
# Supplementary functions section
#


waitHospitals = []
costHospitals = []


def getNearbyHospitals(latitude, longitude, sRadius, hospitals, hospitalNames):
    # Search all hospitals within certain radius
    # (rip the rankby=ranking.DISTANCE,searchTerm="disease" didn't work)
    query_result = google_places.nearby_search(lat_lng={
        'lat': latitude,
        'lng': longitude
    },
        radius=sRadius,
        types=[types.TYPE_HOSPITAL])
    # If any attributions related with search results print them
    '''if query_result.has_attributions:
        print(query_result.html_attributions)'''

    # Iterate over the search results
    for place in query_result.places:
        name = place.name
        # url variable to store google maps' url
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
        # print(place.geo_location['lat'], place.geo_location['lng'])
        r = requests.get(url + 'origins=' + str(latitude) + ',' +
                         str(longitude) + '&destinations=' +
                         str(place.geo_location['lat']) + ',' +
                         str(place.geo_location['lng']) + '&key=' + API_KEY)
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
                        time,  # time
                        address,
                        float(place.geo_location['lat']),  # latitude
                        float(place.geo_location['lng']),  # longitude
                        distance,  # distance
                        costHospital['AvgOutOfPocketCost'],  # cost
                        costHospital['tags']  # filters
                    )
                    costHospitals.append(costTuple)
                    break
        # regardless of whether the google hospital
        # was found in our small set of hospitals
        # we still register it, insert based on waiting time
        else:
            ref = {
                0: "urgent_care",
                1: "blood_loss",
                2: "mental_health",
                3: "infection",
                4: "pediatrics",
                5: "poison",
                6: "rash_redness",
                7: "sickness",
                8: "sports_injuries"
            }
            randNum = random.randint(3, 8)
            tagsToAdd = []
            for i in range(randNum):
                newRand = random.randint(0, 8)
                if ref[newRand] not in tagsToAdd:
                    tagsToAdd.append(ref[newRand])

            waitTuple = (name, time, address, float(place.geo_location['lat']),
                         float(place.geo_location['lng']), distance, tagsToAdd)

            waitTuple = (
                name,
                time,
                address,
                float(place.geo_location['lat']),
                float(place.geo_location['lng']),
                distance,
                tagsToAdd
            )
            waitHospitals.append(waitTuple)
