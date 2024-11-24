import os
import json
import jwt
import datetime
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest, Unauthorized
from flasgger import Swagger
import re
import requests

app = Flask(__name__)

# Swagger Configuration
template = {
    "swagger": "2.0",
    "info": {
        "title": "User Service API",
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

# Secret key for JWT
SECRET_KEY = 'your_secret_key_here'

# JSON file path
USER_FILE = "./src/users.json"

# Authentication service URL
AUTH_SERVICE_URL = "http://localhost:5003"


# Load or initialize data
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump({}, f)

# Load data into memory
with open(USER_FILE, 'r') as f:
    users = json.load(f)

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


def validate_email(email):
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength."""
    if len(password) < 4:
        return False
    return True

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    parameters:
      - name: Personal Information
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              description: Full name of the user
            email:
              type: string
              description: Email address
            password:
              type: string
              description: Password (minimum 4 characters)
            role:
              type: string
              description: User role (Admin or User)
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input
    """
    data = request.json
    
    # Validate required fields
    if not all(key in data for key in ['name', 'email', 'password', 'role']):
        raise BadRequest("Missing required fields")
    
    # Validate email format
    if not validate_email(data['email']):
        raise BadRequest("Invalid email format")
    
    # Validate password strength
    if not validate_password(data['password']):
        raise BadRequest("Password must be at least 4 characters long")
    
    # Check if email already exists
    if data['email'] in users:
        raise BadRequest("Email already registered")
    
    # Validate role
    if data['role'] not in ['Admin', 'User']:
        raise BadRequest("Invalid role. Must be 'Admin' or 'User'")
    
    # Create user
    hashed_password = generate_password_hash(data['password'])
    user = {
        'name': data['name'],
        'email': data['email'],
        'password': hashed_password,
        'role': data['role']
    }
    users[data['email']] = user
    save_data(USER_FILE, users)
    
    return jsonify({
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    }), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and provide access token
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful, returns JWT token
      401:
        description: Invalid credentials
    """
    data = request.json
    if not all(key in data for key in ['email', 'password']):
        raise BadRequest("Missing email or password")
    
    user = users.get(data['email'])
    if not user or not check_password_hash(user['password'], data['password']):
        raise Unauthorized("Invalid credentials")
    
    # Generate JWT token
    token = jwt.encode({
        'email': user['email'],
        'role': user['role'],
        'exp': datetime.datetime.now() + datetime.timedelta(hours=2)
    }, SECRET_KEY, algorithm='HS256')
    
    return jsonify({
        'token': token,
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    }), 200

@app.route('/profile/<email>', methods=['GET'])
def get_profile(email):
    """
    Get user profile by email (requires valid token)
    ---
    parameters:
      - name: email
        in: path
        type: string
        required: true
        description: Email of the user whose profile to retrieve
    responses:
      200:
        description: User profile details
      401:
        description: Invalid or missing token
      403:
        description: Forbidden - insufficient permissions
      404:
        description: User not found
    """
    # Fix 1: Proper Swagger documentation format
    # Fix 2: Validate email format
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    # Fix 3: Proper token check
    token = request.headers.get('Authorization')
    is_auth, error_msg, status_code = check_auth(token, admin_required=True)
    if not is_auth:
        return jsonify({"error": error_msg}), status_code

    # Fix 4: Proper user lookup and response
    user = users.get(email)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fix 5: Correct user data access
    return jsonify({
        'name': user['name'],    # Changed from users['name']
        'email': user['email'],  # Changed from users['email']
        'role': user['role']     # Changed from users['role']
    }), 200


if __name__ == '__main__':
    app.run(port=5002, debug=True)