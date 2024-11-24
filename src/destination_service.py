import uuid
import os
import json
from flask import Flask, request, jsonify
from flasgger import Swagger
from werkzeug.exceptions import BadRequest, NotFound
import requests

app = Flask(__name__)

# Swagger Configuration
template = {
    "swagger": "2.0",
    "info": {
        "title": "Destination Service API",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger = Swagger(app, template=template)

# JSON file paths
DESTINATION_FILE = "./src/destinations.json"

# Authentication service URL
AUTH_SERVICE_URL = "http://localhost:5003"

# Load or initialize data
if not os.path.exists(DESTINATION_FILE):
    with open(DESTINATION_FILE, 'w') as f:
        json.dump({}, f)

# Load data into memory
with open(DESTINATION_FILE, 'r') as f:
    destinations = json.load(f)

def save_data(file_path, data):
    """Save data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def check_auth(token, admin_required=False):
    """Check authentication with auth service."""
    if not token:
        return False, "Token is missing", 401
    
    headers = {'Authorization': token}
    if admin_required:
        response = requests.post(f"{AUTH_SERVICE_URL}/auth/check-admin", headers=headers)
    else:
        response = requests.post(f"{AUTH_SERVICE_URL}/auth/verify", headers=headers)
    
    return response.status_code == 200, response.json().get('error', 'Authentication failed'), response.status_code

def destination_exists(name):
    """Check if a destination with the given name already exists."""
    return any(dest['name'].lower() == name.lower() for dest in destinations.values())

@app.route('/destinations', methods=['GET'])
def get_destinations():
    """
    Retrieve all destinations
    ---
    responses:
      200:
        description: List of destinations
    """
    return jsonify(list(destinations.values())), 200
 

@app.route('/destinations', methods=['POST'])
def add_destination():
    """
    Add a new destination (Admin only)
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
            location:
              type: string
    responses:
      201:
        description: Destination created successfully
      400:
        description: Invalid input
      401:
        description: Unauthorized
      403:
        description: Forbidden - Not an admin
    """

    is_auth, error_msg, status_code = check_auth(request.headers.get('Authorization'), admin_required=True)
    if not is_auth:
        return jsonify({"error": error_msg}), status_code
   

    data = request.json
    if not all(key in data for key in ['name', 'description', 'location']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if destination name already exists
    if destination_exists(data['name']):
        return jsonify({"error": "Destination with this name already exists"}), 400
    
    destination_id = str(uuid.uuid4())
    destination = {
        'id': destination_id,
        'name': data['name'],
        'description': data['description'],
        'location': data['location']
    }
    destinations[destination_id] = destination
    save_data(DESTINATION_FILE, destinations)
    return jsonify(destination), 201

@app.route('/destinations/<id>', methods=['DELETE'])
def delete_destination(id):
    """
    Delete a destination (Admin only)
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: Destination ID
    responses:
      200:
        description: Destination deleted successfully
      404:
        description: Destination not found
      401:
        description: Unauthorized
      403:
        description: Forbidden - Not an admin
    """

    is_auth, error_msg, status_code = check_auth(request.headers.get('Authorization'), admin_required=True)
    if not is_auth:
        return jsonify({"error": error_msg}), status_code
  

    if id not in destinations:
        return jsonify({"error": "Destination not found"}), 404
    
    del destinations[id]
    save_data(DESTINATION_FILE, destinations)
    return jsonify({"message": "Destination deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5001, debug=True)