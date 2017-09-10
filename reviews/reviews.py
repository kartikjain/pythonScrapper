# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from pymongo import MongoClient
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
# mongo = PyMongo(app)
uri = "mongodb://admin:password@localhost/admin"
mongo  = MongoClient(uri)

@app.route('/hotels/<string:key>/<string:value>', methods=['GET'])
@app.route('/hotels', methods=['GET'])
def get_all_hotels(key=None,value=None):
  if key is not None and value is not None:
      hotels = mongo.platform.hotels.find({key:value},{"reviews":0})
  else:
      hotels = mongo.platform.hotels.find({},{"reviews":0})
  output = []
  for hotel in hotels:
    output.append(hotel)
  return jsonify({'result' : output})

@app.route('/hotel/<string:id>/reviews/<string:key>/<string:value>/<string:op>', methods=['GET'])
@app.route('/hotel/<string:id>/reviews', methods=['GET'])
def get_all_reviews_for_hotel(id,key=None,value=None,op=None):
  reviews = mongo.platform.hotels.find_one({"_id": id},{"reviews":1})
  output = []
  if key is not None and value is not None and op is not None:
    if op == ">":
      try:
        for review in reviews['reviews']:
          if int(review[key]) >= int(value):
            output.append(review)
      except:
        raise ValueError("That is not a valid operation!")
    elif op == "=":
      for review in reviews['reviews']:
        if str(review[key]) == str(value):
          output.append(review)
  else:
      for review in reviews['reviews']:
          output.append(review)
  return jsonify({'result' : output})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))

    #if port == 3000:
     #   app.debug = True

    app.run(host='0.0.0.0', port=port)

