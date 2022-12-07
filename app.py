import json
import uuid

from bson import json_util
from flask import Flask, jsonify, request
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://fewdw:{password}@iotapi.4dv1isx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
doors_db = client.door
data_collections = doors_db.data


# get all data from mongo db data document
def get_all_data():
    data = data_collections.find()
    return list(data)


def getTimeStamp():
    return datetime.datetime.today().replace(microsecond=0)


# get all data when door was locked
def get_all_locked():
    data = data_collections.find({"action": "locked"})
    return list(data)


# get all data when door was locked
def get_all_unlocked():
    data = data_collections.find({"action": "unlocked"})
    return list(data)


# get all data from a certain location
def get_all_location(location):
    data = data_collections.find({"location": location})
    return list(data)


# get all data from a certain customer
def get_all_customer(customerid):
    data = data_collections.find({"customerid": customerid})
    return list(data)


# add data to mongo db data document
# locked OR unlocked
def add_collection(action, location, customerid):
    test_document = {
        "action": action,
        "location": location,
        "customerid": customerid,
        "timestamp": getTimeStamp()
    }
    data_collections.insert_one(test_document).inserted_id


@app.route('/data/')
def get_all():
    return json.loads(json_util.dumps(get_all_data()))


# get all data using start and end
@app.route('/data/time')
def get_all_time_series():
    start = request.json["start"]
    end = request.json["end"]

    if start is None and end is not None:
        try:
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$lte": end}}
    elif end is None and start is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$gte": start}}

    elif start is not None and end is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$gte": start, "$lte": end}}

    pipeline = [{'$match': query}]
    data = list(data_collections.aggregate(pipeline))
    return json.loads(json_util.dumps(data))


# get all data using time from specific customer
@app.route('/data/customerid')
def get_all_time_series_by_customer_id():
    start = request.json["start"]
    end = request.json["end"]
    customerid = request.json["customerid"]

    if start is None and end is not None:
        try:
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$lte": end}}
    elif end is None and start is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$gte": start}}

    elif start is not None and end is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$gte": start, "$lte": end}}

    pipeline = [{
        '$match': {'customerid': customerid},
        '$match': query}]

    data = list(data_collections.aggregate(pipeline))
    return json.loads(json_util.dumps(data))


# get all data using time from specific customer
@app.route('/data/customerid/location')
def get_all_time_series_by_customer_id_and_location():
    start = request.json["start"]
    end = request.json["end"]
    customerid = request.json["customerid"]
    location = request.json["location"]

    if start is None and end is not None:
        try:
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$lte": end}}
    elif end is None and start is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$gte": start}}

    elif start is not None and end is not None:
        try:
            start = datetime.datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
            end = datetime.datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
        except Exception as e:
            return {"error": "timestamp not following format %Y-%m-%dT%H:%M:%S"}, 400
        query = {"timestamp": {"$gte": start, "$lte": end}}

    pipeline = [{
        '$match': query,
        '$match': {'customerid': customerid},
        '$match': {'location': location}}]

    data = list(data_collections.aggregate(pipeline))
    return json.loads(json_util.dumps(data))


@app.route('/data/locked', methods=['GET'])
def get_locked():
    return json.loads(json_util.dumps(get_all_locked()))


@app.route('/data/unlocked', methods=['GET'])
def get_unlocked():
    return json.loads(json_util.dumps(get_all_unlocked()))


@app.route('/data/location/<location>', methods=['GET'])
def get_location(location):
    return json.loads(json_util.dumps(get_all_location(location)))


@app.route('/data/user/<user>', methods=['GET'])
def get_data_by_user(user):
    return json.loads(json_util.dumps(get_all_customer(user)))


@app.route('/data/', methods=["POST"])
def add_new_data():
    action = request.json['action']
    if action not in ["locked", "unlocked"]:
        return {"error", "wrong type of action submitted"}, 404

    location = request.json['location']
    userid = request.json['userid']
    add_collection(action, location, userid)
    return jsonify({"data saved": f"{location} was {action} by {userid}"})


@app.route('/data/', methods=["DELETE"])
def delete_data():
    _id = ObjectId(request.json['id'])
    data_collections.delete_one({'_id': _id})
    return {str(_id): "successfully deleted"}


@app.route('/data/', methods=["PUT"])
def update_data():
    _id = ObjectId(request.json['id'])
    action = request.json['action']
    userid = request.json['userid']
    if str(action) not in ["locked", "unlocked"]:
        return {"error", "wrong action type"}, 404
    location = request.json['location']

    new_doc = {
        "action": action,
        "location": location,
        "customerid": userid,
        "timestamp": getTimeStamp()
    }
    data_collections.replace_one({"_id": _id}, new_doc)
    return {str(_id): "was updated"}


if __name__ == '__main__':
    app.run()
