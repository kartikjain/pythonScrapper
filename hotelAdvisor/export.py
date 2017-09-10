from pymongo import MongoClient
import json

uri = "mongodb://admin:password@localhost/admin"
client  = MongoClient(uri)
with open("items.json") as file:
	data = json.load(file)
client.platform.hotels.insert_many(data)


with open("reviews.json") as file:
	data = json.load(file)
for review in data:
	client.platform.hotels.update_one({'_id':review['hotel_id']},{"$addToSet": {"reviews": review}},upsert=False)