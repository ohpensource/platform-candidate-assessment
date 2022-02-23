"""
This is the mvdb module and supports all the REST actions for the
mvdb data
"""
import json
import boto3
from flask import jsonify, request
from config import db, table_name, table, app
from botocore.exceptions import ClientError
from helpers import DecimalEncoder
from aws_xray_sdk.core import xray_recorder


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
