from flask import Flask, request, jsonify
import pymongo
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps

app = Flask(__name__)

class User():
    def __init__(self,id:ObjectId, apiKey:str, subscription:str):
        self._id = id
        self.apiKey = apiKey
        self.subscription = subscription

def db_bean():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/subscriptions')
    client = MongoClient(mongo_url)
    db = client["subscriptions"]
    return db

@app.route('/')
def hello_world():
    return 'Hello to my app'

@app.route('/auth/all')
def auth_all():
    db = db_bean()
    collection = db["users"]
    users = collection.find({})
    records = []
    for record in users:
        record['_id'] = str(record['_id'])  # Convert ObjectId to string for JSON serialization
        records.append(record)
    return jsonify(records)

@app.route('/auth')
def auth():
    db = db_bean()
    collection = db["users"]
    api_key = request.args.get('api_key')
    user = collection.find_one({"apiKey": api_key})
    if (user):
        user['_id'] = str(user['_id']) 
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/auth', methods=['POST'])
def insert_user():
    db = db_bean()
    collection = db["users"]
    result = collection.insert_one(request.get_json())
    result.inserted_id
    result2 = collection.find_one({"_id": result.inserted_id})
    return dumps(result2), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)