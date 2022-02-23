"""
Main module of the server file
"""
import os
import json
import mvdb
from flask import Flask, jsonify, request, render_template
from config import app
from flask_swagger_ui import get_swaggerui_blueprint

# Set variables for swagger UI
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Movies Database API"
    },
)

# create a URL route in our application for "/"

@app.route("/")
def home():
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

# List all movies

@app.route("/movies", methods=['GET'])
def get_all():
    return mvdb.get_all()

# list one specific movie

@app.route("/movies/", methods=['GET'])
def get_movie():
    return mvdb.get_movie()

# add new movie

@app.route("/movies/", methods=['POST'])
def add_movie():
    return mvdb.add_movie()


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
    app.register_blueprint(swaggerui_blueprint)
    app.run(host="0.0.0.0", debug=True)
    # app.run()
