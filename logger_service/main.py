from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

class Log:
    def __init__(self, apiKey:str, subscription:str, executionTime:float, operation: str, endpoint: str):
        self.apiKey = apiKey
        self.subscription = subscription
        self.executionTime = executionTime
        self.operation = operation
        self.endpoint = endpoint

def db_bean():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017/subscriptions')
    client = MongoClient(mongo_url)
    db = client["subscriptions"]
    return db

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/log', methods=['POST'])
def log_request():
    db = db_bean()
    collection = db["logs"]
    log = Log(request.json['apiKey'], request.json['subscription'], request.json['executionTime'], request.json['operation'], request.json['endpoint'])
    if (log):
        result = collection.insert_one(log.__dict__)
        result2 = collection.find_one({"_id": result.inserted_id})
        if (result2):
            result2['_id'] = str(result2['_id']) 
            return jsonify(result2), 201
        else:
            return jsonify({"error": "User not found and created"}), 404
    else:
        return jsonify({"error": "Request Object not valid"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)