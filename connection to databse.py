

import pymongo

# Connect to the MongoDB database
client = pymongo.MongoClient(" Connection String ")
db = client[" name of database to view collection "]
collection = db[" collection name of database "]

data = collection.find()  # it will find all threads from database

