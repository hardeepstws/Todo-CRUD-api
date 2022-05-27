import uuid
import boto3

from flask import Flask, jsonify, request


TODO_TABLE = "todo-table-dev"
client = boto3.client('dynamodb', endpoint_url='http://localhost:8000')


app = Flask(__name__)


@app.route("/todos")
def get_all_todos():
    response = client.scan(TableName=TODO_TABLE)
    items = response['Items']
    return jsonify(items)
 
 
@app.route("/todos", methods=["POST"])
def create_todo():
    title = request.json.get('title')
    if not title:
        return jsonify({'error': 'Please provide title'}), 400

    id_ = str(uuid.uuid4())
 
    resp = client.put_item(
        TableName=TODO_TABLE,
        Item={
            'id': {'S': id_ },
            'title': {'S': title }
        }
    )
 
    return jsonify({
        'id': id_,
        'title': title
    })


@app.route("/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    title = request.json.get('title')
    if not title:
        return jsonify({'error': 'Please provide title'}), 400
 
    resp = client.update_item(
        TableName=TODO_TABLE,
        Key={
            'id': {'S': todo_id }
        },
        UpdateExpression="set title = :t",
        ExpressionAttributeValues={
            ':t': {'S': title }
        },
        ReturnValues="UPDATED_NEW"
    )
 
    return jsonify({
        'id': todo_id,
        'title': title
    })


@app.route("/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    resp = client.delete_item(
        TableName=TODO_TABLE,
        Key={
            'id': {'S': todo_id }
        },
        ReturnValues="ALL_OLD"
    )
 
    return jsonify({
        "message": "Todo deleted successfully"
    })