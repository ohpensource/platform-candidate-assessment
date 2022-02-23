import os
import boto3
import botocore
from flask import Flask
from aws_xray_sdk.core import xray_recorder, patch_all, plugins
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk import global_sdk_config

# Xray SDK Enable/Disable
global_sdk_config.set_sdk_enabled(False)

app = Flask(__name__)

if os.environ.get('AWS_XRAY_TRACING_NAME') is None:
  xray_svc_name = 'mvdb-api'
else:
  xray_svc_name = os.environ.get('AWS_XRAY_TRACING_NAME')

xray_recorder.configure(
    # sampling=False,
    service=xray_svc_name,
    context_missing='LOG_ERROR',
    plugins=('EC2Plugin', 'ECSPlugin', 'ElasticBeanstalkPlugin'),
    # daemon_address='127.0.0.1:3000',
    # dynamic_naming='*mysite.com*'
)

patch_all()
XRayMiddleware(app, xray_recorder)


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
