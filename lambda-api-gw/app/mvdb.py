"""
Main module of the server file
"""
import os
import json
import decimal
import os
import boto3
import botocore
import logging
import jsonpickle
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from flask import Flask, jsonify, request, render_template
from flask_lambda import FlaskLambda
from aws_xray_sdk.core import xray_recorder, patch_all

app = FlaskLambda(__name__)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

# Specify table
if os.environ.get('TABLE_NAME') is None:
  table_name = 'movies'
else:
  table_name = os.environ.get('TABLE_NAME')

# Set region
if os.environ.get('REGION') is None:
  region = 'eu-west-1'
else:
  region = os.environ.get('REGION')

print(f"region: {region}")

# Intialize the database
db = boto3.client('dynamodb', region_name=region)
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table(table_name)

# We need this class for dynamo queries
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

# create a URL route in our application for "/"

@app.route("/")
def home():
    logger.info('## ENVIRONMENT VARIABLES\r' + jsonpickle.encode(dict(**os.environ)))
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the Movies Database API'
    }
    response = jsonify(message)
    return response

# list methods

@app.route('/echo', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PATCH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route("/movies", methods=['GET'])
def get_all():
    # Create the list of mvdb from our data
    try:
        result = db.scan(TableName=table_name)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result['Items'], cls=DecimalEncoder)
        }
    finally:
        print('end')

@app.route("/movies/", methods=['GET'])
def get_movie():
    try:
        year = int(request.args['year'])
        title = request.args['title']
        result = table.get_item(Key={'year': year, 'title': title})
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result['Item'], cls=DecimalEncoder)
        }

    except ClientError as e:
        print(e.response['Error']['Message'])
    finally:
        print('end')

@app.route("/movies/", methods=['POST'])
def add_movie():
    try:
        year = int(request.args['year'])
        title = request.args['title']
        plot = request.args['plot']
        rating = request.args['rating']

        result = table.put_item(
            Item={
                'year': year,
                'title': title,
                'info': {
                    'plot': plot,
                    'rating': rating
                }
            }
        )
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result, cls=DecimalEncoder)
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
    finally:
        print('end')


if __name__ == '__main__':
    app.run(debug=True)



