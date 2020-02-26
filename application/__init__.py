import os
import datetime
from flask import Flask, request, json, jsonify, Response

from .requisition_data import RequisitionData, RequisitionDataEncoder
from rabbitmq.publisher import Publiser

from database import MongoDBInstance

app = Flask(__name__)
producer = Publiser(queue_name=os.getenv('QUEUE_NAME'), exchange_name=os.getenv('EXCHANGE_NAME'))
mongo = MongoDBInstance()


def serialize_request_data(user_id, path, date, method, user_agent):
    return json.dumps(RequisitionData(
        user_id=user_id,
        uri=path,
        access_time=date,
        request_method=method,
        user_agent=user_agent
    ), cls=RequisitionDataEncoder)


@app.route('/lists', methods=['GET'])
def lists():
    user_id = request.args.get('user_id')

    request_body = json.loads(serialize_request_data(
        user_id,
        request.path,
        datetime.datetime.now(),
        request.method,
        request.user_agent.string
    ))
    producer.publish(json.dumps(request_body))
    return jsonify(success='true', message='Success')


@app.route('/updateCommentNotes/<_id>', methods=['POST', 'PUT'])
def update_comment_notes(_id):
    user_id = request.json['user_id']

    request_body = json.loads(serialize_request_data(
        user_id,
        request.path,
        datetime.datetime.now(),
        request.method,
        request.user_agent.string
    ))
    producer.publish(json.dumps(request_body))
    return jsonify(success='true', message='Success')


@app.route('/navigationStats/<user_id>', methods=['GET', 'POST'])
def navigation_stats(user_id):
    user_id = user_id
    date = request.args.get('date')
    requests_list = [_ for _ in mongo.find_all({"user_id": user_id, "access_time": {"$lt": date}})]
    requests_count = mongo.count_documents({'user_id': user_id})
    requests_uri = [_['uri'] for _ in requests_list]
    count_uri_lists = 0
    count_update_comment = 0

    for c in requests_uri:
        if c == '/lists':
            count_uri_lists += 1
        elif c.startswith('/updateCommentNotes'):
            count_update_comment += 1

    percent_requests_lists = (requests_count * count_uri_lists) / 100
    percent_requests_update = (requests_count * count_update_comment) / 100

    return Response(f"{user_id} opened {percent_requests_lists}% /lists<br>{user_id} opened {percent_requests_update}% \
    /updateCommentNotes")