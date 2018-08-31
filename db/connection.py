import pymongo

client = pymongo.MongoClient("mongodb://admin:novell@54.68.243.229/rar")  # defaults to port 27017

db = client.rar

# print the number of documents in a collection
print(db.cool_collection.count())
