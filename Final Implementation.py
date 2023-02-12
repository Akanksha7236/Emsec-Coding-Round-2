

from flask import Flask ,jsonify, request
from flask_pymongo import PyMongo
import pymongo
import pandas as pd
import csv

app = Flask(__name__)

# connection with MongoDb
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
mongo = PyMongo(app)


# CRUD Operation

from bson.json_util import dumps
from bson.objectid import ObjectId


# add Task

@app.route('/add', methods=['POST','GET'])
def add_user():
	_json = request.json
	_task = _json['task']
	_is_completed = _json['is_completed']
	_end_date = _json['end_date']
	# validate the received values
	if _task and _is_completed and _end_date and request.method == 'POST':
		
		# save details
		id = mongo.db.user.insert({'task': _task, 'is_completed': _is_completed, 'end_date':_end_date})
		resp = jsonify('Task added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/users')
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	return resp
		
@app.route('/user/<id>')
def user(id):
	user = mongo.db.user.find_one({'_id': ObjectId(id)})
	resp = dumps(user)
	return resp


#Update Task


@app.route('/update', methods=['PUT'])
def update_user():
	_json = request.json
	_id = _json['_id']
	_task = _json['task']
	_is_completed = _json['is_completed']
	_end_date = _json['end_date']		
	# validate the received values
	if _task and _is_completed and _end_date and _id and request.method == 'PUT':
		
		# save edits
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'task': _task, 'is_completed': _is_completed, 'end_date':_end_date}})
		resp = jsonify('Task updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
    

# Delete Task

@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('Task deleted successfully!')
	resp.status_code = 200
	return resp
		


# implemented pagination


# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["tasks_db"]
tasks_collection = db["tasks"]

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    page_size = 10
    page = request.args.get("page", default=1, type=int)

    start = (page - 1) * page_size
    end = start + page_size

    tasks = list(tasks_collection.find().skip(start).limit(end))
    total_tasks = tasks_collection.count_documents({})

    response = {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "page_size": page_size,
        "current_page": page
    }

    return jsonify(response), 200


# convert to csv 

@app.route("/api/tasks/csv", methods=["GET"])
def get_tasks_csv():
    tasks = list(tasks_collection.find())
    df = pd.DataFrame(tasks)

    response = df.to_csv(" path to your file where you want to save",index=False)

    return response, 200, {
        "Content-Type": "text/csv",
        "Content-Disposition": "attachment;filename=tasks.csv"
    }



# to handle error


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()