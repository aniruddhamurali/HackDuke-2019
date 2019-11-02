from googleplaces import GooglePlaces, types, lang 
import requests 
import json 
    
# Generate an API key by going to this location 
# https://cloud.google.com /maps-platform/places/?apis = 
# places in the google developers 
  
# Use your own API key for making api request calls 
#API_KEY = 'AIzaSyDplP_jSYrYZWCYqfmG_lhFqxQRURA4jUU'
API_KEY = 'AIzaSyBHGtFlzUzLX4251KTO3IBfen2no0Jllic'
  
# Initialising the GooglePlaces constructor 
google_places = GooglePlaces(API_KEY) 
  
# call the function nearby search with 
# the parameters as longitude, latitude, 
# radius and type of place which needs to be searched of  
# type can be HOSPITAL, CAFE, BAR, CASINO, etc 
query_result = google_places.nearby_search( 
        # lat_lng ={'lat': 46.1667, 'lng': -1.15}, 
        lat_lng ={'lat': 28.4089, 'lng': 77.3178}, 
        radius = 5000, 
        types =[types.TYPE_HOSPITAL]) 
  
# If any attributions related with search results print them 
if query_result.has_attributions: 
    print (query_result.html_attributions) 
  
  
# Iterate over the search results 
for place in query_result.places: 
    # print(type(place)) 
    # place.get_details() 
    print(place.name) 
    print("Latitude", place.geo_location['lat']) 
    print("Longitude", place.geo_location['lng']) 
    print(place)
    print() 