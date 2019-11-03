# coordinates = {'lat': 36.4089, 'lng': -78.3178}

# # call the function nearby search with
# # the parameters as longitude, latitude, radius and type of place
# query_result = google_places.nearby_search(
#         lat_lng = coordinates,
#         radius = 1000,
#         types =[types.TYPE_HOSPITAL])

# # If any attributions related with search results print them
# if query_result.has_attributions:
#     print(query_result.html_attributions)

# hospitals = []
# hospitalNames = []
# with open('cleanedHospInfo.csv') as file:
#     for line in file:
#         line = line.split(',')
#         hospitals.append((line[0].lower(), line[1], line[2], line[3]))
#         hospitalNames.append(line[0].lower())

# closeHospitals = []

# # Iterate over the search results
# for place in query_result.places:
#     print(place.name)
#     print("Latitude", place.geo_location['lat'])
#     print("Longitude", place.geo_location['lng'])
#     print(place)

#     # url variable store url
#     url ='https://maps.googleapis.com/maps/api/distancematrix/json?'

#     r = requests.get(url + 'origins=' + str(coordinates['lat']) + ',' + str(coordinates['lng']) +
#                     '&destinations=' + str(place.geo_location['lat']) + ',' + str(place.geo_location['lng']) +
#                     '&key=' + API_KEY)

#     # json method of response object
#     x = r.json()

#     name = place.name
#     address = x['destination_addresses'][0]
#     distance = x['rows'][0]['elements'][0]['distance']['text']
#     time = x['rows'][0]['elements'][0]['duration']['text']
#     print(x)
#     print()

#     print(distance)
#     print(time)

#     if name.lower() in hospitalNames:
#         index = hospitalNames.index(name)
#         hospital = hospitals[index]
#         # Hospital name, price, latitude, longitude, hospital, address, distance, time
#         closeHospitals.append((hospital[0], hospital[1], hospital[2], hospital[3], address, distance, time))
#         print(hospital[0], hospital[1], hospital[2], hospital[3], address, distance, time)
