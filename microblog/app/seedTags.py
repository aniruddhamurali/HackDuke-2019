from flask_pymongo import pymongo
import random

client = pymongo.MongoClient("mongodb+srv://aliu:aliu@hackduke2019-nkevk.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client.inline
hospitals = db.HospitalCost

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
for hospital in hospitals.find():
    randNum = random.randint(3, 9)
    tagsToAdd = []
    for i in range(randNum):
        newRand = random.randint(0, 8)
        tagsToAdd.append(ref[newRand])
    print(hospital["HospitalName"], tagsToAdd)
    hospitals.update_one(
        {"HospitalName": hospital["HospitalName"]},
        {"$set" : {"tags":tagsToAdd}}
    )